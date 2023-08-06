#!/usr/bin/env python3
import sys

from conf2env import (import_from_string, pydantic_settings_to_table,
                      table_to_markdown)


def read_object():
    python_obj = sys.argv[1]

    return import_from_string(python_obj)


def main():
    obj = read_object()
    _table = pydantic_settings_to_table(obj)
    table_to_markdown(_table)

main()
