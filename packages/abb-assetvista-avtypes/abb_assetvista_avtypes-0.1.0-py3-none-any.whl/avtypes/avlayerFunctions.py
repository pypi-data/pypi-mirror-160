#!/usr/bin/env python
"""Provides AssetVista datatypes definitions for creating and parsing data.

This module defines methods for parsing AvtypeNumeric,
AvtypeInteger, AvtypeBoolean and AvtypeString.
"""

import json

from .avlayerTypes import AvtypeNumeric, AvtypeInteger, AvtypeBoolean, AvtypeString


__author__ = "Tiago Prata"
__copyright__ = "Copyright 2022, ABB Automacao Ltda (Brazil)"
__credits__ = ["ABB Automacao Ltda", "Tiago Prata"]
__license__ = "Copyright"
__version__ = "1.0.0"
__maintainer__ = "AssetVista Team"
__email__ = "BR-assetvista@abb.com"
__status__ = "Development (do not use in production)"


def parse_str_to_avtypenumeric(string_value) -> AvtypeNumeric:
    """Parse json values in a string format to AvtypeNumeric

    Args:
        string_value (str): JSON values dumped as string. String must have the AvtypeNumeric properties as keys (e.g: {'value': 8.0, 'description': 'desc' [...]})

    Returns:
        AvtypeNumeric: AvtypeNumeric object parsed
    """
    # load string as json
    string_obj = json.loads(string_value)
    value = string_obj.get('value')
    if value == None:
        return None

    # Read JSON keys
    description = string_obj.get('description')
    unit = string_obj.get('unit')
    in_use = string_obj.get('in_use')
    timestamp = string_obj.get('timestamp')
    simulation_enabled = string_obj.get('simulation_enabled')
    simulation_value = string_obj.get('simulation_value')
    max = string_obj.get('max')
    min = string_obj.get('min')
    quality = string_obj.get('quality')

    # Create AvtypeNumeric
    avtype_numeric = AvtypeNumeric(description = description,
                                    unit = unit,
                                    in_use = in_use,
                                    timestamp = timestamp,
                                    simulation_enabled = simulation_enabled,
                                    simulation_value = simulation_value,
                                    max = max,
                                    min = min,
                                    quality = quality,
                                    value_from_input = value)

    return avtype_numeric


def parse_str_to_avtypeinteger(string_value) -> AvtypeInteger:
    """Parse json values in a string format to AvtypeInteger

    Args:
        string_value (str): JSON values dumped as string. String must have the AvtypeInteger properties as keys (e.g: {'value': 8, 'description': 'desc' [...]})

    Returns:
        AvtypeInteger: AvtypeInteger object parsed
    """
    # load string as json
    string_obj = json.loads(string_value)
    value = string_obj.get('value')
    if value == None:
        return None

    # Read JSON keys
    description = string_obj.get('description')
    unit = string_obj.get('unit')
    in_use = string_obj.get('in_use')
    timestamp = string_obj.get('timestamp')
    simulation_enabled = string_obj.get('simulation_enabled')
    simulation_value = string_obj.get('simulation_value')
    max = string_obj.get('max')
    min = string_obj.get('min')
    out_of_range = string_obj.get('out_of_range')
    quality = string_obj.get('quality')

    # Create AvtypeInteger
    avtype_integer = AvtypeInteger(description = description,
                                    unit = unit,
                                    in_use = in_use,
                                    timestamp = timestamp,
                                    simulation_enabled = simulation_enabled,
                                    simulation_value = simulation_value,
                                    max = max,
                                    min = min,
                                    quality = quality,
                                    value_from_input = value)

    return avtype_integer


def parse_str_to_avtypeboolean(string_value) -> AvtypeBoolean:
    """Parse json values in a string format to AvtypeBoolean

    Args:
        string_value (str): JSON values dumped as string. String must have the AvtypeBoolean properties as keys (e.g: {'value': False, 'description': 'desc' [...]})

    Returns:
        AvtypeBoolean: AvtypeBoolean object parsed
    """
    # load string as json
    string_obj = json.loads(string_value)
    value = string_obj.get('value')
    if value == None:
        return None

    # Read JSON keys
    description = string_obj.get('description')
    in_use = string_obj.get('in_use')
    timestamp = string_obj.get('timestamp')
    simulation_enabled = string_obj.get('simulation_enabled')
    simulation_value = string_obj.get('simulation_value')
    quality = string_obj.get('quality')

    # Create AvtypeBoolean
    avtype_boolean = AvtypeBoolean(description = description,
                                    in_use = in_use,
                                    timestamp = timestamp,
                                    simulation_enabled = simulation_enabled,
                                    simulation_value = simulation_value,
                                    quality = quality,
                                    value_from_input = value)

    return avtype_boolean


def parse_str_to_avtypestring(string_value) -> AvtypeString:
    """Parse json values in a string format to AvtypeString

    Args:
        string_value (str): JSON values dumped as string. String must have the AvtypeString properties as keys (e.g: {'value': 'test', 'description': 'desc' [...]})

    Returns:
        AvtypeString: AvtypeString object parsed
    """
    # load string as json
    string_obj = json.loads(string_value)
    value = string_obj.get('value')
    if value == None:
        return None

    # Read JSON keys
    description = string_obj.get('description')
    in_use = string_obj.get('in_use')
    timestamp = string_obj.get('timestamp')
    simulation_enabled = string_obj.get('simulation_enabled')
    simulation_value = string_obj.get('simulation_value')
    quality = string_obj.get('quality')

    # Create AvtypeBoolean
    avtype_string = AvtypeString(description = description,
                                    in_use = in_use,
                                    timestamp = timestamp,
                                    simulation_enabled = simulation_enabled,
                                    simulation_value = simulation_value,
                                    quality = quality,
                                    value_from_input = value)

    return avtype_string