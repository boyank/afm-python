from math import isnan
from ._utils import get_random_int


def generate_afm(
    force_first_digit: int = None,
    pre99: bool = False,
    individual: bool = False,
    legal_entity: bool = False,
    repeat_tolerance: int = None,
    valid: bool = True
) -> str:
    """Generates an TIN/AFM number based on object parameters.

    Parameters
    ----------
    force_first_digit : int, optional
        If specified, overrides all pre99, legal_entity and individual (default is None)
    pre99 : bool, optional
        For TIN/AFM before 1/1/1999 (starts with 0),
        (if True, overrides both legal_entity and individual)
        (default is False)
    individual : bool, optional
        Natural persons, (starts with 1-4) (default is False)
    legal_entity : bool, optional
        Legal entities (starts 7-9) (default is False)
    repeat_tolerance : int, optional
        Number for max repeat tolerance
        (0 for no repeats, unspecified for no check)
        (default is None)
    valid : bool, optional
        Generate valid or invalid TIN/AFM (default is True)

    Returns
    -------
    str
        A valid or invalid 9 digit TIN/AFM number
    """
    min_digit = 7 if legal_entity else 1
    max_digit = 4 if individual else 9
    repeat_of = None if not repeat_tolerance and repeat_tolerance != 0 else repeat_tolerance
    digit = force_first_digit if force_first_digit is not None and not isnan(force_first_digit) \
                              else (0 if pre99 else get_random_int(min_digit, max_digit))
    last_gen_digit = digit
    repeats = 0
    body = str(digit)
    weighted_sum = digit * 0x100

    for i in range(7, 0, -1):
        digit = get_random_int(0, 9, 
            last_gen_digit if repeat_of is not None and repeats >= repeat_of else None)
        body += str(digit)
        weighted_sum += digit << i
        if digit == last_gen_digit:
            repeats += 1
        else:
            repeats = 0
        last_gen_digit = digit
    
    validator = weighted_sum % 11
    d9_valid = validator % 10
    d9 = d9_valid if valid else get_random_int(0, 9, d9_valid)

    return body + str(d9)

def generate_valid_afm(**args) -> str:
    """Generates a valid TIN/AFM number based on object parameters.

    Parameters
    ----------
    force_first_digit : int, optional
        If specified, overrides all pre99, legal_entity and individual (default is None)
    pre99 : bool, optional
        For TIN/AFM before 1/1/1999 (starts with 0),
        (if True, overrides both legal_entity and individual)
        (default is False)
    individual : bool, optional
        Natural persons, (starts with 1-4) (default is False)
    legal_entity : bool, optional
        Legal entities (starts 7-9) (default is False)
    repeat_tolerance : int, optional
        Number for max repeat tolerance
        (0 for no repeats, unspecified for no check)
        (default is None)

    Returns
    -------
    str
        A valid 9 digit TIN/AFM number
    """
    args['valid'] = True
    return generate_afm(**args)

def generate_invalid_afm(**args) -> str:
    """Generates an invalid TIN/AFM number based on object parameters.

    Parameters
    ----------
    force_first_digit : int, optional
        If specified, overrides all pre99, legal_entity and individual (default is None)
    pre99 : bool, optional
        For TIN/AFM before 1/1/1999 (starts with 0),
        (if True, overrides both legal_entity and individual)
        (default is False)
    individual : bool, optional
        Natural persons, (starts with 1-4) (default is False)
    legal_entity : bool, optional
        Legal entities (starts 7-9) (default is False)
    repeat_tolerance : int, optional
        Number for max repeat tolerance
        (0 for no repeats, unspecified for no check)
        (default is None)

    Returns
    -------
    str
        An invalid 9 digit TIN/AFM number
    """
    args['valid'] = False
    return generate_afm(**args)
