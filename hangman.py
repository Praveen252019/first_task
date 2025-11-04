# hangman.py
import random
import string

WORDS = [
    "python","hangman","developer","computer","algorithm",
    "function","variable","internet","keyboard","challenge",
    "assistant","package","repository","programming","learning"
]

def display_state(word, guessed):
    displayed = " ".join(c if c in guessed else "_" for c in word)
    print("\nWord: ", displayed)

def play_hangman():
    word = random.choice(WORDS)
    guessed = set()
    wrong = set()
    max_wrong = 6

    print("Welcome to Hangman! Guess letters. You have", max_wrong, "wrong attempts.")
    while True:
        display_state(word, guessed)
        print("Wrong guesses:", " ".join(sorted(wrong)) or "None", f"({len(wrong)}/{max_wrong})")
        if all(c in guessed for c in word):
            print("\nYou won! The word was:", word)
            break
        if len(wrong) >= max_wrong:
            print("\nYou lost. The word was:", word)
            break

        choice = input("Enter a letter (or guess the whole word): ").strip().lower()
        if not choice:
            continue
        if len(choice) == 1:
            if choice not in string.ascii_lowercase:
                print("Enter a valid letter a-z.")
                continue
            if choice in guessed or choice in wrong:
                print("Already guessed.")
                continue
            if choice in word:
                print("Nice! That letter is in the word.")
                guessed.add(choice)
            else:
                print("Nope, that letter is not in the word.")
                wrong.add(choice)
        else:
            # whole word guess
            if choice == word:
                print("\nCorrect! You guessed the word:", word)
                break
            else:
                print("Wrong word guess.")
                wrong.add(choice)
                if len(wrong) >= max_wrong:
                    print("\nYou lost. The word was:", word)
                    break

if __name__ == "__main__":
    while True:
        play_hangman()
        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            print("Bye!")
            break
