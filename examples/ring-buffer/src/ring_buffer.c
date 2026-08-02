#include "ring_buffer.h"

void ring_buffer_init(ring_buffer_t *buffer)
{
    if (buffer == NULL) {
        return;
    }

    buffer->read_index = 0u;
    buffer->write_index = 0u;
    buffer->count = 0u;
    buffer->rejected_writes = 0u;
}

bool ring_buffer_push(ring_buffer_t *buffer, uint16_t sample)
{
    if (buffer == NULL) {
        return false;
    }

    if (buffer->count == RING_BUFFER_CAPACITY) {
#if defined(RING_BUFFER_DELIBERATE_FULL_FAULT)
        /*
         * Deliberate teaching fault: silently overwrite the oldest sample
         * and report success even though this buffer's contract is
         * reject-on-full. Only the separate fault target defines this macro.
         */
        buffer->samples[buffer->write_index] = sample;
        buffer->write_index =
            (buffer->write_index + 1u) % RING_BUFFER_CAPACITY;
        buffer->read_index =
            (buffer->read_index + 1u) % RING_BUFFER_CAPACITY;
        return true;
#else
        buffer->rejected_writes += 1u;
        return false;
#endif
    }

    buffer->samples[buffer->write_index] = sample;
    buffer->write_index =
        (buffer->write_index + 1u) % RING_BUFFER_CAPACITY;
    buffer->count += 1u;
    return true;
}

bool ring_buffer_pop(ring_buffer_t *buffer, uint16_t *sample)
{
    if ((buffer == NULL) || (sample == NULL) || (buffer->count == 0u)) {
        return false;
    }

    *sample = buffer->samples[buffer->read_index];
    buffer->read_index =
        (buffer->read_index + 1u) % RING_BUFFER_CAPACITY;
    buffer->count -= 1u;
    return true;
}

size_t ring_buffer_size(const ring_buffer_t *buffer)
{
    return (buffer == NULL) ? 0u : buffer->count;
}

size_t ring_buffer_capacity(void)
{
    return RING_BUFFER_CAPACITY;
}

uint32_t ring_buffer_rejected_writes(const ring_buffer_t *buffer)
{
    return (buffer == NULL) ? 0u : buffer->rejected_writes;
}

bool ring_buffer_is_empty(const ring_buffer_t *buffer)
{
    return (buffer == NULL) || (buffer->count == 0u);
}

bool ring_buffer_is_full(const ring_buffer_t *buffer)
{
    return (buffer != NULL) && (buffer->count == RING_BUFFER_CAPACITY);
}
