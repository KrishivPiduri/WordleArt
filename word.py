import sys
from collections import Counter


def get_word_list(filename="words.txt"):
    """
    Loads a list of 5-letter words from a text file.
    Each word should be on a new line.
    """
    try:
        with open(filename, 'r') as f:
            words = [line.strip().upper() for line in f]
            # Filter for 5-letter words just in case
            words = [word for word in words if len(word) == 5 and word.isalpha()]
        if not words:
            print(f"Error: Word list '{filename}' is empty or not found.")
            print("Please create this file and add 5-letter words to it.")
            sys.exit(1)
        return words
    except FileNotFoundError:
        print(f"Error: Word list file '{filename}' not found.")
        print("Please create this file in the same directory and add 5-letter words.")
        sys.exit(1)


def calculate_pattern(target, guess):
    """
    Calculates the Wordle color pattern for a guess against a target.
    G = Green (correct letter, correct position)
    Y = Yellow (correct letter, wrong position)
    B = Black/Gray (incorrect letter)
    """
    if len(target) != 5 or len(guess) != 5:
        return None  # Invalid input

    pattern = ["B"] * 5
    target_counts = Counter(target)

    # 1. First pass: Find Greens (G)
    for i in range(5):
        if guess[i] == target[i]:
            pattern[i] = "G"
            # Decrement count for the matched letter
            target_counts[guess[i]] -= 1

    # 2. Second pass: Find Yellows (Y) and Blacks (B)
    for i in range(5):
        # Skip if already marked as Green
        if pattern[i] == "G":
            continue

        # Check if letter is in target and hasn't been fully used up
        if guess[i] in target_counts and target_counts[guess[i]] > 0:
            pattern[i] = "Y"
            # Decrement count for the matched letter
            target_counts[guess[i]] -= 1
        else:
            pattern[i] = "B"  # Letter is not in target or all instances are used

    return "".join(pattern)


def find_guesses_for_art(target_word, art_patterns, word_list):
    """
    Searches the word_list to find a guess word for each art_pattern.
    """
    print(f"Searching for guesses for target word: {target_word}\n")
    found_guesses = []

    for pattern_to_find in art_patterns:
        found_match = False
        for guess_word in word_list:
            # Calculate the pattern for this guess
            result_pattern = calculate_pattern(target_word, guess_word)

            # Check if it matches the pattern we're looking for
            if result_pattern == pattern_to_find:
                found_guesses.append(guess_word)
                found_match = True
                break  # Move to the next pattern

        if not found_match:
            found_guesses.append(None)  # Mark that no match was found

    return found_guesses


# --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# --- MAIN PART: CONFIGURE YOUR ART HERE ---
# --- --- --- --- --- --- --- --- --- --- --- --- --- ---

if __name__ == "__main__":
    # 1. GET YOUR WORD LIST
    # This script NEEDS a word list file.
    # Create a file named "wordle_list.txt" in the same directory.
    # Add a large list of 5-letter words to it (one per line).
    # You can find lists by searching "Wordle guess list" or "5-letter word list".
    ALL_WORDS = get_word_list("words.txt")

    # 2. SET YOUR TARGET WORD
    # This is the "solution" word for your entire art piece.
    # It MUST be 5 letters and uppercase.
    TARGET_WORD = "GUISE"

    # 3. DEFINE YOUR ART
    # Create a list of 5-character strings.
    # G = Green, Y = Yellow, B = Black/Gray
    # Example: A simple 'H' shape
    ART_TO_CREATE = [
        "YBYYY",  # Example: "CHILD"
        "YBYBB",  # Example: "MIGHT"
        "YYBYY",  # Example: "RIGHT"
        "BBYBY",  # Example: "CHILD"
        "YYYBY"
    ]

    # --- Run the solver ---
    guesses = find_guesses_for_art(TARGET_WORD, ART_TO_CREATE, ALL_WORDS)

    # --- Print the results ---
    print("--- 🎨 Your Wordle Art Plan ---")
    print(f"Target Word: {TARGET_WORD}\n")

    for i, pattern in enumerate(ART_TO_CREATE):
        guess = guesses[i]
        if guess:
            print(f"For pattern {pattern}, use guess: **{guess}**")
        else:
            print(f"For pattern {pattern}, **NO GUESS FOUND** in your word list.")

    print("\n--- Done ---")