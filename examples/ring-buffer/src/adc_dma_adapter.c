#include "adc_dma_adapter.h"

void adc_dma_adapter_init(
    adc_dma_adapter_t *adapter,
    ring_buffer_t *destination
)
{
    if (adapter == NULL) {
        return;
    }

    adapter->destination = destination;
    adapter->completed_blocks = 0u;
    adapter->accepted_samples = 0u;
    adapter->dropped_samples = 0u;
}

adc_dma_transfer_status_t adc_dma_adapter_on_transfer_complete(
    adc_dma_adapter_t *adapter,
    const uint16_t *samples,
    size_t sample_count
)
{
    size_t index = 0u;
    bool dropped_any = false;

    if ((adapter == NULL) || (adapter->destination == NULL)) {
        return ADC_DMA_TRANSFER_INVALID_ARGUMENT;
    }
    if ((sample_count > 0u) && (samples == NULL)) {
        return ADC_DMA_TRANSFER_INVALID_ARGUMENT;
    }

    adapter->completed_blocks += 1u;
    for (index = 0u; index < sample_count; ++index) {
        if (ring_buffer_push(adapter->destination, samples[index])) {
            adapter->accepted_samples += 1u;
        } else {
            adapter->dropped_samples += 1u;
            dropped_any = true;
        }
    }

    return dropped_any ? ADC_DMA_TRANSFER_PARTIAL : ADC_DMA_TRANSFER_OK;
}
