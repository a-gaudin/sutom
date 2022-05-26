import pandas as pd

def check_input(inputs):
    last_input = inputs[-1]
    last_input_length = len(last_input)

    if (not last_input[0].isalpha()):
        raise Exception("First character should be a letter")

    if (last_input_length < 4 or last_input_length > 12):
        raise Exception("This program only handles inputs from 4 to 12 letters")

def get_words(filename):
    words_df = pd.read_csv(filename, sep=" ", header=None)
    words_df.columns = ["words"]
    return words_df

def get_words_matching_pattern(words_df, pattern):
    return words_df.loc[words_df["words"].str.match(pattern, case=False)]

def create_regex_pattern(inputs, outputs):
    pattern = '(?='
    wrong_letters = []
    misplaced_letters = []

    for i in range(len(output)):
        if output[i] == 'g':
            pattern.append(input[i])
        elif output[i] == 'm':
            pattern.append('[^' + input[i] + ']')
            misplaced_letters.append(input[i])
        elif output[i] == 'w':
            wrong_letters.append(input[i])

    for misplaced_letter in misplaced_letters:
        pattern.append('(?=.*' + misplaced_letter + '.*)')

    return pattern

def main():
    data = {'words':['slope', 'stove', 'store', 'stone', 'stena']}
    words_df = pd.DataFrame(data)

    regex_pattern = '(?=s[^wy][a-z][a-z]e)(?=.*r.*)(?=.*t.*)'

    words_left_df = get_words_matching_pattern(words_df, regex_pattern)
    print(words_left_df)

    # input_ = input("Fill in the input, replace missing letters by *, e.g. t*rtu*: ")
    # inputs = [input_]
    #
    # check_input(inputs)
    # words_df = get_words(f"data/mots_{len(input_)}.txt")
    # print(words_df)
    #
    # output = input("Fill in the result code (good g, misplaced m, wrong g), e.g. gwgggm: ")
    # outputs = [output]

main()
