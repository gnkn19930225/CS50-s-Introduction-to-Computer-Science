#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int n = 0;
    do
    {
        n = get_int("Height: ");
    }
    while(n <= 0 || n > 8);

    for(int i = 0; i < n ; i++)
    {
        for(int j = n - 1 - i; j > 0; j--)
        {
            printf(" ");
        }
        for(int j = 0; j<=i ; j++)
        {
            printf("#");
        }
        printf("\n");

    }

}
