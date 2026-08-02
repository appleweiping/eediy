#ifndef EEDIY_ADC_DMA_ADAPTER_H
#define EEDIY_ADC_DMA_ADAPTER_H

#include "ring_buffer.h"

#include <stddef.h>
#include <stdint.h>

typedef enum {
    ADC_DMA_TRANSFER_OK = 0,
    ADC_DMA_TRANSFER_PARTIAL,
    ADC_DMA_TRANSFER_INVALID_ARGUMENT
} adc_dma_transfer_status_t;

typedef struct {
    ring_buffer_t *destination;
    uint32_t completed_blocks;
    uint32_t accepted_samples;
    uint32_t dropped_samples;
} adc_dma_adapter_t;

void adc_dma_adapter_init(
    adc_dma_adapter_t *adapter,
    ring_buffer_t *destination
);

adc_dma_transfer_status_t adc_dma_adapter_on_transfer_complete(
    adc_dma_adapter_t *adapter,
    const uint16_t *samples,
    size_t sample_count
);

#endif
