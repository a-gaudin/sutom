import os
import pandas as pd

def check_inputs(word: str, colors: str):
    """ Raise errors if inputs are incoherent or are not handled """
    if len(word) != len(colors):
        raise ValueError("Word and Colors should be the same length") 

    if (len(word) < 4 or len(word) > 12):
        raise ValueError("This program only handles words from 4 to 12 letters")

def get_dictionary(file_path: str) -> pd.DataFrame:
    """ Get a dictionary for the word's length, 4096 words sorted by popularity
    Args:
        file_path (string): path to distionary as a csv file
    Returns:
        (pd.DataFrame): dictionary for word's length as a single-column df
    """
    dictionary_df = pd.read_csv(file_path, sep=" ", header=None)
    dictionary_df.columns = ["words"]
    return dictionary_df

def create_history(all_words: list, all_colors: list) -> list[dict[str, str, str]]:
    """ Get a history of all the inputs e.g. [{'red_letters': 'v', 'blue_letters': 't', 'yellow_letters': 'a'}, {'red_letters': '', 'blue_letters': 'oei', 'yellow_letters': ''}, {'red_letters': '', 'blue_letters': 'ltr', 'yellow_letters': ''}, {'red_letters': 'e', 'blue_letters': '', 'yellow_letters': ''}] 
    Args:
        all_words (list): all the input words
        all_wolors (list): all the input color transcriptions
    Returns:
        history (list[dict['red_letters': str, 'blue_letters': str, 'yellow_letters': str]]): all the inputs tranformed
    """
    colors_transposed = list(zip(*all_colors))

    history = []

    for i, colors_nth_letter in enumerate(colors_transposed):
        history_nth_letter = {"red_letters": '', "blue_letters": '', "yellow_letters": ''}

        for j, color in enumerate(colors_nth_letter):
            letter = all_words[j][i]

            if color == "r" and letter not in history_nth_letter["red_letters"]:
                history_nth_letter["red_letters"] = letter
            elif color == "b" and letter not in history_nth_letter["blue_letters"]:
                history_nth_letter["blue_letters"] += letter
            elif color == "y" and letter not in history_nth_letter["yellow_letters"]:
                history_nth_letter["yellow_letters"] += letter

        history.append(history_nth_letter)

    return history

def get_all_letters_for_color(history: list[dict[str, str, str]], color: str) -> str:
    """ Args:
        history (list[dict['red_letters': str, 'blue_letters': str, 'yellow_letters': str]]): all the inputs tranformed
        color (str): color to extract
    Returns:
        letters (str): all the letters for a certain color
    """
    letters = ''
    for row in history:
        letters += row[color]
    return letters

def remove_common_characters(string1: str, string2: str) -> str:
    """ Args:
        string1 (str): string to trim
        string2 (str): string with the duplicate letters to remove
    Returns:
        (str): string1 without the common characters from string2
    """
    return string1.translate(str.maketrans({e:None for e in set(string1).intersection(string2)}))

def get_all_yellow_letters(history: list[dict[str, str, str]]) -> str:
    """ Args:
        history (list[dict['red_letters': str, 'blue_letters': str, 'yellow_letters': str]]): all the inputs tranformed
    Returns:
        (str): all the yellow letters
    """
    return get_all_letters_for_color(history, 'yellow_letters')

def get_all_blue_letters(history: list[dict[str, str, str]], yellow_letters: str):
    """ Args:
        history (list[dict['red_letters': str, 'blue_letters': str, 'yellow_letters': str]]): all the inputs tranformed
    Returns:
        (str): all the blue letters
    """
    letters = get_all_letters_for_color(history, 'blue_letters')
    letters = remove_common_characters(letters, yellow_letters)
    return letters

def create_regex_pattern(history, blue_letters, yellow_letters):
    """ Get a regex pattern of all the inputs, e.g. '(?=v[^t][^ti]e)(?=.*a.*)(?=.*s.*)'
    Args:
        history (list[dict['red_letters': str, 'blue_letters': str, 'yellow_letters': str]]): all the inputs tranformed
        blue_letters (str): all the blue letters
        yellow_letters (str): all the yellow letters
    Returns:
        pattern (str): regex pattern of all the inputs
    """ 
    pattern = '(?='

    for row in history:
        if row["red_letters"]:
            pattern += row["red_letters"][0]
        else:
            pattern += '[^' + blue_letters + ''.join(row["yellow_letters"]) + ']'

    pattern += ')'

    for yellow in yellow_letters:
        pattern += '(?=.*' + yellow + '.*)'

    return pattern

def get_matching_words(dictionary_df, pattern):
    """ Get all the words in the dicitonary that matches a regex pattern
    Args:
        dictionary_df (pd.DataFrame): dictionary of words
        pattern (str): regex pattern
    Returns:
        (pd.DataFrame): df of all matching words
    """ 
    return dictionary_df.loc[dictionary_df["words"].str.match(pattern, case=False)]

def main():
    print("""
Sutom solver (https://sutom.nocle.fr/)

Instructions:
1. Fill in the 'Word' input, i.e. the tentative French word (e.g. 'vite')
2. Fill in the 'Colors' input, i.e. the result's color transcription (e.g. 'rbbr' where 'r' is red (right), 'b' is blue (wrong), 'y' is yellow (wrong spot))
    """)

    all_words = []
    all_colors = []

    while True:
        # New request
        word = input("""
Word: """)
        colors = input("Colors: ")
        check_inputs(word, colors)

        # Store results for each iteration
        all_words.append(word)
        all_colors.append(colors)

        # Loading appropriate dictionary
        dictionary_path = os.path.join(os.path.dirname(__file__), f"data/mots_{len(word)}.txt")
        dictionary_df = get_dictionary(dictionary_path)

        # Compile results into a list of dictionaries (history)
        history = create_history(all_words, all_colors)
        all_yellow_letters = get_all_letters_for_color(history, 'yellow_letters')
        all_blue_letters = get_all_blue_letters(history, all_yellow_letters)

        # Search for matching words in dictionary
        regex_pattern = create_regex_pattern(history, all_blue_letters, all_yellow_letters)
        matching_words = get_matching_words(dictionary_df, regex_pattern)
        print(f"{len(matching_words)} words left:")
        print(matching_words.to_string())

if __name__ == "__main__":
    main()
