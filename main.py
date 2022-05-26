from black import out
import pandas as pd

def check_inputs(tested_inputs):
    for tested_input in tested_inputs:
        if (len(tested_input) < 4 or len(tested_input) > 12):
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
    # New request
    input_ = input("Fill in the input, replace missing letters by *, e.g. t*rtu*: ")
    output = input("Fill in the result code (good g, misplaced m, wrong g), e.g. gwgggm: ")
    check_inputs([input_, output])

    # Store results for each iteration
    inputs.append(input_)
    outputs.append(output)

    # input_ = "voiture"
    # inputs = ["voiture", "voilage", "voitage", "voivage"]
    # outputs = ["ggwgwwg", "ggwmggg", "ggwgggg", "ggwmggg"]

    # Loading appropriate dictionary
    words_df = get_words(f"data/mots_{len(input_)}.txt")
    
    # Compile results into a list of dictionaries (history)
    history = get_history(inputs, outputs)
    wrongs = get_all_letters_in_group(history, "wrong")
    misplaced = get_all_letters_in_group(history, "misplaced")

    # Search for matching words in dictionary
    regex_pattern = create_regex_pattern(history, wrongs, misplaced)
    words_left_df = get_words_matching_pattern(words_df, regex_pattern)
    print(words_left_df)

    # Recursion for new requests
    main()

# Initialization of request results
inputs = []
outputs = []
words_left_df = pd.DataFrame()
main()
