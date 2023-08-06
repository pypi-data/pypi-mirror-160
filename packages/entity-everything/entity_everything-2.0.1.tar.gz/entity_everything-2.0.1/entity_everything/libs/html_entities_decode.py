import re


def html_entities_decode(str_to_convert: str):
    result = str_to_convert

    found_groups = re.findall(r"&#(\d+);", str_to_convert)
    for group in found_groups:
        result = result.replace(f"&#{group};", chr(int(group)))

    return result
