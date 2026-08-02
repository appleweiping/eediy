#include "ring_buffer.h"

#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    ring_buffer_t buffer;
    size_t index = 0u;

    ring_buffer_init(&buffer);
    for (index = 0u; index < RING_BUFFER_CAPACITY; ++index) {
        if (!ring_buffer_push(&buffer, (uint16_t)index)) {
            (void)puts("deliberate-fault: setup failed");
            return EXIT_FAILURE;
        }
    }

    if (ring_buffer_push(&buffer, 999u)) {
        (void)puts("deliberate-fault: accepted sample 999 while full");
        return 7;
    }

    (void)puts("deliberate-fault: not observed");
    return EXIT_SUCCESS;
}
