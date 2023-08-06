"""Provides AssetVista datatypes definitions for creating and parsing data to Edgenius.

This module defines classes and methods for creating and parsing in the Edgenius formats.
"""

from typing import Dict, List, Union
import json

from .edgeniusFunctions import get_timestamp_edgenius_format
from .avlayerTypes import AvtypeNumeric, AvtypeInteger, AvtypeBoolean, AvtypeString
from .avlayerFunctions import parse_str_to_avtypenumeric, parse_str_to_avtypeinteger, parse_str_to_avtypeboolean, parse_str_to_avtypestring


__author__ = "Tiago Prata"
__copyright__ = "Copyright 2022, ABB Automacao Ltda (Brazil)"
__credits__ = ["ABB Automacao Ltda", "Tiago Prata"]
__license__ = "Copyright"
__version__ = "1.0.0"
__maintainer__ = "AssetVista Team"
__email__ = "BR-assetvista@abb.com"
__status__ = "Development (do not use in production)"


class EdgeniusInput:
    def __init__(self, key_name: str, value: Union[str, bool, int, float, List[str], List[bool], List[int], List[float]], quality: str = None, timestamp: str = None):
        self.key_name = key_name
        self.value = value
        self.quality = quality
        self.timestamp = timestamp
        self.avtype = self._parse_value_to_avtype(value)

    def _is_value_an_avtype(self, value: str) -> bool:
        """Checks it the payload is a valid json-like object and if its 'datatype' property is one of the valid Avtypes.

        Args:
            value (str): JSON-like string to be parsed to an Avtype

        Returns:
            bool: True if the value is a valid avtype.
        """

        try:
            obj = json.loads(value)
        except:
            return False

        if obj.get('dataType') != None:
            if (obj['dataType'] == 'AvtypeNumeric' or obj['dataType'] == 'AvtypeInteger' or
                obj['dataType'] == 'AvtypeBoolean' or obj['dataType'] == 'AvtypeString'):
                return True

        return False

    def _parse_value_to_avtype(self, value: str) -> Union[AvtypeBoolean, AvtypeInteger, AvtypeNumeric, AvtypeString]:
        if not self._is_value_an_avtype(value): return None

        avinput = json.loads(value)

        if avinput.get('value') == None: return None              # if 'value' existis

        if avinput['dataType'] == 'AvtypeNumeric':
            return parse_str_to_avtypenumeric(value)
        elif avinput['dataType'] == 'AvtypeInteger':
            return parse_str_to_avtypeinteger(value)
        elif avinput['dataType'] == 'AvtypeBoolean':
            return parse_str_to_avtypeboolean(value)
        elif avinput['dataType'] == 'AvtypeString':
            return parse_str_to_avtypestring(value)

        return None


class EdgeniusInputs:
    """Parses the Edgenius Streaming Calculation Engine inputs to Avtypes

    Args:
        payload_from_edgenius (Dict): Dictionary containing the values received from an Edgenius call.
    """

    def __init__(self, payload_from_edgenius: Dict):
        self.payload = payload_from_edgenius
        self.inputs: Dict[str, EdgeniusInput] = {}
        self._inputs_and_values = {}
        self._get_inputs()


    def _get_inputs(self):
        """Create an avtype-like input for every valid input in the payload."""

        self.inputs.clear()
        for key, value in self.payload.items():
            _quality = None
            _timestamp = None

            if value.get('value') != None:              # if 'value' existis
                if value.get('quality') != None: _quality = value['quality']
                if value.get('timestamp') != None: _timestamp = value['timestamp']
                self.inputs[key] = EdgeniusInput(key, value['value'], _quality, _timestamp)
                self._inputs_and_values[key] = value['value']


    def get_input_raw_value(self, key_name: str) -> Union[bool, int, float, str, None]:
        _value = None
        if self.inputs.get(key_name) != None:
            _value = self.inputs[key_name].value

        return _value

    
    def get_input_as_avtype(self, key_name: str) -> Union[AvtypeNumeric, AvtypeInteger, AvtypeBoolean, AvtypeString, None]:
        _value = None
        if self.inputs.get(key_name) != None:
            _value = self.inputs[key_name].avtype

        return _value


    def get_dict_of_inputs_and_values(self, skip_inputs_names: List[str] = None):
        new_dict = dict(self._inputs_and_values)
        if (skip_inputs_names):
            for name in skip_inputs_names:
                new_dict.pop(name)
        return new_dict



class EdgeniusOutput:
    """Write a key vaue in a Edgenius output format
    
    Args:
        key_name (str): Name of the key (variable)
        value ([float, int, bool, str]): Value of the variable
        timestamp (str, optional): Timestamp of the variable. Defaults to None.
        quality (int, optional): Quality. Defaults to None.
    """

    def __init__(self, key_name: str, value, timestamp: str = None, quality: int  = None):
        if not timestamp:
            self.timestamp = get_timestamp_edgenius_format()
        else: 
            self.timestamp = timestamp

        if not quality:
            self.quality = 1024
        else:
            self.quality = quality

        self.key_name = key_name

        if isinstance(value, (AvtypeNumeric, AvtypeInteger, AvtypeBoolean, AvtypeString)):
            self.value = str(value)
        else:
            self.value = value

    def get_key_and_values(self):
        """Return the inputed key and a dictionary in a Edgenius format

        Returns:
            key, value[Dict]: Key and dictionary in a Edgenius format
        """
        values = {"value": self.value, "quality": self.quality, "timestamp": self.timestamp}
        return self.key_name, values


class EdgeniusOutputList:
    """Defines a list of EdgeniusOutputs

    Args:
        list_of_edgenius_outputs (List[EdgeniusOutput]): List of many EdgeniusOutputs
    """

    def __init__(self, list_of_edgenius_outputs: List[EdgeniusOutput]):
        self.outputs = list_of_edgenius_outputs

    def get_all_outputs(self) -> dict:
        """Create and return a dict of EdgeniusOutputs

        Returns:
            dict: Dictionary containing all the EdgeniusOutputs
        """
        all_outputs = {}
        for output in self.outputs:
            output_key, output_value = output.get_key_and_values()
            all_outputs[output_key] = output_value

        return all_outputs