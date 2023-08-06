import json
import os
import sys
from typing import List

from democritus_file_system import atomic_write, file_exists, file_read

from .json_data_temp_utils import json_read_first_arg_string


def json_files(directory_path: str) -> List[str]:
    """Find all json files in the given directory_path."""
    from democritus_file_system import directory_file_names_matching

    pattern = '*.json'
    files = directory_file_names_matching(directory_path, pattern)

    return files


def json_read(json_string: str):
    import re

    # TODO: do more here to make sure the path looks like a file path
    if file_exists(json_string):
        json_string = file_read(json_string)

    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        if 'property name enclosed in double quotes' in str(e):
            print('> Found a single quote in the json... I\'ll try replacing all single quotes with double quotes')
            try:
                unescaped_single_quote_pattern = r"(?<!\\)'"
                json_string = re.sub(unescaped_single_quote_pattern, '"', json_string)
                return json.loads(json_string)
            except json.JSONDecodeError as second_error:
                print(
                    '! Even replacing all of the single quotes with double quotes did not work:\n\t{}'.format(
                        second_error
                    )
                )
                raise e
        else:
            raise e


def json_write(file_path, json_content, **kwargs):
    """Write the json_content to the file_path."""
    with atomic_write(file_path) as f:
        json.dump(json_content, f, **kwargs)

    # # TODO: would like to return a bool from this function (like the file_write function)
    # # TODO: need to make the x_write functions consistent across different types (e.g. the yaml_write function returns a string while this function actually writes content)


@json_read_first_arg_string
def json_prettify(json_object):
    """."""
    pretty_json = json.dumps(json_object, indent=4)
    return pretty_json


def json_pretty_print(json_string):
    """Pretty print the json so it is readable."""
    print(json_prettify(json_string))


def _create_json_structure(json_data, path='', json_structure=''):
    """Create a json structure (as a string) for the given json_data."""
    from democritus_strings import cardinalize

    # the `tab` variable is blank on purpose.... I left it in the code so that it can be changed at a later date, but I think it looks best without using the tab
    tab = ''
    if isinstance(json_data, list):
        for index, i in enumerate(json_data):
            new_path = path + '[{}]'.format(index)
            json_structure = _create_json_structure(i, path=new_path, json_structure=json_structure)
    elif isinstance(json_data, dict):
        path = tab + path
        for key, value in json_data.items():
            new_path = path + "['{}']".format(key)
            if isinstance(value, list) or isinstance(value, dict):
                json_structure = json_structure + '\n{} (list of {} {})'.format(
                    new_path, len(value), cardinalize(type(value).__name__, len(value))
                )
                json_structure = _create_json_structure(value, path=new_path, json_structure=json_structure)
            else:
                # replace any newlines in the value so that they do not throw off the structure
                value = value.replace('\n', '\\n')
                json_structure = json_structure + '\n{}: {}'.format(new_path, value)
    # handle strings, ints, bools, etc...
    else:
        json_structure = json_structure + '\n{}: {} ({})'.format(path, str(json_data), type(json_data))

    return json_structure.strip()


@json_read_first_arg_string
def json_search(json_data, value_to_find):
    """Find the value_to_find in the json_data."""
    json_structure = _create_json_structure(json_data)

    paths = []

    for entry in json_structure.split('\n'):
        # TODO: this will not work if the key has a colon in it
        path = entry.split(':')[0]
        value = ':'.join(entry.split(':')[1:]).strip()
        if value_to_find in value:
            paths.append(path)

    return paths


@json_read_first_arg_string
def json_structure(json_data):
    """Print out the structure of the given json blob."""
    structure = _create_json_structure(json_data)
    return structure


# todo - how to read all files in a directory as json... (in fact, pattern = "how to _ all files in a directory")


def json_path_dot_notation_to_bracket_notation(json_path_dot_notation: str) -> str:
    if json_path_dot_notation == '':
        return ''
    replacement_characters = '"]["'
    new_path = f'["{json_path_dot_notation.replace(".", replacement_characters)}"]'
    return new_path


def json_path_bracket_notation_to_dot_notation(json_path_dot_notation: str) -> str:
    replacement_character = '.'
    new_path = json_path_dot_notation.strip('[]"\'')
    new_path = new_path.replace("']['", replacement_character)
    new_path = new_path.replace("\"][\"", replacement_character)
    return new_path
