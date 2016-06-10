import re


def get_paired_regex(text, start_regex, end_regex):
    """Return the index of where the paired end_regex begins.

    We assume that the text starts after the initial 'start_regex'.
    """
    regex = re.compile("(" + start_regex + ")|(" + end_regex + ")")
    matches = re.finditer(regex, text)

    counter = 1

    for match in matches:
        arguments = match.groups()
        is_start_match = arguments[0] is not None  # Is this a start or end match?

        if is_start_match:
            counter += 1
        else:
            counter -= 1

            if counter == 0:
                return match.start(), match.start() + len(match.group(0))
    return None
