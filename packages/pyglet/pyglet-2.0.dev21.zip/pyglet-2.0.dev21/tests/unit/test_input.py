import pytest

from pyglet import input


def test_parse_all_mappings():
    for mapping in input.controller.mapping_list:
        guid = mapping.split(',')[0]
        assert input.controller.get_mapping(guid)
