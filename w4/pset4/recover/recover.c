#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

// BYTE data type
typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // exactly one command line argument handle
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }
    // open file and try to read it
    FILE *f = fopen(argv[1], "r");
    
    // if file doesn't exist or can't read handle
    if (f == NULL)
    {
        printf("Could not open %s.\n", argv[1]);
        return 1;
    }
    // buffer to read data
    BYTE buffer[512];
    // index for file numbering, start with -1 to indicate havent find yet, probability of no JPEG at all
    int count = -1;
    // "###.jpg/0" = 8 length
    char filename[8];
    // image file
    FILE *img = NULL;
    // read until end of file
    while (fread(buffer, 512, 1, f))
    {
        // if the header is in buffer
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // if the first header is found
            if (count == -1)
            {
                // pre-increment to make 000.jpg
                count++;
                // make 000.jpg
                sprintf(filename, "%03i.jpg", count);
                // open first output file to write with the 000.jpg
                img = fopen(filename, "w");
                // write into the first output file
                fwrite(buffer, 512, 1, img);
            }
            // if the header isn't first to be found
            else
            {   
                // close the previous output file
                fclose(img);
                // pre-increment
                count++;
                // make new name for output file
                sprintf(filename, "%03i.jpg", count);
                // open new output file to write with the new name
                img = fopen(filename, "w");
                // write into the new output file
                fwrite(buffer, 512, 1, img);
            }
        }
        // if header isn't in buffer
        else
        {
            // if the output file has been created
            if (count > -1)
            {
                // write data into the output file
                fwrite(buffer, 512, 1, img);
            }
        }
    }
    // close the last output file
    fclose(img);
    // close the data input file
    fclose(f);
}
