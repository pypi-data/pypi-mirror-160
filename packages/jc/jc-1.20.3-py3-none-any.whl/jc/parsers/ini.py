"""jc - JSON Convert `INI` file parser

Parses standard `INI` files and files containing simple key/value pairs.

- Delimiter can be `=` or `:`. Missing values are supported.
- Comment prefix can be `#` or `;`. Comments must be on their own line.
- If duplicate keys are found, only the last value will be used.

> Note: Values starting and ending with double or single quotation marks
> will have the marks removed. If you would like to keep the quotation
> marks, use the `-r` command-line argument or the `raw=True` argument in
> `parse()`.

Usage (cli):

    $ cat foo.ini | jc --ini

Usage (module):

    import jc
    result = jc.parse('ini', ini_file_output)

Schema:

ini or key/value document converted to a dictionary - see the configparser
standard library documentation for more details.

    {
      "key1":       string,
      "key2":       string
    }

Examples:

    $ cat example.ini
    [DEFAULT]
    ServerAliveInterval = 45
    Compression = yes
    CompressionLevel = 9
    ForwardX11 = yes

    [bitbucket.org]
    User = hg

    [topsecret.server.com]
    Port = 50022
    ForwardX11 = no

    $ cat example.ini | jc --ini -p
    {
      "bitbucket.org": {
        "serveraliveinterval": "45",
        "compression": "yes",
        "compressionlevel": "9",
        "forwardx11": "yes",
        "user": "hg"
      },
      "topsecret.server.com": {
        "serveraliveinterval": "45",
        "compression": "yes",
        "compressionlevel": "9",
        "forwardx11": "no",
        "port": "50022"
      }
    }
"""
import jc.utils
import configparser


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.7'
    description = 'INI file parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    details = 'Using configparser from the standard library'
    compatible = ['linux', 'darwin', 'cygwin', 'win32', 'aix', 'freebsd']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary representing an ini or simple key/value pair document.
    """
    # remove quotation marks from beginning and end of values
    for heading in proc_data:
        # standard ini files with headers
        if isinstance(proc_data[heading], dict):
            for key, value in proc_data[heading].items():
                if value is not None and value.startswith('"') and value.endswith('"'):
                    proc_data[heading][key] = value.lstrip('"').rstrip('"')

                elif value is not None and value.startswith("'") and value.endswith("'"):
                    proc_data[heading][key] = value.lstrip("'").rstrip("'")

                elif value is None:
                    proc_data[heading][key] = ''

        # simple key/value files with no headers
        else:
            if proc_data[heading] is not None and proc_data[heading].startswith('"') and proc_data[heading].endswith('"'):
                proc_data[heading] = proc_data[heading].lstrip('"').rstrip('"')

            elif proc_data[heading] is not None and proc_data[heading].startswith("'") and proc_data[heading].endswith("'"):
                proc_data[heading] = proc_data[heading].lstrip("'").rstrip("'")

            elif proc_data[heading] is None:
                proc_data[heading] = ''

    return proc_data


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary representing the ini file
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    if jc.utils.has_data(data):

        ini = configparser.ConfigParser(allow_no_value=True,
                                        interpolation=None,
                                        strict=False)
        try:
            ini.read_string(data)
            raw_output = {s: dict(ini.items(s)) for s in ini.sections()}

        except configparser.MissingSectionHeaderError:
            data = '[data]\n' + data
            ini.read_string(data)
            output_dict = {s: dict(ini.items(s)) for s in ini.sections()}
            for key, value in output_dict['data'].items():
                raw_output[key] = value

    if raw:
        return raw_output
    else:
        return _process(raw_output)
