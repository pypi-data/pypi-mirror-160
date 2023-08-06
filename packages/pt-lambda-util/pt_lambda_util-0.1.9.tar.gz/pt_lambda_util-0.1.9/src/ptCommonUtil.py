def convert_key_value_string_to_dict(key_value_string, key_value_sep="=", block_sep=";"):
    res = []
    for sub in key_value_string.split(block_sep):
        if key_value_sep in sub:
            res.append(map(str.strip, sub.split(key_value_sep, 1)))
    res = dict(res)
    return res