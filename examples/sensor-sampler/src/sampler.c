#include "sampler.h"

#include <stddef.h>

static void log_request(const sampler_t *sampler, uint32_t timestamp_ms)
{
    sampler_event_t event;

    if (sampler->log == NULL) {
        return;
    }

    event.kind = SAMPLER_EVENT_REQUEST;
    event.state = sampler->state;
    event.timestamp_ms = timestamp_ms;
    event.deadline_ms = sampler->deadline_ms;
    event.outcome = sampler->last_outcome;
    sampler->log(&event, sampler->log_context);
}

static void log_outcome(const sampler_t *sampler)
{
    sampler_event_t event;

    if (sampler->log == NULL) {
        return;
    }

    event.kind = SAMPLER_EVENT_OUTCOME;
    event.state = sampler->state;
    event.timestamp_ms = sampler->last_outcome.timestamp_ms;
    event.deadline_ms = sampler->deadline_ms;
    event.outcome = sampler->last_outcome;
    sampler->log(&event, sampler->log_context);
}

static void finish_invalid(
    sampler_t *sampler,
    sampler_reason_t reason,
    uint32_t timestamp_ms
)
{
    sampler->state = SAMPLER_STATE_IDLE;
    sampler->last_outcome.valid = false;
    sampler->last_outcome.value_milli_units = 0;
    sampler->last_outcome.timestamp_ms = timestamp_ms;
    sampler->last_outcome.reason = reason;
    log_outcome(sampler);
}

static void finish_valid(
    sampler_t *sampler,
    int32_t value_milli_units,
    uint32_t timestamp_ms
)
{
    sampler->state = SAMPLER_STATE_IDLE;
    sampler->last_outcome.valid = true;
    sampler->last_outcome.value_milli_units = value_milli_units;
    sampler->last_outcome.timestamp_ms = timestamp_ms;
    sampler->last_outcome.reason = SAMPLER_REASON_NONE;
    log_outcome(sampler);
}

static bool deadline_reached(uint32_t now_ms, uint32_t deadline_ms)
{
    return (now_ms - deadline_ms) < UINT32_C(0x80000000);
}

bool sampler_init(
    sampler_t *sampler,
    sensor_target_adapter_t target,
    uint32_t timeout_ms,
    sampler_log_fn log,
    void *log_context
)
{
    if ((sampler == NULL)
        || (target.start == NULL)
        || (target.poll == NULL)
        || (target.cancel == NULL)
        || (target.publish == NULL)
        || (timeout_ms == 0u)
        || (timeout_ms >= UINT32_C(0x80000000))) {
        return false;
    }

    sampler->target = target;
    sampler->log = log;
    sampler->log_context = log_context;
    sampler->state = SAMPLER_STATE_IDLE;
    sampler->timeout_ms = timeout_ms;
    sampler->deadline_ms = 0u;
    sampler->last_outcome.valid = false;
    sampler->last_outcome.value_milli_units = 0;
    sampler->last_outcome.timestamp_ms = 0u;
    sampler->last_outcome.reason = SAMPLER_REASON_NOT_READY;
    return true;
}

bool sampler_request(sampler_t *sampler, uint32_t timestamp_ms)
{
    sensor_start_result_t start_result;

    if ((sampler == NULL) || (sampler->state != SAMPLER_STATE_IDLE)) {
        return false;
    }

    start_result = sampler->target.start(sampler->target.context);
    if (start_result == SENSOR_START_SENSOR_MISSING) {
        finish_invalid(
            sampler,
            SAMPLER_REASON_SENSOR_MISSING,
            timestamp_ms
        );
        return true;
    }
    if (start_result == SENSOR_START_BUS_BUSY) {
        finish_invalid(sampler, SAMPLER_REASON_BUS_BUSY, timestamp_ms);
        return true;
    }
    if (start_result != SENSOR_START_OK) {
        return false;
    }

    sampler->state = SAMPLER_STATE_WAITING;
    sampler->deadline_ms = timestamp_ms + sampler->timeout_ms;
    log_request(sampler, timestamp_ms);
    return true;
}

bool sampler_poll(sampler_t *sampler, uint32_t timestamp_ms)
{
    sensor_poll_result_t poll_result;
    int32_t value_milli_units = 0;

    if ((sampler == NULL) || (sampler->state != SAMPLER_STATE_WAITING)) {
        return false;
    }

    if (deadline_reached(timestamp_ms, sampler->deadline_ms)) {
        sampler->target.cancel(sampler->target.context);
        finish_invalid(
            sampler,
            SAMPLER_REASON_DELAYED_INTERRUPT,
            timestamp_ms
        );
        return true;
    }

    poll_result = sampler->target.poll(
        sampler->target.context,
        &value_milli_units
    );
    if (poll_result == SENSOR_POLL_PENDING) {
        return true;
    }
    if (poll_result == SENSOR_POLL_CRC_ERROR) {
        finish_invalid(sampler, SAMPLER_REASON_CRC_ERROR, timestamp_ms);
        return true;
    }
    if (poll_result != SENSOR_POLL_READY) {
        return false;
    }

    if (!sampler->target.publish(
            sampler->target.context,
            value_milli_units,
            timestamp_ms
        )) {
        finish_invalid(sampler, SAMPLER_REASON_BUFFER_FULL, timestamp_ms);
        return true;
    }

    finish_valid(sampler, value_milli_units, timestamp_ms);
    return true;
}

sampler_state_t sampler_state(const sampler_t *sampler)
{
    return (sampler == NULL) ? SAMPLER_STATE_IDLE : sampler->state;
}

sampler_outcome_t sampler_last_outcome(const sampler_t *sampler)
{
    const sampler_outcome_t invalid_default = {
        false,
        0,
        0u,
        SAMPLER_REASON_NOT_READY
    };

    return (sampler == NULL) ? invalid_default : sampler->last_outcome;
}

const char *sampler_state_name(sampler_state_t state)
{
    switch (state) {
    case SAMPLER_STATE_IDLE:
        return "idle";
    case SAMPLER_STATE_WAITING:
        return "waiting";
    default:
        return "unknown";
    }
}

const char *sampler_reason_name(sampler_reason_t reason)
{
    switch (reason) {
    case SAMPLER_REASON_NONE:
        return "none";
    case SAMPLER_REASON_NOT_READY:
        return "not_ready";
    case SAMPLER_REASON_SENSOR_MISSING:
        return "sensor_missing";
    case SAMPLER_REASON_BUS_BUSY:
        return "bus_busy";
    case SAMPLER_REASON_CRC_ERROR:
        return "crc_error";
    case SAMPLER_REASON_BUFFER_FULL:
        return "buffer_full";
    case SAMPLER_REASON_DELAYED_INTERRUPT:
        return "delayed_interrupt";
    default:
        return "unknown";
    }
}
