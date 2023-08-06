"""jc - JSON Convert `id` command output parser

Usage (cli):

    $ id | jc --id

    or

    $ jc id

Usage (module):

    import jc
    result = jc.parse('id', id_command_output)

Schema:

    {
      "uid": {
        "id":       integer,
        "name":     string
      },
      "gid": {
        "id":       integer,
        "name":     string
      },
      "groups": [
        {
          "id":     integer,
          "name":   string
        },
        {
          "id":     integer,
          "name":   string
        }
      ],
      "context": {
        "user":     string,
        "role":     string,
        "type":     string,
        "level":    string
      }
    }

Examples:

    $ id | jc --id -p
    {
      "uid": {
        "id": 1000,
        "name": "joeuser"
      },
      "gid": {
        "id": 1000,
        "name": "joeuser"
      },
      "groups": [
        {
          "id": 1000,
          "name": "joeuser"
        },
        {
          "id": 10,
          "name": "wheel"
        }
      ],
      "context": {
        "user": "unconfined_u",
        "role": "unconfined_r",
        "type": "unconfined_t",
        "level": "s0-s0:c0.c1023"
      }
    }

    $ id | jc --id -p -r
    {
      "uid": {
        "id": "1000",
        "name": "joeuser"
      },
      "gid": {
        "id": "1000",
        "name": "joeuser"
      },
      "groups": [
        {
          "id": "1000",
          "name": "joeuser"
        },
        {
          "id": "10",
          "name": "wheel"
        }
      ],
      "context": {
        "user": "unconfined_u",
        "role": "unconfined_r",
        "type": "unconfined_t",
        "level": "s0-s0:c0.c1023"
      }
    }
"""
import jc.utils


class info():
    """Provides parser metadata (version, author, etc.)"""
    version = '1.5'
    description = '`id` command parser'
    author = 'Kelly Brazil'
    author_email = 'kellyjonbrazil@gmail.com'
    compatible = ['linux', 'darwin', 'aix', 'freebsd']
    magic_commands = ['id']


__version__ = info.version


def _process(proc_data):
    """
    Final processing to conform to the schema.

    Parameters:

        proc_data:   (Dictionary) raw structured data to process

    Returns:

        Dictionary. Structured data to conform to the schema.
    """
    if 'uid' in proc_data:
        if 'id' in proc_data['uid']:
            proc_data['uid']['id'] = jc.utils.convert_to_int(proc_data['uid']['id'])

    if 'gid' in proc_data:
        if 'id' in proc_data['gid']:
            proc_data['gid']['id'] = jc.utils.convert_to_int(proc_data['gid']['id'])

    if 'groups' in proc_data:
        for group in proc_data['groups']:
            if 'id' in group:
                group['id'] = jc.utils.convert_to_int(group['id'])

    return proc_data


def _get_item(my_list, index, default=None):
      if index < len(my_list):
        return my_list[index]

      return default


def parse(data, raw=False, quiet=False):
    """
    Main text parsing function

    Parameters:

        data:        (string)  text data to parse
        raw:         (boolean) unprocessed output if True
        quiet:       (boolean) suppress warning messages if True

    Returns:

        Dictionary. Raw or processed structured data.
    """
    jc.utils.compatibility(__name__, info.compatible, quiet)
    jc.utils.input_type_check(data)

    raw_output = {}

    # Clear any blank lines
    cleandata = list(filter(None, data.split()))

    if jc.utils.has_data(data):

        for section in cleandata:
            if section.startswith('uid'):
                uid_parsed = section.replace('(', '=').replace(')', '=')
                uid_parsed = uid_parsed.split('=')
                raw_output['uid'] = {}
                raw_output['uid']['id'] = uid_parsed[1]
                raw_output['uid']['name'] = _get_item(uid_parsed, 2)

            if section.startswith('gid'):
                gid_parsed = section.replace('(', '=').replace(')', '=')
                gid_parsed = gid_parsed.split('=')
                raw_output['gid'] = {}
                raw_output['gid']['id'] = gid_parsed[1]
                raw_output['gid']['name'] = _get_item(gid_parsed, 2)

            if section.startswith('groups'):
                groups_parsed = section.replace('(', '=').replace(')', '=')
                groups_parsed = groups_parsed.replace('groups=', '')
                groups_parsed = groups_parsed.split(',')
                raw_output['groups'] = []

                for group in groups_parsed:
                    group_dict = {}
                    grp_parsed = group.split('=')
                    group_dict['id'] = grp_parsed[0]
                    group_dict['name'] = _get_item(grp_parsed, 1)
                    raw_output['groups'].append(group_dict)

            if section.startswith('context'):
                context_parsed = section.replace('context=', '')
                context_parsed = context_parsed.split(':', maxsplit=3)
                raw_output['context'] = {}
                raw_output['context']['user'] = context_parsed[0]
                raw_output['context']['role'] = context_parsed[1]
                raw_output['context']['type'] = context_parsed[2]
                raw_output['context']['level'] = context_parsed[3]

    if raw:
        return raw_output
    else:
        return _process(raw_output)
