from BCCancerAPI.dbmodels import User
from typing import Any, Dict
from sqlalchemy.orm import class_mapper


def row_to_dict(row):

    dict = {}
    for column in row.keys()._keys:
        dict[column] = str(getattr(row, column))
    return dict


def user_to_dict(user: [User, None]) -> Dict[str, Any]:
    # Get the mapper object for the Ornament class
    mapper = class_mapper(user.__class__)

    # Get a list of all the column names
    columns = [column.key for column in mapper.columns]
    # Create a dictionary with the column names as keys and the attribute values as values
    user_dict = {}
    for column in columns:
        value = getattr(user, column)
        user_dict[column] = value
    return user_dict
