#!/usr/bin/env python3
"""This module contains helper functions."""

import re


def convert_camel_to_snake(text: str):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def universal_obj_hook(obj: [list, dict]):
    if isinstance(obj, list):
        result = []
        for i in obj:
            result.append(_object_hook(i))
        return result

    if isinstance(obj, dict):
        return _object_hook(obj)

    return obj


def _object_hook(obj: dict):
    cleaned_object = {}
    for key, value in obj.items():
        key = convert_camel_to_snake(key.replace('-', '_'))

        if len(key) and key[0].isdigit():
            key = '_' + key

        cleaned_object.update({key: value})
    return cleaned_object
