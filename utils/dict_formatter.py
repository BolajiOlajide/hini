import json


def dict_to_binary(the_dict):
    return ' '.join(
        format(ord(letter), 'b')
        for letter in json.dumps(the_dict)
    )
