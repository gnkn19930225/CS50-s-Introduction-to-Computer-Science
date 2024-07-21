#include <cs50.h>
#include <stdio.h>

bool check_card_number(long number);
char* get_card_type(long number);

int main(void)
{
    long card_number = get_long("Card Number: ");

    if (check_card_number(card_number))
    {
        printf("%s", get_card_type(card_number));
    }
    else
    {
        printf("INVALID\n");
    }
}

bool check_card_number(long number)
{
    int sum = 0;

    for (int i = 0; number != 0; i++, number /= 10)
    {
        if (i % 2 == 0)
        {
            sum += number % 10;
        }
        else
        {
            int digit = 2 * (number % 10);
            sum += digit / 10 + digit % 10;
        }
    }
    return sum % 10 == 0;
}

char* get_card_type(long number)
{
    int length = 0;
    int first_two_digits = 0;

    for (int i = 0; number != 0; i++, number /= 10)
    {
        length++;

        if (number >= 10 && number < 100)
        {
            first_two_digits = number;
        }
    }

    if (length == 15 && (first_two_digits == 34 || first_two_digits == 37))
    {
        return "AMEX\n";
    }
    else if (length == 16 && (first_two_digits >= 51 && first_two_digits <= 55))
    {
        return "MASTERCARD\n";
    }
    else if ((length == 13 || length == 16) && first_two_digits / 10 == 4)
    {
        return "VISA\n";
    }
    else
    {
        return "INVALID\n";
    }
}
