"""jc - JSON Convert utils"""
import sys
import re
import locale
import shutil
from datetime import datetime, timezone
from textwrap import TextWrapper
from functools import lru_cache
from typing import List, Iterable, Union, Optional


def _asciify(string: str) -> str:
    """
    Return a string downgraded from Unicode to ASCII with some simple
    conversions.
    """
    string = string.replace('©', '(c)')
    # the ascii() function adds single quotes around the string
    string = ascii(string)[1:-1]
    string = string.replace(r'\n', '\n')
    return string


def _safe_print(string: str, sep=' ', end='\n', file=sys.stdout, flush=False) -> None:
    """Output for both UTF-8 and ASCII encoding systems"""
    try:
        print(string, sep=sep, end=end, file=file, flush=flush)
    except UnicodeEncodeError:
        print(_asciify(string), sep=sep, end=end, file=file, flush=flush)


def _safe_pager(string: str) -> None:
    """Pager output for both UTF-8 and ASCII encoding systems"""
    from pydoc import pager
    try:
        pager(string)
    except UnicodeEncodeError:
        pager(_asciify(string))


def warning_message(message_lines: List[str]) -> None:
    """
    Prints warning message to `STDERR` for non-fatal issues. The first line
    is prepended with 'jc:  Warning - ' and subsequent lines are indented.
    Wraps text as needed based on the terminal width.

    Parameters:

        message:   (list) list of string lines

    Returns:

        None - just prints output to STDERR
    """
    # this is for backwards compatibility with existing custom parsers
    if isinstance(message_lines, str):
        message_lines = [message_lines]

    columns = shutil.get_terminal_size().columns

    first_wrapper = TextWrapper(width=columns, subsequent_indent=' ' * 15)
    next_wrapper = TextWrapper(width=columns, initial_indent=' ' * 15,
                               subsequent_indent=' ' * 19)

    first_line = message_lines.pop(0)
    first_str = f'jc:  Warning - {first_line}'
    first_str = first_wrapper.fill(first_str)
    _safe_print(first_str, file=sys.stderr)

    for line in message_lines:
        if line == '':
            continue
        message = next_wrapper.fill(line)
        _safe_print(message, file=sys.stderr)


def error_message(message_lines: List[str]) -> None:
    """
    Prints an error message to `STDERR` for fatal issues. The first line is
    prepended with 'jc:  Error - ' and subsequent lines are indented.
    Wraps text as needed based on the terminal width.

    Parameters:

        message:   (list) list of string lines

    Returns:

        None - just prints output to STDERR
    """
    columns = shutil.get_terminal_size().columns

    first_wrapper = TextWrapper(width=columns, subsequent_indent=' ' * 13)
    next_wrapper = TextWrapper(width=columns, initial_indent=' ' * 13,
                               subsequent_indent=' ' * 17)

    first_line = message_lines.pop(0)
    first_str = f'jc:  Error - {first_line}'
    first_str = first_wrapper.fill(first_str)
    _safe_print(first_str, file=sys.stderr)

    for line in message_lines:
        if line == '':
            continue
        message = next_wrapper.fill(line)
        _safe_print(message, file=sys.stderr)


def is_compatible(compatible: List) -> bool:
    """
    Returns True if the parser is compatible with the running OS platform.
    """
    platform_found = False

    for platform in compatible:
        if sys.platform.startswith(platform):
            platform_found = True
            break

    return platform_found


def compatibility(mod_name: str, compatible: List, quiet: bool = False) -> None:
    """
    Checks for the parser's compatibility with the running OS platform and
    prints a warning message to `STDERR` if not compatible and
    `quiet=False.`

    Parameters:

        mod_name:     (string) __name__ of the calling module

        compatible:   (list) sys.platform name(s) compatible with
                      the parser. compatible options:
                      linux, darwin, cygwin, win32, aix, freebsd

        quiet:        (bool) supress compatibility message if True

    Returns:

        None - just prints output to STDERR
    """
    if not quiet and not is_compatible(compatible):
        mod = mod_name.split('.')[-1]
        compat_list = ', '.join(compatible)
        warning_message([
            f'{mod} parser is not compatible with your OS ({sys.platform}).',
            f'Compatible platforms: {compat_list}'
        ])


def has_data(data: Union[str, bytes]) -> bool:
    """
    Checks if the string input contains data. If there are any
    non-whitespace characters then return `True`, else return `False`.

    For bytes, returns True if there is any data.

    Parameters:

        data:        (string, bytes) input to check whether it contains data

    Returns:

        Boolean      True if input string (data) contains non-whitespace
                     characters, otherwise False. For bytes data, returns
                     True if there is any data, otherwise False.
    """
    if isinstance(data, str):
        return bool(data and not data.isspace())

    return bool(data)


def convert_to_int(value: Union[str, float]) -> Optional[int]:
    """
    Converts string and float input to int. Strips all non-numeric
    characters from strings.

    Parameters:

        value:         (string/float) Input value

    Returns:

        integer/None   Integer if successful conversion, otherwise None
    """
    if isinstance(value, str):
        str_val = re.sub(r'[^0-9\-\.]', '', value)
        try:
            return int(str_val)
        except (ValueError, TypeError):
            try:
                return int(float(str_val))
            except (ValueError, TypeError):
                return None

    elif isinstance(value, (int, float)):
        return int(value)

    else:
        return None


def convert_to_float(value: Union[str, int]) -> Optional[float]:
    """
    Converts string and int input to float. Strips all non-numeric
    characters from strings.

    Parameters:

        value:         (string/integer) Input value

    Returns:

        float/None     Float if successful conversion, otherwise None
    """
    if isinstance(value, str):
        try:
            return float(re.sub(r'[^0-9\-\.]', '', value))
        except (ValueError, TypeError):
            return None

    elif isinstance(value, (int, float)):
        return float(value)

    else:
        return None


def convert_to_bool(value: Union[str, int, float]) -> bool:
    """
    Converts string, integer, or float input to boolean by checking
    for 'truthy' values.

    Parameters:

        value:          (string/integer/float) Input value

    Returns:

        True/False      False unless a 'truthy' number or string is found
                        ('y', 'yes', 'true', '1', 1, -1, etc.)
    """
    # if number, then bool it
    # if string, try to convert to float
    #   if float converts, then bool the result
    #   if float does not convert then look for truthy string and bool True
    #   else False
    truthy = ['y', 'yes', 'true', '*']

    if isinstance(value, (int, float)):
        return bool(value)

    if isinstance(value, str):
        try:
            test_value = convert_to_float(value)
            if test_value is not None:
                return bool(test_value)
        except Exception:
            pass

        if value:
            return value.lower() in truthy

    return False


def input_type_check(data: str) -> None:
    """Ensure input data is a string. Raises `TypeError` if not."""
    if not isinstance(data, str):
        raise TypeError("Input data must be a 'str' object.")


class timestamp:
    def __init__(self,
                 datetime_string: str,
                 format_hint: Optional[Iterable] = None
    ) -> None:
        """
        Input a datetime text string of several formats and convert to a
        naive or timezone-aware epoch timestamp in UTC.

        Parameters:

            datetime_string  (str):  a string representation of a
                datetime in several supported formats

            format_hint  (iterable):  an optional iterable of format ID
                integers to instruct the timestamp object to try those
                formats first in the order given. Other formats will be
                tried after the format hint list is exhausted. This can
                speed up timestamp conversion so several different formats
                don't have to be tried in brute-force fashion.

        Returns a timestamp object with the following attributes:

            string  (str):  the input datetime string

            format  (int | None):  the format rule that was used to decode
                the datetime string. None if conversion fails.

            naive  (int | None):  timestamp based on locally configured
                timezone. None if conversion fails.

            utc  (int | None):  aware timestamp only if UTC timezone
                detected in datetime string. None if conversion fails.
        """
        self.string = datetime_string

        if not format_hint:
            format_hint = tuple()
        else:
            format_hint = tuple(format_hint)

        dt = self._parse_dt(self.string, format_hint=format_hint)
        self.format = dt['format']
        self.naive = dt['timestamp_naive']
        self.utc = dt['timestamp_utc']

    def __repr__(self):
        return f'timestamp(string={self.string!r}, format={self.format}, naive={self.naive}, utc={self.utc})'

    @staticmethod
    @lru_cache(maxsize=512)
    def _parse_dt(dt_string, format_hint=None):
        """
        Input a datetime text string of several formats and convert to
        a naive or timezone-aware epoch timestamp in UTC.

        Parameters:

            dt_string:    (string) a string representation of a date-time
                          in several supported formats

            format_hint:  (list | tuple) a list of format ID int's that
                          should be tried first. This can increase
                          performance since the function will not need to
                          try many incorrect formats before finding the
                          correct one.

        Returns:

            Dictionary of the following format:

                {
                    # for debugging purposes. None if conversion fails
                    "format":               int,

                    # timestamp based on locally configured timezone.
                    # None if conversion fails.
                    "timestamp_naive":      int,

                    # aware timestamp only if UTC timezone detected.
                    # None if conversion fails.
                    "timestamp_utc":        int
                }

                The `format` integer denotes which date_time format
                conversion succeeded.

                The `timestamp_naive` integer is the converted date-time
                string to a naive epoch timestamp.

                The `timestamp_utc` integer is the converted date-time
                string to an aware epoch timestamp in the UTC timezone. If
                an aware conversion cannot be performed (e.g. the UTC
                timezone is not found in the date-time string), then this
                field will be None.

                If the conversion completely fails, all fields will be None.
        """
        data = dt_string or ''
        normalized_datetime = ''
        utc_tz = False
        dt = None
        dt_utc = None
        timestamp_naive = None
        timestamp_utc = None
        timestamp_obj = {
            'format': None,
            'timestamp_naive': None,
            'timestamp_utc': None
        }
        utc_tz = False

        # convert format_hint to a tuple so it is hashable (for lru_cache)
        if not format_hint:
            format_hint = tuple()
        else:
            format_hint = tuple(format_hint)

        # sometimes UTC is referenced as 'Coordinated Universal Time'. Convert to 'UTC'
        data = data.replace('Coordinated Universal Time', 'UTC')

        if 'UTC' in data:
            utc_tz = True
            if 'UTC+' in data or 'UTC-' in data:
                utc_tz = bool('UTC+0000' in data or 'UTC-0000' in data)

        elif '+0000' in data or '-0000' in data:
            utc_tz = True

        formats = [
            {'id': 1000, 'format': '%a %b %d %H:%M:%S %Y', 'locale': None},  # manual C locale format conversion: Tue Mar 23 16:12:11 2021 or Tue Mar 23 16:12:11 IST 2021
            {'id': 1100, 'format': '%a %b %d %H:%M:%S %Y %z', 'locale': None}, # git date output: Thu Mar 5 09:17:40 2020 -0800
            {'id': 1500, 'format': '%Y-%m-%d %H:%M', 'locale': None},  # en_US.UTF-8 local format (found in who cli output): 2021-03-23 00:14
            {'id': 1600, 'format': '%m/%d/%Y %I:%M %p', 'locale': None},  # Windows english format (found in dir cli output): 12/07/2019 02:09 AM
            {'id': 1700, 'format': '%m/%d/%Y, %I:%M:%S %p', 'locale': None},  # Windows english format wint non-UTC tz (found in systeminfo cli output): 3/22/2021, 1:15:51 PM (UTC-0600)
            {'id': 1705, 'format': '%m/%d/%Y, %I:%M:%S %p %Z', 'locale': None},  # Windows english format with UTC tz (found in systeminfo cli output): 3/22/2021, 1:15:51 PM (UTC)
            {'id': 1710, 'format': '%m/%d/%Y, %I:%M:%S %p UTC%z', 'locale': None},  # Windows english format with UTC tz (found in systeminfo cli output): 3/22/2021, 1:15:51 PM (UTC+0000)
            {'id': 2000, 'format': '%a %d %b %Y %I:%M:%S %p %Z', 'locale': None},  # en_US.UTF-8 local format (found in upower cli output): Tue 23 Mar 2021 04:12:11 PM UTC
            {'id': 3000, 'format': '%a %d %b %Y %I:%M:%S %p', 'locale': None},  # en_US.UTF-8 local format with non-UTC tz (found in upower cli output): Tue 23 Mar 2021 04:12:11 PM IST
            {'id': 4000, 'format': '%A %d %B %Y %I:%M:%S %p %Z', 'locale': None},  # European-style local format (found in upower cli output): Tuesday 01 October 2019 12:50:41 PM UTC
            {'id': 5000, 'format': '%A %d %B %Y %I:%M:%S %p', 'locale': None},  # European-style local format with non-UTC tz (found in upower cli output): Tuesday 01 October 2019 12:50:41 PM IST
            {'id': 6000, 'format': '%a %b %d %I:%M:%S %p %Z %Y', 'locale': None},  # en_US.UTF-8 format (found in date cli): Wed Mar 24 06:16:19 PM UTC 2021
            {'id': 7000, 'format': '%a %b %d %H:%M:%S %Z %Y', 'locale': None},  # C locale format (found in date cli): Wed Mar 24 11:11:30 UTC 2021
            {'id': 7100, 'format': '%b %d %H:%M:%S %Y', 'locale': None},  # C locale format (found in stat cli output - osx): # Mar 29 11:49:05 2021
            {'id': 7200, 'format': '%Y-%m-%d %H:%M:%S.%f %z', 'locale': None},  # C locale format (found in stat cli output - linux): 2019-08-13 18:13:43.555604315 -0400
            {'id': 7250, 'format': '%Y-%m-%d %H:%M:%S', 'locale': None},  # C locale format with non-UTC tz (found in modified vmstat cli output): # 2021-09-16 20:32:28 PDT
            {'id': 7255, 'format': '%Y-%m-%d %H:%M:%S %Z', 'locale': None},  # C locale format (found in modified vmstat cli output): # 2021-09-16 20:32:28 UTC
            {'id': 7300, 'format': '%a %Y-%m-%d %H:%M:%S %Z', 'locale': None},  # C locale format (found in timedatectl cli output): # Wed 2020-03-11 00:53:21 UTC
            # attempt locale changes last
            {'id': 8000, 'format': '%a %d %b %Y %H:%M:%S %Z', 'locale': ''},  # current locale format (found in upower cli output): # mar. 23 mars 2021 23:12:11 UTC
            {'id': 8100, 'format': '%a %d %b %Y %H:%M:%S', 'locale': ''},  # current locale format with non-UTC tz (found in upower cli output): # mar. 23 mars 2021 19:12:11 EDT
            {'id': 8200, 'format': '%A %d %B %Y, %H:%M:%S UTC%z', 'locale': ''},  # fr_FR.utf8 locale format (found in date cli output): vendredi 26 mars 2021, 13:26:46 (UTC+0000)
            {'id': 8300, 'format': '%A %d %B %Y, %H:%M:%S', 'locale': ''},  # fr_FR.utf8 locale format with non-UTC tz (found in date cli output): vendredi 26 mars 2021, 13:26:46 (UTC-0400)
            {'id': 9000, 'format': '%c', 'locale': ''}  # locally configured locale format conversion: Could be anything :) this is a last-gasp attempt
        ]

        # from https://www.timeanddate.com/time/zones/
        # only removed UTC timezone and added known non-UTC offsets
        tz_abbr = [
            'A', 'ACDT', 'ACST', 'ACT', 'ACWST', 'ADT', 'AEDT', 'AEST', 'AET', 'AFT', 'AKDT',
            'AKST', 'ALMT', 'AMST', 'AMT', 'ANAST', 'ANAT', 'AQTT', 'ART', 'AST', 'AT', 'AWDT',
            'AWST', 'AZOST', 'AZOT', 'AZST', 'AZT', 'AoE', 'B', 'BNT', 'BOT', 'BRST', 'BRT', 'BST',
            'BTT', 'C', 'CAST', 'CAT', 'CCT', 'CDT', 'CEST', 'CET', 'CHADT', 'CHAST', 'CHOST',
            'CHOT', 'CHUT', 'CIDST', 'CIST', 'CKT', 'CLST', 'CLT', 'COT', 'CST', 'CT', 'CVT', 'CXT',
            'ChST', 'D', 'DAVT', 'DDUT', 'E', 'EASST', 'EAST', 'EAT', 'ECT', 'EDT', 'EEST', 'EET',
            'EGST', 'EGT', 'EST', 'ET', 'F', 'FET', 'FJST', 'FJT', 'FKST', 'FKT', 'FNT', 'G',
            'GALT', 'GAMT', 'GET', 'GFT', 'GILT', 'GMT', 'GST', 'GYT', 'H', 'HDT', 'HKT', 'HOVST',
            'HOVT', 'HST', 'I', 'ICT', 'IDT', 'IOT', 'IRDT', 'IRKST', 'IRKT', 'IRST', 'IST', 'JST',
            'K', 'KGT', 'KOST', 'KRAST', 'KRAT', 'KST', 'KUYT', 'L', 'LHDT', 'LHST', 'LINT', 'M',
            'MAGST', 'MAGT', 'MART', 'MAWT', 'MDT', 'MHT', 'MMT', 'MSD', 'MSK', 'MST', 'MT', 'MUT',
            'MVT', 'MYT', 'N', 'NCT', 'NDT', 'NFDT', 'NFT', 'NOVST', 'NOVT', 'NPT', 'NRT', 'NST',
            'NUT', 'NZDT', 'NZST', 'O', 'OMSST', 'OMST', 'ORAT', 'P', 'PDT', 'PET', 'PETST', 'PETT',
            'PGT', 'PHOT', 'PHT', 'PKT', 'PMDT', 'PMST', 'PONT', 'PST', 'PT', 'PWT', 'PYST', 'PYT',
            'Q', 'QYZT', 'R', 'RET', 'ROTT', 'S', 'SAKT', 'SAMT', 'SAST', 'SBT', 'SCT', 'SGT',
            'SRET', 'SRT', 'SST', 'SYOT', 'T', 'TAHT', 'TFT', 'TJT', 'TKT', 'TLT', 'TMT', 'TOST',
            'TOT', 'TRT', 'TVT', 'U', 'ULAST', 'ULAT', 'UYST', 'UYT', 'UZT', 'V', 'VET', 'VLAST',
            'VLAT', 'VOST', 'VUT', 'W', 'WAKT', 'WARST', 'WAST', 'WAT', 'WEST', 'WET', 'WFT',
            'WGST', 'WGT', 'WIB', 'WIT', 'WITA', 'WST', 'WT', 'X', 'Y', 'YAKST', 'YAKT', 'YAPT',
            'YEKST', 'YEKT', 'Z', 'UTC-1200', 'UTC-1100', 'UTC-1000', 'UTC-0930', 'UTC-0900',
            'UTC-0800', 'UTC-0700', 'UTC-0600', 'UTC-0500', 'UTC-0400', 'UTC-0300', 'UTC-0230',
            'UTC-0200', 'UTC-0100', 'UTC+0100', 'UTC+0200', 'UTC+0300', 'UTC+0400', 'UTC+0430',
            'UTC+0500', 'UTC+0530', 'UTC+0545', 'UTC+0600', 'UTC+0630', 'UTC+0700', 'UTC+0800',
            'UTC+0845', 'UTC+0900', 'UTC+1000', 'UTC+1030', 'UTC+1100', 'UTC+1200', 'UTC+1300',
            'UTC+1345', 'UTC+1400'
        ]

        # normalize the timezone by taking out any timezone reference, except UTC
        cleandata = data.replace('(', '').replace(')', '')
        normalized_datetime_list = []
        for term in cleandata.split():
            if term not in tz_abbr:
                normalized_datetime_list.append(term)

        normalized_datetime = ' '.join(normalized_datetime_list)

        # normalize further by converting any greater-than 6-digit subsecond to 6-digits
        p = re.compile(r'(\W\d\d:\d\d:\d\d\.\d{6})\d+\W')
        normalized_datetime = p.sub(r'\g<1> ', normalized_datetime)

        # try format hints first, then fall back to brute-force method
        hint_obj_list = []
        for fmt_id in format_hint:
            for fmt in formats:
                if fmt_id == fmt['id']:
                    hint_obj_list.append(fmt)

        remaining_formats = [fmt for fmt in formats if not fmt['id'] in format_hint]
        optimized_formats = hint_obj_list + remaining_formats

        for fmt in optimized_formats:
            try:
                locale.setlocale(locale.LC_TIME, fmt['locale'])
                dt = datetime.strptime(normalized_datetime, fmt['format'])
                timestamp_naive = int(dt.replace(tzinfo=None).timestamp())
                timestamp_obj['format'] = fmt['id']
                locale.setlocale(locale.LC_TIME, None)
                break
            except Exception:
                locale.setlocale(locale.LC_TIME, None)
                continue

        if dt and utc_tz:
            dt_utc = dt.replace(tzinfo=timezone.utc)
            timestamp_utc = int(dt_utc.timestamp())

        if timestamp_naive:
            timestamp_obj['timestamp_naive'] = timestamp_naive
            timestamp_obj['timestamp_utc'] = timestamp_utc

        return timestamp_obj
