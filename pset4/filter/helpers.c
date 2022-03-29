#include "helpers.h"
#include <math.h>
#include <stdio.h>
#include<stdlib.h>
// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            float sum = image[h][w].rgbtRed + image[h][w].rgbtBlue + image[h][w].rgbtGreen;
            sum = round(sum / 3);
            image[h][w].rgbtRed = sum, image[h][w].rgbtBlue = sum, image[h][w].rgbtGreen = sum;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int ogGreen, ogBlue, ogRed;
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            ogGreen = image[h][w].rgbtGreen, ogBlue = image[h][w].rgbtBlue, ogRed = image[h][w].rgbtRed;
            float NewGreen, NewBlue, NewRed;
            NewGreen = .349 * ogRed + .686 * ogGreen + .168 * ogBlue;
            NewBlue = .272 * ogRed + .534 * ogGreen + .131 * ogBlue;
            NewRed = .393 * ogRed + .769 * ogGreen + .189 * ogBlue;

            NewGreen = (NewGreen > 255) ? 255 : round(NewGreen);
            NewBlue = (NewBlue > 255) ? 255 : round(NewBlue);
            NewRed = (NewRed > 255) ? 255 : round(NewRed);

            image[h][w].rgbtRed = NewRed, image[h][w].rgbtBlue = NewBlue, image[h][w].rgbtGreen = NewGreen;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temporary;
    
    for (int h = 0; h < height; h++)
    {

        for (int w = 0; w < round(width / 2) ; w++)
        {
            temporary = image[h][w];
            image[h][w] = image[h][width - 1 - w];
            image[h][width - 1 - w] = temporary;
        }

    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    float counter;
    RGBTRIPLE avg[height][width];
    RGBTRIPLE copy[height][width];
    float sumR = 0, sumG = 0, sumB = 0;

    for (int h = 0; h < height; h++)
    {

        for (int w = 0; w < width; w++)
        {
            copy[h][w] = image[h][w];
        }
    }

    for (int h = 0; h < height; h++)
    {

        for (int w = 0; w < width; w++)
        {
            counter = 0;
            sumR = 0, sumG = 0, sumB = 0;
            for (int c = -1; c < 2; c++)
            {
                for (int a = -1; a < 2; a++)
                {
                    if (w + c >= 0 && w + c < width && h + a >= 0 && h + a < height)
                    {
                        sumR += copy[h + a][w + c].rgbtRed;
                        sumG += copy[h + a][w + c].rgbtGreen;
                        sumB += copy[h + a][w + c].rgbtBlue;
                        counter++;
                    }

                }
            }

            avg[h][w].rgbtRed = round(sumR / counter);
            avg[h][w].rgbtGreen = round(sumG / counter);
            avg[h][w].rgbtBlue = round(sumB / counter);

            if (avg[h][w].rgbtRed > 255)
            {
                
                avg[h][w].rgbtRed = 255;
                
            }

            else if (avg[h][w].rgbtGreen > 255)
            {
                
                avg[h][w].rgbtGreen = 255;
                
            }
            
            else if (avg[h][w].rgbtBlue > 255)
            {
                
                avg[h][w].rgbtBlue = 255;
                
            }


            image[h][w] = avg[h][w];

        }
    }
    return;
}
