#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float average1 = (image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0;
            int average = round(average1);
            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //Calculating
            int sepiaRed = round((.393 * copy[i][j].rgbtRed) + (.769 * copy[i][j].rgbtGreen) + (.189 * copy[i][j].rgbtBlue));
            int sepiaGreen = round((.349 * copy[i][j].rgbtRed) + (.686 * copy[i][j].rgbtGreen) + (.168 * copy[i][j].rgbtBlue));
            int sepiaBlue = round((.272 * copy[i][j].rgbtRed) + (.534 * copy[i][j].rgbtGreen) + (.131 * copy[i][j].rgbtBlue));

            //Capping for red
            if (sepiaRed > 255)
            {
                sepiaRed-=256;
            }

            //Capping for green
            if (sepiaGreen > 255)
            {
                sepiaGreen-=256;
            }

            //Capping for blue
            if (sepiaBlue > 255)
            {
                sepiaBlue-=256;
            }

            //Setting
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
    int length = width - 1;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < (width / 2.0); j++)
        {
            int h = length - j;
            int tmp = image[i][h].rgbtRed;
            int tmp1 = image[i][h].rgbtGreen;
            int tmp2 = image[i][h].rgbtBlue;
            image[i][h].rgbtRed = image[i][j].rgbtRed;
            image[i][h].rgbtGreen = image[i][j].rgbtGreen;
            image[i][h].rgbtBlue = image[i][j].rgbtBlue;
            image[i][j].rgbtRed = tmp;
            image[i][j].rgbtGreen = tmp1;
            image[i][j].rgbtBlue = tmp2;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // To keep track of what to divide ((1 + 2) / counter [2])
            int counter = 0;

            // Values of the current pixel going to be modified later
            float red = 0.0;
            float blue = 0.0;
            float green = 0.0;

            // Automated Pattern
            int hpattern[] = {i - 1, i, i + 1};
            int wpattern[] = {j - 1, j, j + 1};

            // Nested loop to make three by three box
            for (int h = 0; h < 3; h++)
            {
                for (int w = 0; w < 3; w++)
                {
                    //if not on edge
                    if ((hpattern[h] >= 0) && (wpattern[w] >= 0))
                    {
                        red+=copy[hpattern[h]][wpattern[w]].rgbtRed;
                        blue+=copy[hpattern[h]][wpattern[w]].rgbtBlue;
                        green+=copy[hpattern[h]][wpattern[w]].rgbtGreen;

                        counter++;
                    }
                }
            }

            // Modifying the image pixels
            image[i][j].rgbtRed = round(red / counter);
            image[i][j].rgbtGreen = round(green / counter);
            image[i][j].rgbtBlue = round(blue /counter);
        }
    }
    return;
}
