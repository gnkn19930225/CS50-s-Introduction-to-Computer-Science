#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    int avg = 0;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            avg = round((double) (image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3);
            image[i][j].rgbtBlue = avg;
            image[i][j].rgbtGreen = avg;
            image[i][j].rgbtRed = avg;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp_pixel;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0, k = width - 1, n = width / 2; j < n; j++, k--)
        {
            temp_pixel = image[i][j];
            image[i][j] = image[i][k];
            image[i][k] = temp_pixel;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    int sum_Red = 0;
    int sum_Green = 0;
    int sum_Blue = 0;
    int count = 0;
    RGBTRIPLE temp[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            sum_Red = 0;
            sum_Green = 0;
            sum_Blue = 0;
            count = 0;

            for (int x = 0; x < 3; x++)
            {
                for (int y = 0; y < 3; y++)
                {
                    if (i - 1 + x < 0 || i + x > height || j - 1 + y < 0 || j + y > width)
                    {
                        continue;
                    }
                    else
                    {
                        sum_Blue += image[i - 1 + x][j - 1 + y].rgbtBlue;
                        sum_Green += image[i - 1 + x][j - 1 + y].rgbtGreen;
                        sum_Red += image[i - 1 + x][j - 1 + y].rgbtRed;
                        count++;
                    }
                }
            }

            // Stores the average
            temp[i][j].rgbtRed = round((double) sum_Red / count);
            temp[i][j].rgbtGreen = round((double) sum_Green / count);
            temp[i][j].rgbtBlue = round((double) sum_Blue / count);
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = temp[i][j];
        }
    }

    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    const int Gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    const int Gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    int sumGx_red = 0, sumGx_green = 0, sumGx_blue = 0;
    int sumGy_red = 0, sumGy_green = 0, sumGy_blue = 0;

    RGBTRIPLE temp[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            sumGx_red = 0, sumGx_green = 0, sumGx_blue = 0;
            sumGy_red = 0, sumGy_green = 0, sumGy_blue = 0;

            for (int x = 0; x < 3; x++)
            {
                for (int y = 0; y < 3; y++)
                {
                    if (i - 1 + x < 0 || i + x > height || j - 1 + y < 0 || j + y > width)
                    {
                        continue;
                    }
                    else
                    {
                        sumGx_red += (image[i - 1 + x][j - 1 + y].rgbtRed * Gx[x][y]);
                        sumGx_green += (image[i - 1 + x][j - 1 + y].rgbtGreen * Gx[x][y]);
                        sumGx_blue += (image[i - 1 + x][j - 1 + y].rgbtBlue * Gx[x][y]);

                        sumGy_red += (image[i - 1 + x][j - 1 + y].rgbtRed * Gy[x][y]);
                        sumGy_green += (image[i - 1 + x][j - 1 + y].rgbtGreen * Gy[x][y]);
                        sumGy_blue += (image[i - 1 + x][j - 1 + y].rgbtBlue * Gy[x][y]);
                    }
                }
            }

            int red = round(sqrt(pow(sumGx_red, 2) + pow(sumGy_red, 2)));
            int green = round(sqrt(pow(sumGx_green, 2) + pow(sumGy_green, 2)));
            int blue = round(sqrt(pow(sumGx_blue, 2) + pow(sumGy_blue, 2)));

            temp[i][j].rgbtRed = red > 255 ? 255 : red;
            temp[i][j].rgbtGreen = green > 255 ? 255 : green;
            temp[i][j].rgbtBlue = blue > 255 ? 255 : blue;
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = temp[i][j];
        }
    }

    return;
}
