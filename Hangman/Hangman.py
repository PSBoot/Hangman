import string
import random
import os

# Print UI
def print_ui(censored_word, correct_characters, incorrect_characters, message):
    # Clear terminal
    os.system('cls||clear')
    # Print game title
    print("HANGMAN")
    print("")
    # Print hangman ascii art based on the number of incorrect guesses
    print(hangman[len(incorrect_characters)])
    print("")
    # Print the number of guesses ramining before the game is lost
    print("Guesses remaining: " + str(6 - len(incorrect_characters)))
    print("")
    # Print the word to be guessed, with unknown letters replaced by underscores
    print("Guess the word: " + censored_word)
    print("")
    # Print the correctly and incorrectly guessed letters and the incorrectly guessed words
    print("Correct guesses: " + ', '.join(correct_characters))
    print("Incorrect guesses: " + ', '.join(incorrect_characters))
    print("")
    # Print informational message based on previous input
    print(message)

# Game logic
def guessing_game(word_list):
    previous_random = 0
    play = True

    # Main game loop
    while play:

        # Get random word from word list
        this_random = random.randint(0,len(word_list)-1)

        # Ensure the random word is different from the last word, if possible
        while len(word_list) > 1 and this_random == previous_random:
            this_random = random.randint(0,len(word_list)-1)
        word = word_list[this_random]
        previous_random = this_random

        # Set game variables to starting values
        game_over = False
        won = False
        correct_characters = []
        incorrect_characters = []
        message = "The word contains " + str(len(word)) + " letters. You lose after 6 incorrect guesses. Guess the word to win. Good luck!"

        # Print game UI
        print_ui(censor_word(word, correct_characters), correct_characters, incorrect_characters, message)

        # Guessing turn loop
        while not game_over:

            # Ask for letter or word input
            print("Enter a letter or word to guess:")
            menu_input = input().lower()

            # Evaluate input
            if not menu_input or menu_input.isspace() or any(not c.isalpha() and not c == " " for c in menu_input):
                # Input is empty, contains only whitespace or contains special characters
                message = "The input \"" + menu_input + "\" is invalid."

            elif len(menu_input) == 1 and menu_input in string.ascii_letters:
                # Input is a letter
                if menu_input in correct_characters + incorrect_characters:
                    # Input letter has already been guessed
                    message = "You've already guessed the letter " + menu_input + "!"
                else:
                    if menu_input in word:
                        # Input letter is a correct guess, added to correct letters
                        correct_characters.append(menu_input)
                        message = "You guessed the word contains the letter " + menu_input + ", which is correct."
                    else:
                        # Input letter is an incorrect guess, added to incorrect letters
                        incorrect_characters.append(menu_input)
                        message = "You guessed the word contains the letter " + menu_input + ", which is incorrect."

            elif menu_input == word:
                # Input word is a correct match, game is won
                game_over = True
                won = True
                message = "You guessed the word is " + word + ", which is correct.\n\nYou win! Input 1 to play again. Input 2 to quit."
            elif menu_input in incorrect_characters:
                # Input word has already been guessed
                message = "You've already guessed the word " + menu_input + "!"
            else:
                # Input word is an incorrect guess
                incorrect_characters.append(menu_input)
                message = "You guessed the word is " + menu_input + ", which is incorrect."

            if not "_" in censor_word(word, correct_characters):
                # All letters in a word are revealed by correct guesses, game is won
                game_over = True
                won = True
                message = "You've found all the letters in the word, which was " + word + ".\n\nYou win! Input 1 to play again. Input 2 to quit."

            # Game is lost if the number of incorrect guesses reaches 6
            if len(incorrect_characters) >= 6:
                game_over = True
                message += "\n\nYou lost! The correct word was " + word + ". Input 1 to play again. Input 2 to quit."

            # Print game UI, showing the uncensored word if the game is won
            shown_word = censor_word(word, correct_characters)
            if won == True:
                shown_word = word
            print_ui(shown_word, correct_characters, incorrect_characters, message)

        # Evaluate menu input: 1 to play again, 2 to quit, any other input is invalid
        wait = True
        while wait:
            menu_input = input()
            if menu_input == "1":
                wait = False
            elif menu_input == "2":
                wait = False
                play = False
            else:
                message = "Invalid input. Input 1 to play again. Input 2 to quit."
                print_ui(shown_word, correct_characters, incorrect_characters, message)
                

# Replace letters in a word that haven't been guessed with underscores
def censor_word(word, guessed_characters):
    censored_word = ""
    for letter in word:
        if letter in guessed_characters or letter == " ":
            censored_word += letter
        else:
            censored_word += "_"
    return censored_word

# Remove special characters and capitalisation from a string, ignore strings starting with //
def sanitize_word(word):
    new_word = ""
    for character in word:
        if character in string.ascii_letters or character == " ":
            new_word += character

    if word[:2] == "//" or new_word.isspace():
        return ""
    else:
        return new_word.lower()

# Hangman ascii art
hangman = ["""
   +--+
   |  |
      |
      |
      |
      |
  =====""",
"""
   +--+
   |  |
   O  |
      |
      |
      |
  =====""",
"""
   +--+
   |  |
   O  |
   |  |
      |
      |
  =====""",
"""
   +--+
   |  |
   O  |
  /|  |
      |
      |
  =====""",
"""
   +--+
   |  |
   O  |
  /|\\ |
      |
      |
  =====""",
"""
   +--+
   |  |
   O  |
  /|\\ |
  /   |
      |
  =====""",
"""
   +--+
   |  |
   O  |
  /|\\ |
  / \\ |
      |
  ====="""]

# Read file and get words
word_list = []
try:
    file = open("words.txt", "r")
    for line in file:
        if sanitize_word(line):
            word_list.append(sanitize_word(line))
    file.close
except Exception:
    # File was not found
    pass

if len(word_list) == 0:
    word_list.append("python")

# Start game
guessing_game(word_list)