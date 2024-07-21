import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")

    # TODO: Read database file into a variable
    str_counts = []
    with open(sys.argv[1]) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            str_counts.append(row)

    # TODO: Read DNA sequence file into a variable
    dna_sequence = []
    with open(sys.argv[2]) as txtfile:
        reader = csv.reader(txtfile)
        for row in reader:
            dna_sequence = row

    # TODO: Find longest match of each STR in DNA sequence
    table = str_counts
    for index, row in enumerate(str_counts):
        for key, value in row.items():
            if key == "name":
                continue
            repeat_times = longest_match(dna_sequence[0], key)
            if repeat_times == int(value):
                table[index][key] = "True"

    # TODO: Check database for matching profiles
    for row in table:
        result = check_all_keys_true(row)
        if result != None:
            break
    if result:
        print(result)
    else:
        print("No match")
    return

def check_all_keys_true(data):
    count_true = 0

    for key, value in data.items():
        if key == "name":
            continue
        if value == "True":
            count_true += 1

    if count_true == len(data) - 1:
        return data["name"]

def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
