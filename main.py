from black import out
import pandas as pd

def check_input(inputs):
    last_input = inputs[-1]
    last_input_length = len(last_input)

    if (last_input_length < 4 or last_input_length > 12):
        raise Exception("This program only handles inputs from 4 to 12 letters")

def get_words(filename):
    words_df = pd.read_csv(filename, sep=" ", header=None)
    words_df.columns = ["words"]
    return words_df

def get_words_matching_pattern(words_df, pattern):
    return words_df.loc[words_df["words"].str.match(pattern, case=False)]

def df_column_to_list(df_column):
    return list(filter(None, df_column.tolist()))

def get_history(inputs, outputs):
    outputs_transposed = list(zip(*outputs))

    history = []

    for i, nth_character in enumerate(outputs_transposed):
        output_summary = {"good": '', "wrong": '', "misplaced": ''}

        for j, character in enumerate(nth_character):
            letter = inputs[j][i]

            if character == 'g' and letter not in output_summary["good"]:
                output_summary["good"] = letter
            elif character == 'w' and letter not in output_summary["wrong"]:
                output_summary["wrong"] += letter
            elif character == 'm' and letter not in output_summary["misplaced"]:
                output_summary["misplaced"] += letter

        history.append(output_summary)
    
    return history

def get_all_letters_in_group(history, group):
    letters = ''
    for row in history:
        letters += row[group]
    return letters

def create_regex_pattern(history, wrongs, misplaced):
    pattern = '(?='

    for row in history:
        if row["good"]:
            pattern += row["good"][0]
        else:
            pattern += '[^' + wrongs + "".join(row["misplaced"]) + ']'
    
    pattern += ')'

    for misplaced_letter in misplaced:
        pattern += '(?=.*' + misplaced_letter + '.*)'

    return pattern

def main():
    # input_ = input("Fill in the input, replace missing letters by *, e.g. t*rtu*: ")
    input_ = "voiture"
    inputs = ["voiture", "voilage", "voitage", "voivage"]
    
    check_input(inputs)
    words_df = get_words(f"data/mots_{len(input_)}.txt")
    print(words_df)
    
    # output = input("Fill in the result code (good g, misplaced m, wrong g), e.g. gwgggm: ")
    outputs = ["ggwgwwg", "ggwmggg", "ggwgggg", "ggwmggg"]

    history = get_history(inputs, outputs)
    wrongs = get_all_letters_in_group(history, "wrong")
    misplaced = get_all_letters_in_group(history, "misplaced")
    regex_pattern = create_regex_pattern(history, wrongs, misplaced)
    print(regex_pattern)

    words_left_df = get_words_matching_pattern(words_df, regex_pattern)
    print(words_left_df)
main()
