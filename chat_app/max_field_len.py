def max_field_len(fields_map):
    max_field = 0
    for key in fields_map:
        if len(key) > max_field:
            max_field = len(key)
    return max_field