#!/usr/bin/env python
"""Defines useful functions to perform calculations used in the Edgenius environment.

This module defines methods to be used in the Edgenius interfaces.
"""

from datetime import datetime


__author__ = "Tiago Prata"
__copyright__ = "Copyright 2022, ABB Automacao Ltda (Brazil)"
__credits__ = ["ABB Automacao Ltda", "Tiago Prata"]
__license__ = "Copyright"
__version__ = "1.0.0"
__maintainer__ = "AssetVista Team"
__email__ = "BR-assetvista@abb.com"
__status__ = "Development (do not use in production)"


def get_timestamp_edgenius_format(dt: datetime = None) -> str:
    """Get a datetime variable and returns it as string in the Edgenius format.

    Args:
        dt (datetime, optional): Datetime variable to be converted. If this argument is not passed, the function will return the Now() datetime. Defaults to None.

    Returns:
        str: Datetime as string in the edgenius format.
    """
    
    if dt == None:
        dt = datetime.now()
    date = dt.strftime('%Y-%m-%dT%H:%M:%S')
    ms = dt.strftime('.%f')[0:4]
    zone = dt.strftime('Z%Z')
    return date+ms+zone