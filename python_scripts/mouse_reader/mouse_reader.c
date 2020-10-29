#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>
#include <signal.h>
#include <string.h>
#include <error.h>
#include <sys/time.h>

struct init_data_t {
    char * fifo_name;
    char * dev_name;
    char * log_name;
    bool debug_reads;
} init_data_t_default = {
    .fifo_name = "mouse_fifo",
    .dev_name = NULL,
    .log_name = NULL,
    .debug_reads = false
};

void gather_args(int argc, char *argv[], struct init_data_t * init_data) {
    for (int i = 1; i < argc; ++i) {
        // Option
        if (argv[i][1] == '-') {
            // Find option,value separator
            char * eq_index = strchr(argv[i], '=');
            if (eq_index == NULL) {
                fprintf(stderr, "Option argument must have a value. --<option>=<value>\n");
                exit(EXIT_FAILURE);
            }

            // Split argument into option and value strings
            size_t option_length = eq_index - argv[i];
            size_t value_length = strlen(argv[i]) - (eq_index - argv[i]) - 1;
            char * option_buffer = malloc(sizeof(char) * (option_length + 1));
            char * value_buffer = malloc(sizeof(char) * (value_length + 1));
            char ** target_string = NULL;
            strncpy(option_buffer, argv[i], option_length);
            strncpy(value_buffer, eq_index+1, value_length);

            // Match on option string
            if (strcmp(option_buffer, "--dev") == 0) {
                target_string = &init_data->dev_name;
            }
            else if (strcmp(option_buffer, "--log") == 0) {
                target_string = &init_data->log_name;
            }
            else if (strcmp(option_buffer, "--fifo") == 0) {
                target_string = &init_data->fifo_name;
            }
            else {
                fprintf(stderr, "Invalid option: %s\n", argv[i]);
                exit(EXIT_FAILURE);
            }

            // Store value string into the right place
            *target_string = malloc(sizeof(char) * strlen(value_buffer));
            strcpy(*target_string, value_buffer);

            free(option_buffer);
            free(value_buffer);
        }
        // Flag
        else {
            if (strcmp(argv[i], "-debug") == 0) {
                init_data->debug_reads = true;
            }
            else {
                fprintf(stderr, "Invalid flag: %s\n", argv[i]);
                exit(EXIT_FAILURE);
            }
        }
    }

    // Check correct configuration
    bool init_fail = false;
    if (init_data->dev_name == NULL) {
        fprintf(stderr, "Supply '--dev=' device file option.\n");
        init_fail = true;
    }

    if (init_fail) {
        fprintf(stderr, "Invalid configuration.\n");
        exit(EXIT_FAILURE);
    }
}

volatile FILE * file_fifo = NULL;
volatile FILE * file_device = NULL;
volatile FILE * file_log = NULL;

// Flush fifo and logs
void handle_sigquit() {
    fclose((FILE *)file_fifo);
    fclose((FILE *)file_device);
    fclose((FILE *)file_log);
    exit(EXIT_SUCCESS);
}

int main(int argc, char *argv[]) {
    size_t event_size = 24;
    uint8_t event_buffer[event_size];
    struct init_data_t init_data = init_data_t_default;

    ///////////////////////////////////////////////////////
    // Arg checks
    gather_args(argc, argv, &init_data);

    ///////////////////////////////////////////////////////
    // Signal handler
    signal(SIGQUIT, handle_sigquit);

    ///////////////////////////////////////////////////////
    // Open files
    file_fifo = fopen(init_data.fifo_name, "w");
    if (file_fifo == NULL) {
        perror("Failed to open fifo");
        exit(EXIT_FAILURE);
    }

    file_device = fopen(init_data.dev_name, "r");
    if (file_device == NULL) {
        perror("Failed to open device file");
        exit(EXIT_FAILURE);
    }

    if (init_data.log_name != NULL) {
        file_log = fopen(init_data.log_name, "w");
        if (file_log == NULL) {
            perror("Failed to open log");
            exit(EXIT_FAILURE);
        }
    }

    ///////////////////////////////////////////////////////
    // Run read dev, write fifo loop
    while (1) {
        // read from device
        int read_num = fread(&event_buffer, 1, event_size, (FILE *)file_device);
        if (read_num == -1) {
            perror("Failed to read from device file");
            exit(EXIT_FAILURE);
        }

        // Display read event
        if (init_data.debug_reads) {
            printf("Read (%d bytes):", read_num);
            for (int i = 0; i < event_size/4; ++i) {
                printf(" %08x", *(uint32_t *)(event_buffer + i*4));
            }
            printf("\n");
        }

        // Write event to output fd
        int write_num = fwrite(&event_buffer, 1, event_size, (FILE *)file_fifo);
        if (write_num == -1) {
            perror("Failed to write to fifo");
            exit(EXIT_FAILURE);
        }

        // Flush output fd for immediate read by another program
        fflush((FILE *)file_fifo);

        // Log event
        if (file_log != NULL) {
            for (int i = 0; i < event_size; ++i) {
                fprintf((FILE *)file_log, "%02x", event_buffer[i]);
            }
            fprintf((FILE *)file_log, "\n");
        }
    }

    return 0;
}
