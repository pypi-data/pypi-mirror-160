import re

def to_nth_str(i):
    """
    Converts an integer to a string like '1st', '2nd', '3rd', _etc_

    Parameters
    ----------
    i : int
        The integer to convert

    Returns
    -------
    str

    Examples
    --------

    Basic Usage:

    >>>
    >>> to_nth_str(1)  # -> "1st"
    >>> to_nth_str(2)  # -> "2nd"
    >>>
    >>> # Not sure what context this will be useful in
    >>> from_nth_str(-66) # -> "-66th"
    >>>
    """
    if i == 1:
        return "1st"
    elif i == 2:
        return "2nd"
    elif i == 3:
        return "3rd"
    else:
        return f"{i}th"

def from_nth_str(s, ignore_case=True):
    """
    Converts a string like '1st', '2nd'... '4th', _etc_ to an integer

    To be specific, the exact pattern searched is:

        \b(-?[0-9]+)(st|nd|rd|th)\b

    Parameters
    ----------
    s : str
        The string to convert
    ignore_case : bool, optional
        Converts ``s`` to lowercase before processing

    Returns
    -------
    str, optional
        If successful, returns the converted string, otherwise returns None

    Examples
    --------

    Basic Usage:

    >>>
    >>> from_nth_str("1st")  # -> 1
    >>> from_nth_str("2nd")  # -> 2
    >>>
    >>> # Not sure what context this will be useful in
    >>> from_nth_str("-5th") # -> -5
    >>>

    On Failure:

    >>>
    >>> from_nth_str("1sttheworst") # -> None
    >>> from_nth_str("2ndthebest")  # -> None
    >>> from_nth_str("3rDtHePrInCeSsWiThThEhAiRyChEsT") # -> None
    >>>
    """
    s = s.lower() if ignore_case else s
    try:
        pttn = r"\b(-?[0-9]+)(st|nd|rd|th)\b"
        repl = r"\1"
        return int(re.sub(pttn, repl, s))
    except ValueError:
        return None
