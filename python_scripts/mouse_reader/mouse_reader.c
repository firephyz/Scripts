#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <stdint.h>
#include <error.h>
#include <sys/time.h>

int main(int argc, char *argv[]) {

    if (argc != 2) {
        printf("Supply target file name.");
        exit(EXIT_FAILURE);
    }

    FILE * fifo = fopen("mouse_fifo", "wba");
    FILE * device = fopen(argv[1], "rb");

    size_t event_size = 24;
    uint8_t event_buffer[event_size];

    if (fifo == NULL) {
        perror("Failed to open fifo");
        exit(EXIT_FAILURE);
    }

    if (device == NULL) {
        perror("Failed to open device file");
        exit(EXIT_FAILURE);
    }

    while (1) {
        int read_num = fread(&event_buffer, 1, event_size, device);
        if (read_num == -1) {
            perror("Failed to read from device file");
            exit(EXIT_FAILURE);
        }
        printf("Read (%3d bytes):", read_num);
        for (int i = 0; i < 24/4; ++i) {
            printf(" %08x", *(uint32_t *)(event_buffer + i*4));
        }
        printf("\n");

        int write_num = fwrite(&event_buffer, 1, event_size, fifo);
        if (write_num == -1) {
            perror("Failed to write to fifo");
            exit(EXIT_FAILURE);
        }

        fflush(fifo);
    }

    return 0;
}
