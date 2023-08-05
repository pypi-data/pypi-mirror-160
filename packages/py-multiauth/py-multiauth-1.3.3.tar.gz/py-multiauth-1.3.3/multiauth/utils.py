"""Utility functions independent of the library."""

from typing import Mapping, TypeVar

from pydash import py_

Default = TypeVar('Default')
Value = TypeVar('Value')


def dict_find_path(nested_dict: Mapping, key: str, prepath: str = '', index: int | None = None) -> str:
    """Recursively find the path of a certain key in a dict."""
    for k, v in nested_dict.items():
        if prepath == '':
            path = k
        elif index is not None:
            path = f'{prepath}.{index}.{k}'
        else:
            path = f'{prepath}.{k}'
        if k == key:  # found value
            return path
        if isinstance(v, dict):
            p = dict_find_path(v, key, path, None)  # recursive call
            if p != '':
                return p
        if isinstance(v, list):
            for i, elem in enumerate(v):
                if isinstance(elem, dict):
                    p = dict_find_path(elem, key, path, i)
                    if p != '':
                        return p
    return ''


def dict_nested_get(dictionary: Mapping[str, Value], key: str, default_return: Default = None) -> Default | Value:
    """Search for a certain key inside a dict and returns its value (no matter the depth)"""
    return py_.get(dictionary, dict_find_path(dictionary, key, ''), default_return)
