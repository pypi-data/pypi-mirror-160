import json
from abc import ABC

from bson import ObjectId


class ObjetoMongoAbstract(ABC):

    def __init__(self, _id=None, **kwargs):
        self._id = _id
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def id(self) -> ObjectId:
        return self._id

    def get_dict(self, id_mongo=True, id_as_string=False) -> dict:
        """
        Return all variables from this object, similar to vars(object) with exception for _id
        @param id_mongo: True -> Return dict with _id
        @param id_as_string: True -> Return _id as str if id_mongo is True
        @return: dict with object variables, similar to vars(object)
        """
        d = vars(self).copy()
        if not id_mongo:
            d.pop('_id')
        elif id_as_string and self._id is not None:
            d['_id'] = str(self._id)
        return d

    def get_dict_no_id(self) -> dict:
        """
        Fachade for get_dict(id_mongo=False). Return all variables from this object, similar to vars(object) with exception for _id
        @return: dict with object variables, similar to vars(object)
        """
        return self.get_dict(id_mongo=False)

    def serialize(self, id_mongo=True) -> str:
        """
        Serialize object to JSON format
        @param id_mongo: True -> Append _id to json
        @return: str in Json format
        """
        return json.dumps(self.get_dict(id_mongo=id_mongo, id_as_string=True))

    @staticmethod
    def serialize_all(objetos, id_mongo=True) -> str:
        """
        Serialize all objects to JSON format
        @param objetos: List for object to convert to JSON
        @param id_mongo: True -> Append _id to json
        @return: str in Json format
        """
        return json.dumps(ObjetoMongoAbstract.generar_list_dicts_from_list_objects(objetos, id_mongo=id_mongo,
                                                                                   id_as_string=True))

    @classmethod
    def generar_object_from_dict(cls, dictionary):
        if dictionary is None:
            return None
        return cls(**dictionary)

    @classmethod
    def generar_objects_from_list_dicts(cls, dictionaries: list):
        return [cls.generar_object_from_dict(dictionary) for dictionary in dictionaries]

    @staticmethod
    def generar_list_dicts_from_list_objects(lista_objetos: list, id_mongo=True, id_as_string=False):
        return [c.get_dict(id_mongo=id_mongo, id_as_string=id_as_string) for c in lista_objetos]
