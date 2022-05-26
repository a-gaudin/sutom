from black import out
import pandas as pd

def check_inputs(input_, output):
    if len(input_) != len(output):
        raise ValueError("Inputs and Outputs should be the same length") 
    
    if (len(input_) < 4 or len(input_) > 12):
        raise ValueError("This program only handles inputs from 4 to 12 letters")
            
def get_dictionary(filename):
    dictionary_df = pd.read_csv(filename, sep=" ", header=None)
    dictionary_df.columns = ["words"]
    return dictionary_df

def get_matching_words(dictionary_df, pattern):
    return dictionary_df.loc[dictionary_df["words"].str.match(pattern, case=False)]

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

def get_letters_in_category(history, category):
    letters = ''
    for row in history:
        letters += row[category]
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
    check_inputs(input_, output)

    # Store results for each iteration
    inputs.append(input_)
    outputs.append(output)

    # Loading appropriate dictionary
    dictionary_df = get_dictionary(f"data/mots_{len(input_)}.txt")
    
    # Compile results into a list of dictionaries (history)
    history = get_history(inputs, outputs)
    wrongs = get_letters_in_category(history, "wrong")
    misplaced = get_letters_in_category(history, "misplaced")

    # Search for matching words in dictionary
    regex_pattern = create_regex_pattern(history, wrongs, misplaced)
    matching_words = get_matching_words(dictionary_df, regex_pattern)
    print(f"{len(matching_words)} words left:")
    print(matching_words.to_string())

    # Recursion for new requests
    main()

# Initialization of request results
inputs = []
outputs = []
matching_words = pd.DataFrame()
main()
