import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Error! 2 arguments needed!")
        sys.exit()

    # TODO: Read database file into a variable
    db = []
    with open(sys.argv[1], "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            db.append(row)

    # TODO: Read DNA sequence file into a variable
    with open(sys.argv[2], "r") as f:
        sequence = f.read()

    # TODO: Find longest match of each STR in DNA sequence

    # Get names of subsequences from csv file excluding 'name'
    subsequences = list(db[0].keys())[1:]

    results = {}
    for subsequence in subsequences:
        results[subsequence] = longest_match(sequence, subsequence)

    # TODO: Check database for matching profiles

    # for every person in dna db
    for name in db:
        x = 0
        for subsequence in subsequences:
            # if person's subsequence is same as stored in results...
            if int(name[subsequence]) == results[subsequence]:
                x+=1
        if x == len(subsequences):
            print(name['name'])
            return

    print("No match")

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
