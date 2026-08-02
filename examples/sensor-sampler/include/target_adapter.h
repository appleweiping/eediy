#ifndef EEDIY_SENSOR_TARGET_ADAPTER_H
#define EEDIY_SENSOR_TARGET_ADAPTER_H

#include <stdbool.h>
#include <stdint.h>

typedef enum {
    SENSOR_START_OK = 0,
    SENSOR_START_SENSOR_MISSING,
    SENSOR_START_BUS_BUSY
} sensor_start_result_t;

typedef enum {
    SENSOR_POLL_PENDING = 0,
    SENSOR_POLL_READY,
    SENSOR_POLL_CRC_ERROR
} sensor_poll_result_t;

typedef struct {
    void *context;
    sensor_start_result_t (*start)(void *context);
    sensor_poll_result_t (*poll)(
        void *context,
        int32_t *value_milli_units
    );
    void (*cancel)(void *context);
    bool (*publish)(
        void *context,
        int32_t value_milli_units,
        uint32_t timestamp_ms
    );
} sensor_target_adapter_t;

#endif
