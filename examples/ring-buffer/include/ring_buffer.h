#ifndef EEDIY_RING_BUFFER_H
#define EEDIY_RING_BUFFER_H

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#define RING_BUFFER_CAPACITY 8u

typedef struct {
    uint16_t samples[RING_BUFFER_CAPACITY];
    size_t read_index;
    size_t write_index;
    size_t count;
    uint32_t rejected_writes;
} ring_buffer_t;

void ring_buffer_init(ring_buffer_t *buffer);
bool ring_buffer_push(ring_buffer_t *buffer, uint16_t sample);
bool ring_buffer_pop(ring_buffer_t *buffer, uint16_t *sample);
size_t ring_buffer_size(const ring_buffer_t *buffer);
size_t ring_buffer_capacity(void);
uint32_t ring_buffer_rejected_writes(const ring_buffer_t *buffer);
bool ring_buffer_is_empty(const ring_buffer_t *buffer);
bool ring_buffer_is_full(const ring_buffer_t *buffer);

#endif
