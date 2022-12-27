// Include required elements
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

// Define BYTE
typedef uint8_t BYTE;

// Extract command-line arguments
int main(int argc, char *argv[])
{
    // Check for proper usage
    if (argc != 2)
    {
        printf("Only one command line argument needed!\n");
        return 1;
    }

    // Open memory card
    FILE *file = fopen(argv[1], "r");

    // Check for possible issues
    if (file == NULL)
    {
        printf("Error in opening file!");
        return 1;
    }

    // Define storage array for future
    unsigned char buffer[512];

    // Define count_jepg to track no. of jpegs found
    int count_jpeg = 0;

    // Define output file
    FILE *output_file = NULL;

    // Malloc space for jpeg filename
    char *filename = malloc(8 * sizeof(char));

    // Read blocks of 512 bytes
    while (fread(buffer, 1, 512, file))
    {
        // Check for start of JPEG file
        if ((buffer[0] == 0xff) && (buffer[1] == 0xd8) && (buffer[2] == 0xff) && ((buffer[3] & 0xf0) == 0xe0))
        {
            // Create JPEG file with distinct filename
            sprintf(filename, "%03i.jpg", count_jpeg);

            // Open output file for writing
            output_file = fopen(filename, "w");

            // Update counter
            count_jpeg++;
        }

        // Check if JPEG is found
        if (output_file != NULL)
        {
            // Write to output file
            fwrite(buffer, 1, 512, output_file);
        }
    }

    // Close files and free malloced space
    free(filename);
    fclose(output_file);
    fclose(file);
}