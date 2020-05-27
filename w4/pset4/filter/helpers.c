#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    //traverse row
    for (int i = 0; i < height; i++)
    {
        //traverse column
        for (int j = 0; j < width; j++)
        {
            // find average
            int avg = round((float)(image[i][j].rgbtBlue + image[i][j].rgbtRed + image[i][j].rgbtGreen) / 3);

            // insert new value
            image[i][j].rgbtBlue = avg;
            image[i][j].rgbtRed = avg;
            image[i][j].rgbtGreen = avg;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    //traverse row
    for (int i = 0; i < height; i++)
    {
        //traverse column
        for (int j = 0; j < width; j++)
        {
            // set original value
            int originalRed = image[i][j].rgbtRed;
            int originalBlue = image[i][j].rgbtBlue;
            int originalGreen = image[i][j].rgbtGreen;

            // find new value with the formula
            int sepiaRed = round(.393 * originalRed + .769 * originalGreen + .189 * originalBlue);
            int sepiaGreen = round(.349 * originalRed + .686 * originalGreen + .168 * originalBlue);
            int sepiaBlue = round(.272 * originalRed + .534 * originalGreen + .131 * originalBlue);

            // if any new value is > 255 then set as 255
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }

            // insert new value
            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    //traverse row
    for (int i = 0; i < height; i++)
    {
        //traverse column
        for (int j = 0, n = round(width / 2); j < n; j++)
        {
            // store original value
            int tempRed = image[i][j].rgbtRed;
            int tempBlue = image[i][j].rgbtBlue;
            int tempGreen = image[i][j].rgbtGreen;

            //insert new value of left side from right side value
            image[i][j].rgbtRed = image[i][width - j - 1].rgbtRed;
            image[i][j].rgbtGreen = image[i][width - j - 1].rgbtGreen;
            image[i][j].rgbtBlue = image[i][width - j - 1].rgbtBlue;

            //insert new value of right side from left side value with temp
            image[i][width - j - 1].rgbtRed = tempRed;
            image[i][width - j - 1].rgbtGreen = tempGreen;
            image[i][width - j - 1].rgbtBlue = tempBlue;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // to store new new value
    RGBTRIPLE new_image[height][width];
    
    //traverse row
    for (int i = 0; i < height; i++)
    {
        //traverse column
        for (int j = 0; j < width; j++)
        {
            // set original value
            int avgRed = 0;
            int avgGreen = 0;
            int avgBlue = 0;
            int count = 0;
            
            // find valid coordinates and add into summation
            for (int a = i - 1; a < i + 2; a++)
            {
                for (int b = j - 1; b < j + 2; b++)
                {
                    if (a >= 0 && a <= height - 1 && b >= 0 && b <= width - 1)
                    {
                        avgRed += image[a][b].rgbtRed;
                        avgGreen += image[a][b].rgbtGreen;
                        avgBlue += image[a][b].rgbtBlue;
                        count ++;
                    }   
                }
            }
            
            // divide to find average
            avgRed = round((float) avgRed / count);
            avgGreen = round((float) avgGreen / count);
            avgBlue = round((float) avgBlue / count);
            
            // insert new value
            new_image[i][j].rgbtRed = avgRed;
            new_image[i][j].rgbtGreen = avgGreen;
            new_image[i][j].rgbtBlue = avgBlue;
        }
    }
    
    //traverse row
    for (int i = 0; i < height; i++)
    {
        //traverse column
        for (int j = 0; j < width; j++)
        {
            // insert new value to the image
            image[i][j] = new_image[i][j];
        }
    }
    return;
}
