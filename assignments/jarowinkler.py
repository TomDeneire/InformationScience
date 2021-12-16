# Python3 implementation of Jaro-Winkler distance
# https://www.geeksforgeeks.org/jaro-and-jaro-winkler-similarity/

def jaro_distance(s1, s2):
    """
    Function to calculate the Jaro similarity of two strings
    """

    # If the strings are equal
    if (s1 == s2):
        return 1.0

    # Length of two strings
    len1 = len(s1)
    len2 = len(s2)

    if (len1 == 0 or len2 == 0):
        return 0.0

    # Maximum distance upto which matching is allowed
    max_dist = (max(len(s1), len(s2)) // 2) - 1

    # Count of matches
    match = 0

    # Hash for matches
    hash_s1 = [0] * len(s1)
    hash_s2 = [0] * len(s2)

    # Traverse through the first string
    for i in range(len1):

        # Check if there is any matches
        for j in range(max(0, i - max_dist),
                       min(len2, i + max_dist + 1)):

            # If there is a match
            if (s1[i] == s2[j] and hash_s2[j] == 0):
                hash_s1[i] = 1
                hash_s2[j] = 1
                match += 1
                break

    # If there is no match
    if (match == 0):
        return 0.0

    # Number of transpositions
    t = 0

    point = 0

    # Count number of occurances where two characters match but
    # there is a third matched character in between the indices
    for i in range(len1):
        if (hash_s1[i]):

            # Find the next matched character in second string
            while (hash_s2[point] == 0):
                point += 1

            if (s1[i] != s2[point]):
                point += 1
                t += 1
            else:
                point += 1

        t /= 2

    # Return the Jaro Similarity
    return ((match / len1 + match / len2
             + (match - t) / match) / 3.0)


def jaro_winkler(s1, s2):
    """
    Jaro-Winkler Similarity
    """

    jaro_dist = jaro_distance(s1, s2)

    # If the Jaro similarity is above a threshold
    if (jaro_dist > 0.7):

        # Find the length of common prefix
        prefix = 0

        for i in range(min(len(s1), len(s2))):

            # If the characters match
            if (s1[i] == s2[i]):
                prefix += 1

            # Else break
            else:
                break

        # Maximum of 4 characters are allowed in prefix
        prefix = min(4, prefix)

        # Calculate jaro winkler Similarity
        jaro_dist += 0.1 * prefix * (1 - jaro_dist)

    return jaro_dist


# Driver code
if __name__ == "__main__":

    s1 = "coat"
    s2 = "cot"

    # Print Jaro-Winkler Similarity of two strings
    print("Jaro-Winkler Similarity =", jaro_winkler(s1, s2))

# This code is contributed by AnkitRai01
