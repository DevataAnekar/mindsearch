from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def get(model_answer,given_answer):
    matching = fuzz.ratio(model_answer.lower(),given_answer.lower())
    if matching > 60:
        return "Correct"
    else:
        return "Incorrect"
