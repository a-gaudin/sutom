import os
import pandas as pd

def check_inputs(word, colors):
    if len(word) != len(colors):
        raise ValueError("Word and Colors should be the same length") 

    if (len(word) < 4 or len(word) > 12):
        raise ValueError("This program only handles words from 4 to 12 letters")

def get_dictionary(filename):
    """ Get a dictionary for the word's length. Each dictionary has 4096 words sorted by popularity
    Returns a single-column dataframe """
    dictionary_df = pd.read_csv(filename, sep=" ", header=None)
    dictionary_df.columns = ["words"]
    return dictionary_df

def create_history(all_words, all_colors):
    """ Returns a list of dictionaries, e.g.:
    [{'reds': 'v', 'blues': 't', 'yellows': 'a'}, {'reds': '', 'blues': 'oei', 'yellows': ''}, {'reds': '', 'blues': 'ltr', 'yellows': ''}, {'reds': 'e', 'blues': '', 'yellows': ''}] """
    colors_transposed = list(zip(*all_colors))

    history = []

    for i, colors_nth_letter in enumerate(colors_transposed):
        history_nth_letter = {"reds": '', "blues": '', "yellows": ''}

        for j, color in enumerate(colors_nth_letter):
            letter = all_words[j][i]

            if color == "r" and letter not in history_nth_letter["reds"]:
                history_nth_letter["reds"] = letter
            elif color == "b" and letter not in history_nth_letter["blues"]:
                history_nth_letter["blues"] += letter
            elif color == "y" and letter not in history_nth_letter["yellows"]:
                history_nth_letter["yellows"] += letter

        history.append(history_nth_letter)

    return history

def get_letters_in_category(history, category):
    letters = ''
    for row in history:
        letters += row[category]
    return letters

def create_regex_pattern(history, wrongs, yellows):
    """ Returns a regex pattern, e.g. '(?=v[^t][^ti]e)(?=.*a.*)(?=.*s.*)'
    It translates as: 1st letter is 'v', 2nd is not 't', 3rd is not 't' or 'i', 4 th is 'e'. 'a' and 's' should be found somewhere """
    pattern = '(?='

    for row in history:
        if row["reds"]:
            pattern += row["reds"][0]
        else:
            pattern += '[^' + wrongs + ''.join(row["yellows"]) + ']'

    pattern += ')'

    for yellow in yellows:
        pattern += '(?=.*' + yellow + '.*)'

    return pattern

def get_matching_words(dictionary_df, pattern):
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
        word = input("Word: ")
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
        wrongs = get_letters_in_category(history, "blues")
        yellows = get_letters_in_category(history, "yellows")

        # Search for matching words in dictionary
        regex_pattern = create_regex_pattern(history, wrongs, yellows)
        matching_words = get_matching_words(dictionary_df, regex_pattern)
        print(f"{len(matching_words)} words left:")
        print(matching_words.to_string())

if __name__ == "__main__":
    main()
