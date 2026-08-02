#ifndef EEDIY_SENSOR_SAMPLER_H
#define EEDIY_SENSOR_SAMPLER_H

#include "target_adapter.h"

#include <stdbool.h>
#include <stdint.h>

typedef enum {
    SAMPLER_STATE_IDLE = 0,
    SAMPLER_STATE_WAITING
} sampler_state_t;

typedef enum {
    SAMPLER_REASON_NONE = 0,
    SAMPLER_REASON_NOT_READY,
    SAMPLER_REASON_SENSOR_MISSING,
    SAMPLER_REASON_BUS_BUSY,
    SAMPLER_REASON_CRC_ERROR,
    SAMPLER_REASON_BUFFER_FULL,
    SAMPLER_REASON_DELAYED_INTERRUPT
} sampler_reason_t;

typedef struct {
    bool valid;
    int32_t value_milli_units;
    uint32_t timestamp_ms;
    sampler_reason_t reason;
} sampler_outcome_t;

typedef enum {
    SAMPLER_EVENT_REQUEST = 0,
    SAMPLER_EVENT_OUTCOME
} sampler_event_kind_t;

typedef struct {
    sampler_event_kind_t kind;
    sampler_state_t state;
    uint32_t timestamp_ms;
    uint32_t deadline_ms;
    sampler_outcome_t outcome;
} sampler_event_t;

typedef void (*sampler_log_fn)(
    const sampler_event_t *event,
    void *context
);

typedef struct {
    sensor_target_adapter_t target;
    sampler_log_fn log;
    void *log_context;
    sampler_state_t state;
    uint32_t timeout_ms;
    uint32_t deadline_ms;
    sampler_outcome_t last_outcome;
} sampler_t;

bool sampler_init(
    sampler_t *sampler,
    sensor_target_adapter_t target,
    uint32_t timeout_ms,
    sampler_log_fn log,
    void *log_context
);

bool sampler_request(sampler_t *sampler, uint32_t timestamp_ms);
bool sampler_poll(sampler_t *sampler, uint32_t timestamp_ms);
sampler_state_t sampler_state(const sampler_t *sampler);
sampler_outcome_t sampler_last_outcome(const sampler_t *sampler);

const char *sampler_state_name(sampler_state_t state);
const char *sampler_reason_name(sampler_reason_t reason);

#endif
