def html_entities_encode(str_to_convert):
    result = ""

    # Print every character's code returned by ord() function in HTML entity format
    for character in str_to_convert:
        result += f"&#{ord(character)};"

    return result
