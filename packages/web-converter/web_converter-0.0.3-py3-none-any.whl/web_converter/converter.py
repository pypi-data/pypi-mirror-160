def convert(string):
    splitted_string = string.split('\n')
    new_dict = {}
    for one in splitted_string:
        if one != '':
            splitted_one = one.split(': ')
            new_dict.update({splitted_one[0]: ''.join(splitted_one[1:])})
    return new_dict

def convert_cookies(string):
    splitted_string = string.split('; ')
    new_dict = {}
    for one in splitted_string:
        if one != '':
            splitted_one = one.split('=')
            new_dict.update({splitted_one[0]: ''.join(splitted_one[1:])})
    return new_dict