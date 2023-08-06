"""Module for convert from project settings to markdown table of
environments."""
from enum import Enum
from sys import stdout
from typing import Iterable

from pydantic import BaseSettings
from pydantic.fields import ModelField, UndefinedType
from pydantic.main import ModelMetaclass

COLS = ['Name', 'Description', 'Type', 'Example', 'Default']


def pydantic_settings_to_table(obj: BaseSettings,
                               prefix: str = '',
                               config=None) -> dict:
    """From pydantic to table.

    Args:
        obj (BaseSettings): pydantic settings class

    Returns:
        list: table for markdown
    """
    if not config:
        config = obj.Config
    _table = []
    for _, field in obj.__fields__.items():
        field: ModelField = field

        env_names = field.field_info.extra.get('env_names', None)
        if env_names is None:
            env_names = [field.name]
        else:
            env_names = list(env_names)

        if isinstance(field.type_, ModelMetaclass):
            for env_name in env_names:
                _prefix = ''
                if getattr(config, 'env_nested_delimiter', False):
                    _prefix = f'{env_name}{config.env_nested_delimiter}'

                if not getattr(config, 'case_sensitive', False):
                    _prefix = _prefix.upper()
                _ttable = pydantic_settings_to_table(field.type_,
                                                     prefix=_prefix,
                                                     config=config)
                _table.extend(_ttable)
            continue

        if len(env_names) == 1:
            env_name = f'{prefix}{env_names[0]}'
        else:
            env_name = '; '.join(env_names)

        if not getattr(config, 'case_sensitive', False):
            env_name = env_name.upper()

        if len(env_names) > 1:
            env_name = f'Any of {env_name}'

        default = None
        if not isinstance(field.default, UndefinedType):
            default = field.default

        if isinstance(default, Enum):
            default = default.value

        example = default or ''
        if 'example' in field.field_info.extra:
            example = field.field_info.extra['example']

        if issubclass(field.type_, Enum):
            example = 'Any of: ' + '; '.join(
                [v.value for v in field.type_.__members__.values()])

        if field.required:
            # env_names = f'* {env_names}'
            default = '-'
        val = [
            env_name,
            field.field_info.description or '',
            field.type_,
            example,
            default,
        ]
        _table.append(dict(zip(COLS, val)))
    return _table


MARKDOWN_TEMPLATE = "| {: <%s} | {: <%s} | {: <%s} | {: <%s} | {: <%s} |"
BREAK_TEMPLATE = "| {:-<%s} | {:-<%s} | {:-<%s} | {:-<%s} | {:-<%s} |"


def table_to_markdown(
    table: list,
    buffer=stdout,
) -> str:
    max_in_column = dict(zip(COLS, [len(col) for col in COLS]))
    for row in table:
        row['Type'] = row['Type'].__name__
        if isinstance(row['Example'],
                      Iterable) and not isinstance(row['Example'], str):
            row['Example'] = ','.join([str(v) for v in row['Example']])
        for k in COLS:
            row[k] = str(row[k])
            size = len(row[k])
            if size > max_in_column[k]:
                max_in_column[k] = size

    maxes = tuple(max_in_column[k] for k in COLS)
    row_template = MARKDOWN_TEMPLATE % maxes

    # HEADER
    print(row_template.format(*COLS), file=buffer)
    # BREAK
    print((BREAK_TEMPLATE % maxes).format('', '', '', '', ''), file=buffer)

    # ROWS
    for row in table:
        print(row_template.format(*[row[k] for k in COLS]), file=buffer)
