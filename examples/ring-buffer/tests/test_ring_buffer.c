#include "adc_dma_adapter.h"
#include "ring_buffer.h"

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static void require_true(bool condition, const char *check_name)
{
    if (!condition) {
        (void)fprintf(
            stderr,
            "ring-buffer check=%s result=FAIL\n",
            check_name
        );
        exit(EXIT_FAILURE);
    }
    (void)printf("ring-buffer check=%s result=PASS\n", check_name);
}

static bool check_empty_and_invalid(void)
{
    ring_buffer_t buffer;
    uint16_t sample = 0u;

    ring_buffer_init(&buffer);
    return ring_buffer_is_empty(&buffer)
        && !ring_buffer_is_full(&buffer)
        && (ring_buffer_size(&buffer) == 0u)
        && !ring_buffer_pop(&buffer, &sample)
        && !ring_buffer_pop(NULL, &sample)
        && !ring_buffer_pop(&buffer, NULL)
        && !ring_buffer_push(NULL, 1u);
}

static bool check_exact_capacity_and_full_rejection(void)
{
    ring_buffer_t buffer;
    size_t index = 0u;

    ring_buffer_init(&buffer);
    for (index = 0u; index < ring_buffer_capacity(); ++index) {
        if (!ring_buffer_push(&buffer, (uint16_t)(100u + index))) {
            return false;
        }
    }

    return ring_buffer_is_full(&buffer)
        && (ring_buffer_size(&buffer) == RING_BUFFER_CAPACITY)
        && !ring_buffer_push(&buffer, 999u)
        && (ring_buffer_rejected_writes(&buffer) == 1u);
}

static bool check_fifo_order_and_wraparound(void)
{
    ring_buffer_t buffer;
    uint16_t sample = 0u;
    size_t index = 0u;

    ring_buffer_init(&buffer);
    for (index = 0u; index < RING_BUFFER_CAPACITY; ++index) {
        if (!ring_buffer_push(&buffer, (uint16_t)index)) {
            return false;
        }
    }
    for (index = 0u; index < 3u; ++index) {
        if (!ring_buffer_pop(&buffer, &sample) || (sample != index)) {
            return false;
        }
    }
    for (index = 8u; index < 11u; ++index) {
        if (!ring_buffer_push(&buffer, (uint16_t)index)) {
            return false;
        }
    }
    for (index = 3u; index < 11u; ++index) {
        if (!ring_buffer_pop(&buffer, &sample) || (sample != index)) {
            return false;
        }
    }

    return ring_buffer_is_empty(&buffer);
}

static bool check_repeated_boundary_cycles(void)
{
    ring_buffer_t buffer;
    uint16_t sample = 0u;
    size_t cycle = 0u;
    size_t index = 0u;

    ring_buffer_init(&buffer);
    for (cycle = 0u; cycle < 64u; ++cycle) {
        for (index = 0u; index < RING_BUFFER_CAPACITY; ++index) {
            if (!ring_buffer_push(
                    &buffer,
                    (uint16_t)(cycle * RING_BUFFER_CAPACITY + index)
                )) {
                return false;
            }
        }
        for (index = 0u; index < RING_BUFFER_CAPACITY; ++index) {
            const uint16_t expected =
                (uint16_t)(cycle * RING_BUFFER_CAPACITY + index);
            if (!ring_buffer_pop(&buffer, &sample) || (sample != expected)) {
                return false;
            }
        }
    }

    return ring_buffer_is_empty(&buffer);
}

static bool check_adc_dma_adapter(void)
{
    ring_buffer_t buffer;
    adc_dma_adapter_t adapter;
    const uint16_t samples[10] = {
        41u, 42u, 43u, 44u, 45u, 46u, 47u, 48u, 49u, 50u
    };

    ring_buffer_init(&buffer);
    adc_dma_adapter_init(&adapter, &buffer);

    return (
        adc_dma_adapter_on_transfer_complete(
            &adapter,
            samples,
            10u
        ) == ADC_DMA_TRANSFER_PARTIAL
    )
        && (adapter.completed_blocks == 1u)
        && (adapter.accepted_samples == RING_BUFFER_CAPACITY)
        && (adapter.dropped_samples == 2u)
        && (ring_buffer_rejected_writes(&buffer) == 2u);
}

static bool check_adapter_argument_boundary(void)
{
    ring_buffer_t buffer;
    adc_dma_adapter_t adapter;

    ring_buffer_init(&buffer);
    adc_dma_adapter_init(&adapter, &buffer);

    return (
        adc_dma_adapter_on_transfer_complete(&adapter, NULL, 0u)
            == ADC_DMA_TRANSFER_OK
    )
        && (adapter.completed_blocks == 1u)
        && (
            adc_dma_adapter_on_transfer_complete(&adapter, NULL, 1u)
                == ADC_DMA_TRANSFER_INVALID_ARGUMENT
        )
        && (adapter.completed_blocks == 1u);
}

int main(void)
{
    require_true(check_empty_and_invalid(), "empty-and-invalid");
    require_true(
        check_exact_capacity_and_full_rejection(),
        "exact-capacity-and-full"
    );
    require_true(check_fifo_order_and_wraparound(), "fifo-wraparound");
    require_true(check_repeated_boundary_cycles(), "repeated-boundary");
    require_true(check_adc_dma_adapter(), "adc-dma-adapter");
    require_true(check_adapter_argument_boundary(), "adapter-arguments");
    (void)puts("ring-buffer summary=PASS checks=6");
    return EXIT_SUCCESS;
}
