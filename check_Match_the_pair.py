


##import re
##
##yourString = "ajay123"
##print(re.sub('[\W\d_]+', '', yourString))


def get(model_answer,given_answer):
    sfiltered = ''
    for char in given_answer.lower():
        if((ord(char) >= 97 and ord(char) <= 122) or (ord(char) >= 65 and ord(char) <= 90) or (ord(char) >= 48 and ord(char) <= 57)):
            sfiltered += char
    if sfiltered == model_answer:
        return "Correct"
    else:
        return "Incorrect"



