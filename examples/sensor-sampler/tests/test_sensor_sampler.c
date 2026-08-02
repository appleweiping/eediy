#include "sampler.h"
#include "target_adapter.h"

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef enum {
    MOCK_NORMAL = 0,
    MOCK_SENSOR_MISSING,
    MOCK_BUS_BUSY,
    MOCK_CRC_ERROR,
    MOCK_BUFFER_FULL,
    MOCK_DELAYED_INTERRUPT
} mock_scenario_t;

typedef struct {
    mock_scenario_t scenario;
    uint32_t poll_count;
    uint32_t cancel_count;
    uint32_t publish_count;
    int32_t published_value;
    uint32_t published_timestamp_ms;
} mock_target_t;

typedef struct {
    const char *scenario_name;
    uint32_t event_count;
} log_context_t;

static void fail_check(const char *message)
{
    (void)fprintf(stderr, "sensor-sampler assertion=FAIL detail=%s\n", message);
    exit(EXIT_FAILURE);
}

static void require_true(bool condition, const char *message)
{
    if (!condition) {
        fail_check(message);
    }
}

static sensor_start_result_t mock_start(void *context)
{
    const mock_target_t *mock = (const mock_target_t *)context;

    if (mock->scenario == MOCK_SENSOR_MISSING) {
        return SENSOR_START_SENSOR_MISSING;
    }
    if (mock->scenario == MOCK_BUS_BUSY) {
        return SENSOR_START_BUS_BUSY;
    }
    return SENSOR_START_OK;
}

static sensor_poll_result_t mock_poll(
    void *context,
    int32_t *value_milli_units
)
{
    mock_target_t *mock = (mock_target_t *)context;

    mock->poll_count += 1u;
    if (mock->scenario == MOCK_DELAYED_INTERRUPT) {
        return SENSOR_POLL_PENDING;
    }
    if (mock->scenario == MOCK_CRC_ERROR) {
        return SENSOR_POLL_CRC_ERROR;
    }

    *value_milli_units = 2500;
    return SENSOR_POLL_READY;
}

static void mock_cancel(void *context)
{
    mock_target_t *mock = (mock_target_t *)context;
    mock->cancel_count += 1u;
}

static bool mock_publish(
    void *context,
    int32_t value_milli_units,
    uint32_t timestamp_ms
)
{
    mock_target_t *mock = (mock_target_t *)context;

    if (mock->scenario == MOCK_BUFFER_FULL) {
        return false;
    }

    mock->publish_count += 1u;
    mock->published_value = value_milli_units;
    mock->published_timestamp_ms = timestamp_ms;
    return true;
}

static void print_event(const sampler_event_t *event, void *context)
{
    log_context_t *log_context = (log_context_t *)context;

    log_context->event_count += 1u;
    if (event->kind == SAMPLER_EVENT_REQUEST) {
        (void)printf(
            "scenario=%s event=request t_ms=%u state=%s deadline_ms=%u\n",
            log_context->scenario_name,
            event->timestamp_ms,
            sampler_state_name(event->state),
            event->deadline_ms
        );
        return;
    }

    (void)printf(
        "scenario=%s event=outcome t_ms=%u validity=%s "
        "value_milli=%ld reason=%s state=%s\n",
        log_context->scenario_name,
        event->outcome.timestamp_ms,
        event->outcome.valid ? "valid" : "invalid",
        (long)event->outcome.value_milli_units,
        sampler_reason_name(event->outcome.reason),
        sampler_state_name(event->state)
    );
}

static sampler_t initialize_sampler(
    mock_target_t *mock,
    log_context_t *log_context
)
{
    sampler_t sampler;
    const sensor_target_adapter_t target = {
        mock,
        mock_start,
        mock_poll,
        mock_cancel,
        mock_publish
    };

    require_true(
        sampler_init(&sampler, target, 5u, print_event, log_context),
        "sampler_init"
    );
    return sampler;
}

static void run_normal(void)
{
    mock_target_t mock = {MOCK_NORMAL, 0u, 0u, 0u, 0, 0u};
    log_context_t log_context = {"normal", 0u};
    sampler_t sampler = initialize_sampler(&mock, &log_context);
    const sampler_outcome_t initial = sampler_last_outcome(&sampler);
    sampler_outcome_t outcome;

    (void)printf(
        "scenario=default_safe event=state t_ms=%u validity=%s "
        "value_milli=%ld reason=%s state=%s\n",
        initial.timestamp_ms,
        initial.valid ? "valid" : "invalid",
        (long)initial.value_milli_units,
        sampler_reason_name(initial.reason),
        sampler_state_name(sampler_state(&sampler))
    );
    require_true(!initial.valid, "default must be invalid");
    require_true(initial.value_milli_units == 0, "default value must be zero");
    require_true(
        initial.reason == SAMPLER_REASON_NOT_READY,
        "default reason must be not_ready"
    );

    require_true(sampler_request(&sampler, 0u), "normal request");
    require_true(sampler_poll(&sampler, 1u), "normal poll");
    outcome = sampler_last_outcome(&sampler);
    require_true(outcome.valid, "normal outcome valid");
    require_true(outcome.value_milli_units == 2500, "normal value");
    require_true(mock.publish_count == 1u, "normal publish count");
    require_true(mock.published_timestamp_ms == 1u, "normal timestamp");
    require_true(log_context.event_count == 2u, "normal event count");
}

static void run_immediate_fault(
    mock_scenario_t scenario,
    const char *scenario_name,
    sampler_reason_t expected_reason
)
{
    mock_target_t mock = {scenario, 0u, 0u, 0u, 0, 0u};
    log_context_t log_context = {scenario_name, 0u};
    sampler_t sampler = initialize_sampler(&mock, &log_context);
    sampler_outcome_t outcome;

    require_true(sampler_request(&sampler, 0u), "immediate fault request");
    outcome = sampler_last_outcome(&sampler);
    require_true(!outcome.valid, "immediate fault invalid");
    require_true(outcome.value_milli_units == 0, "immediate fault default");
    require_true(outcome.reason == expected_reason, "immediate fault reason");
    require_true(log_context.event_count == 1u, "immediate fault event count");
}

static void run_poll_fault(
    mock_scenario_t scenario,
    const char *scenario_name,
    sampler_reason_t expected_reason
)
{
    mock_target_t mock = {scenario, 0u, 0u, 0u, 0, 0u};
    log_context_t log_context = {scenario_name, 0u};
    sampler_t sampler = initialize_sampler(&mock, &log_context);
    sampler_outcome_t outcome;

    require_true(sampler_request(&sampler, 0u), "poll fault request");
    require_true(sampler_poll(&sampler, 1u), "poll fault poll");
    outcome = sampler_last_outcome(&sampler);
    require_true(!outcome.valid, "poll fault invalid");
    require_true(outcome.value_milli_units == 0, "poll fault default");
    require_true(outcome.reason == expected_reason, "poll fault reason");
    require_true(log_context.event_count == 2u, "poll fault event count");
}

static void run_delayed_interrupt(void)
{
    mock_target_t mock = {MOCK_DELAYED_INTERRUPT, 0u, 0u, 0u, 0, 0u};
    log_context_t log_context = {"delayed_interrupt", 0u};
    sampler_t sampler = initialize_sampler(&mock, &log_context);
    sampler_outcome_t outcome;

    require_true(sampler_request(&sampler, 0u), "delayed request");
    require_true(sampler_poll(&sampler, 1u), "delayed first poll");
    require_true(sampler_poll(&sampler, 4u), "delayed second poll");
    require_true(
        sampler_state(&sampler) == SAMPLER_STATE_WAITING,
        "must wait before deadline"
    );
    require_true(sampler_poll(&sampler, 5u), "delayed timeout poll");
    outcome = sampler_last_outcome(&sampler);
    require_true(!outcome.valid, "delayed outcome invalid");
    require_true(outcome.value_milli_units == 0, "delayed default");
    require_true(
        outcome.reason == SAMPLER_REASON_DELAYED_INTERRUPT,
        "delayed reason"
    );
    require_true(mock.poll_count == 2u, "no target poll at deadline");
    require_true(mock.cancel_count == 1u, "cancel once at deadline");
    require_true(log_context.event_count == 2u, "delayed event count");
}

static void check_api_boundaries(void)
{
    sampler_t sampler;
    const sensor_target_adapter_t empty_target = {
        NULL,
        NULL,
        NULL,
        NULL,
        NULL
    };
    mock_target_t mock = {MOCK_DELAYED_INTERRUPT, 0u, 0u, 0u, 0, 0u};
    const sensor_target_adapter_t target = {
        &mock,
        mock_start,
        mock_poll,
        mock_cancel,
        mock_publish
    };
    sampler_t initialized;

    require_true(
        !sampler_init(&sampler, empty_target, 5u, NULL, NULL),
        "reject incomplete target"
    );
    require_true(
        !sampler_init(&sampler, empty_target, 0u, NULL, NULL),
        "reject zero timeout"
    );
    require_true(
        !sampler_init(
            &sampler,
            target,
            UINT32_C(0x80000000),
            NULL,
            NULL
        ),
        "reject ambiguous wraparound timeout"
    );
    require_true(
        sampler_init(&initialized, target, 5u, NULL, NULL),
        "boundary sampler_init"
    );
    require_true(
        !sampler_poll(&initialized, 0u),
        "reject poll while idle"
    );
    require_true(
        sampler_request(&initialized, 0u),
        "boundary first request"
    );
    require_true(
        !sampler_request(&initialized, 1u),
        "reject concurrent request"
    );
}

static void check_wrapped_deadline(void)
{
    mock_target_t mock = {MOCK_DELAYED_INTERRUPT, 0u, 0u, 0u, 0, 0u};
    const sensor_target_adapter_t target = {
        &mock,
        mock_start,
        mock_poll,
        mock_cancel,
        mock_publish
    };
    sampler_t sampler;
    sampler_outcome_t outcome;

    require_true(
        sampler_init(&sampler, target, 5u, NULL, NULL),
        "wrapped sampler_init"
    );
    require_true(
        sampler_request(&sampler, UINT32_MAX - 2u),
        "wrapped request"
    );
    require_true(sampler_poll(&sampler, UINT32_MAX), "wrapped first poll");
    require_true(sampler_poll(&sampler, 1u), "wrapped second poll");
    require_true(
        sampler_state(&sampler) == SAMPLER_STATE_WAITING,
        "wrapped deadline must remain pending"
    );
    require_true(sampler_poll(&sampler, 2u), "wrapped timeout poll");
    outcome = sampler_last_outcome(&sampler);
    require_true(
        outcome.reason == SAMPLER_REASON_DELAYED_INTERRUPT,
        "wrapped deadline reason"
    );
    require_true(outcome.timestamp_ms == 2u, "wrapped deadline timestamp");
    require_true(mock.poll_count == 2u, "wrapped target poll count");
    require_true(mock.cancel_count == 1u, "wrapped cancel count");
}

int main(void)
{
    run_normal();
    run_immediate_fault(
        MOCK_SENSOR_MISSING,
        "sensor_missing",
        SAMPLER_REASON_SENSOR_MISSING
    );
    run_immediate_fault(
        MOCK_BUS_BUSY,
        "bus_busy",
        SAMPLER_REASON_BUS_BUSY
    );
    run_poll_fault(
        MOCK_CRC_ERROR,
        "crc_error",
        SAMPLER_REASON_CRC_ERROR
    );
    run_poll_fault(
        MOCK_BUFFER_FULL,
        "buffer_full",
        SAMPLER_REASON_BUFFER_FULL
    );
    run_delayed_interrupt();
    check_api_boundaries();
    check_wrapped_deadline();
    (void)puts("sensor-sampler summary=PASS scenarios=6");
    return EXIT_SUCCESS;
}
