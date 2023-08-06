#!/usr/bin/env python
"""Provides AssetVista datatypes definitions for creating and parsing data.

This module defines classes and methods for creating and parsing AvtypeNumeric,
AvtypeInteger, AvtypeBoolean and AvtypeString.
"""

from __future__ import annotations
import json
from typing import Union
import pint

from .edgeniusFunctions import get_timestamp_edgenius_format


__author__ = "Tiago Prata"
__copyright__ = "Copyright 2022, ABB Automacao Ltda (Brazil)"
__credits__ = ["ABB Automacao Ltda", "Tiago Prata"]
__license__ = "Copyright"
__version__ = "1.0.0"
__maintainer__ = "AssetVista Team"
__email__ = "BR-assetvista@abb.com"
__status__ = "Development (do not use in production)"


def _convert_value_to(value: Union(float, int), origianl_unit: str, target_unit: str) -> Union(float, int):
        ureg = pint.UnitRegistry(preprocessors=[
            lambda s: s.replace('%%', ' permille '),
            lambda s: s.replace('%', ' percent '),
        ])
        ureg.define('permille = 0.001 = %%')  # or 'permille = 1 / 1000 = %%'
        ureg.define('percent = 0.01 = %')

        if ureg(origianl_unit).check('[temperature]'):
            Q_ = ureg.Quantity
            value_with_unit = Q_(value, ureg[origianl_unit])
            return value_with_unit.to(target_unit).magnitude
        else:
            value_with_unit = value * ureg(origianl_unit)
            return value_with_unit.to(target_unit).magnitude


class AvtypeNumeric:
    """Type definition for Numeric (float) values to be used in the AssetVista Edgenius environment.
    
    Args:
        description (str): Description of the variable
        value (float): Variable value. It displays the 'simulation_value' if 'simulation_enabled' is True, otherwise it displays the 'value_from_input' value.
        unit (str): Variable unit (e.g.: current, voltage, meters, etc). (It is recommended to use the definitions from Pint package)
        simulation_enabled (bool): If enabled, the 'simulation_value' property will override the 'value' value.
        simulation_value (float): Value to be ised when 'siulation_enabled' is True
        max (float): The maximum value this variable can indicate. If the 'value' is above 'max', 'out_of_range' is set to True.
        min (float): The minimum value this variable can indicate. If the 'value' is below 'min', 'out_of_range' is set to True.
        value_from_input (float): Value to be assigned to the class. It is displayed in the 'value' if 'simualtion_enabled' is False.
        in_use (bool, optional): Indicates if this variable is in use. Defaults to True.
        timestamp (str, optional): Timestamp last time the variable was calculated. Defaults to Now() (in Edgenius format).
        quality (int, optional): Variable quality. Defaults to 1024.
        dataType (str, optional): String indicating the datatype from avtypes. Defaults to 'AvtypeNumeric'.
    """

    # class attributes are only used for defining the BaseModel attributes
    description: str = ""
    value: float = 0.0
    unit: str = ""
    in_use: bool = True
    timestamp: str = ""
    simulation_enabled: bool = False
    simulation_value: float = 0.0
    max: float = 0.0
    min: float = 0.0
    out_of_range: bool = False
    quality: int = 1024
    dataType: str = 'AvtypeNumeric'
    value_from_input: float = 0.0

    def __init__(self, description: str,
                        unit: str,
                        simulation_enabled: bool,
                        simulation_value: float,
                        max: float,
                        min: float,
                        value_from_input: float,
                        in_use: bool = True,
                        timestamp: str = get_timestamp_edgenius_format(),
                        quality: int = 1024,
                        dataType: str = 'AvtypeNumeric'):

        out_of_range = False
        if (min<max):
            if simulation_enabled:
                out_of_range = (simulation_value > max or simulation_value < min)
            else:
                out_of_range = (value_from_input > max or value_from_input < min)
        
        self.description = description
        self.value = simulation_value if simulation_enabled else value_from_input
        self.unit = unit
        self.in_use = in_use
        self.timestamp = timestamp
        self.simulation_enabled = simulation_enabled
        self.simulation_value = simulation_value
        self.max = max
        self.min = min
        self.out_of_range = out_of_range
        self.quality = quality
        self.dataType = dataType
        self.value_from_input = value_from_input

    def __str__(self):
        return json.dumps(self.__dict__)

    def convert_to(self, target_unit: str) -> AvtypeNumeric:
        conv_obj = AvtypeNumeric(description=self.description,
                                    unit=target_unit,
                                    simulation_enabled=self.simulation_enabled,
                                    simulation_value=_convert_value_to(self.simulation_value, self.unit, target_unit),
                                    max=_convert_value_to(self.max, self.unit, target_unit),
                                    min=_convert_value_to(self.min, self.unit, target_unit),
                                    value_from_input=_convert_value_to(self.value_from_input, self.unit, target_unit),
                                    in_use=self.in_use,
                                    timestamp=self.timestamp,
                                    quality=self.quality)

        return conv_obj


class AvtypeInteger:
    """Type definition for Integer (int) values to be used in the AssetVista Edgenius environment.
    
    Args:
        description (str): Description of the variable
        value (int): Variable value. It displays the 'simulation_value' if 'simulation_enabled' is True, otherwise it displays the 'value_from_input' value.
        unit (str): Variable unit (e.g.: current, voltage, meters, etc). (It is recommended to use the definitions from Pint package)
        simulation_enabled (bool): If enabled, the 'simulation_value' property will override the 'value' value.
        simulation_value (int): Value to be ised when 'siulation_enabled' is True
        max (int): The maximum value this variable can indicate. If the 'value' is above 'max', 'out_of_range' is set to True.
        min (int): The minimum value this variable can indicate. If the 'value' is below 'min', 'out_of_range' is set to True.
        value_from_input (int): Value to be assigned to the class. It is displayed in the 'value' if 'simualtion_enabled' is False.
        in_use (bool, optional): Indicates if this variable is in use. Defaults to True.
        timestamp (str, optional): Timestamp last time the variable was calculated. Defaults to Now() (in Edgenius format).
        quality (int, optional): Variable quality. Defaults to 1024.
        dataType (str, optional): String indicating the datatype from avtypes. Defaults to 'AvtypeInteger'.
    """

    # class attributes are only used for defining the BaseModel attributes
    description: str = ""
    value: int = 0
    unit: str = ""
    in_use: bool = True
    timestamp: str = ""
    simulation_enabled: bool = False
    simulation_value: int = 0
    max: int = 0
    min: int = 0
    out_of_range: bool = False
    quality: int = 1024
    dataType: str = 'AvtypeInteger'
    value_from_input: int = 0

    def __init__(self, description: str,
                        unit: str,
                        simulation_enabled: bool,
                        simulation_value: int,
                        max: int,
                        min: int,
                        value_from_input: int,
                        in_use: bool = True,
                        timestamp: str = get_timestamp_edgenius_format(),
                        quality: int = 1024,
                        dataType: str = 'AvtypeInteger'):
        
        out_of_range = False
        if (min<max):
            if simulation_enabled:
                out_of_range = (simulation_value > max or simulation_value < min)
            else:
                out_of_range = (value_from_input > max or value_from_input < min)

        self.description = description
        self.value = simulation_value if simulation_enabled else value_from_input
        self.unit = unit
        self.in_use = in_use
        self.timestamp = timestamp
        self.simulation_enabled = simulation_enabled
        self.simulation_value = simulation_value
        self.max = max
        self.min = min
        self.out_of_range = out_of_range
        self.quality = quality
        self.dataType = dataType
        self.value_from_input = value_from_input

    def __str__(self):
        return json.dumps(self.__dict__)

    def convert_to(self, target_unit: str) -> AvtypeInteger:
        conv_obj = AvtypeInteger(description=self.description,
                                    unit=target_unit,
                                    simulation_enabled=self.simulation_enabled,
                                    simulation_value=int(_convert_value_to(self.simulation_value, self.unit, target_unit)),
                                    max=int(_convert_value_to(self.max, self.unit, target_unit)),
                                    min=int(_convert_value_to(self.min, self.unit, target_unit)),
                                    value_from_input=int(_convert_value_to(self.value_from_input, self.unit, target_unit)),
                                    in_use=self.in_use,
                                    timestamp=self.timestamp,
                                    quality=self.quality)

        return conv_obj


class AvtypeBoolean:
    """Type definition for Boolean (bool) values to be used in the AssetVista Edgenius environment.
    
    Args:
        description (str): Description of the variable
        value (bool): Variable value. It displays the 'simulation_value' if 'simulation_enabled' is True, otherwise it displays the 'value_from_input' value.
        simulation_enabled (bool): If enabled, the 'simulation_value' property will override the 'value' value.
        simulation_value (bool): Value to be ised when 'siulation_enabled' is True
        value_from_input (bool): Value to be assigned to the class. It is displayed in the 'value' if 'simualtion_enabled' is False.
        in_use (bool, optional): Indicates if this variable is in use. Defaults to True.
        timestamp (str, optional): Timestamp last time the variable was calculated. Defaults to Now() (in Edgenius format).
        quality (int, optional): Variable quality. Defaults to 1024.
        dataType (str, optional): String indicating the datatype from avtypes. Defaults to 'AvtypeBoolean'.
    """

    # class attributes are only used for defining the BaseModel attributes
    description: str = ""
    value: bool = False
    in_use: bool = True
    timestamp: str = ""
    simulation_enabled: bool = False
    simulation_value: bool = False
    quality: int = 1024
    dataType: str = 'AvtypeBoolean'
    value_from_input: bool = False

    def __init__(self, description: str,
                        simulation_enabled: bool,
                        simulation_value: bool,
                        value_from_input: bool,
                        in_use: bool = True,
                        timestamp: str = get_timestamp_edgenius_format(),
                        quality: int = 1024,
                        dataType: str = 'AvtypeBoolean'):
        
        self.description = description
        self.value = simulation_value if simulation_enabled else value_from_input
        self.in_use = in_use
        self.timestamp = timestamp
        self.simulation_enabled = simulation_enabled
        self.simulation_value = simulation_value
        self.quality = quality
        self.dataType = dataType
        self.value_from_input = value_from_input

    def __str__(self):
        return json.dumps(self.__dict__)


class AvtypeString:
    """Type definition for String (str) values to be used in the AssetVista Edgenius environment.
    
    Args:
        description (str): Description of the variable
        value (str): Variable value. It displays the 'simulation_value' if 'simulation_enabled' is True, otherwise it displays the 'value_from_input' value.
        simulation_enabled (bool): If enabled, the 'simulation_value' property will override the 'value' value.
        simulation_value (str): Value to be ised when 'siulation_enabled' is True
        value_from_input (str): Value to be assigned to the class. It is displayed in the 'value' if 'simualtion_enabled' is False.
        in_use (bool, optional): Indicates if this variable is in use. Defaults to True.
        timestamp (str, optional): Timestamp last time the variable was calculated. Defaults to Now() (in Edgenius format).
        quality (int, optional): Variable quality. Defaults to 1024.
        dataType (str, optional): String indicating the datatype from avtypes. Defaults to 'AvtypeBoolean'.
    """

    # class attributes are only used for defining the BaseModel attributes
    description: str = ""
    value: str = ""
    in_use: bool = True
    timestamp: str = ""
    simulation_enabled: bool = False
    simulation_value: str = ""
    quality: int = 1024
    dataType: str = 'AvtypeString'
    value_from_input: str = ""

    def __init__(self, description: str,
                        simulation_enabled: bool,
                        simulation_value: str,
                        value_from_input: str,
                        in_use: bool = True,
                        timestamp: str = get_timestamp_edgenius_format(),
                        quality: int = 1024,
                        dataType: str = 'AvtypeString'):
        
        self.description = description
        self.value = simulation_value if simulation_enabled else value_from_input
        self.in_use = in_use
        self.timestamp = timestamp
        self.simulation_enabled = simulation_enabled
        self.simulation_value = simulation_value
        self.quality = quality
        self.dataType = dataType
        self.value_from_input = value_from_input

    def __str__(self):
        return json.dumps(self.__dict__)

