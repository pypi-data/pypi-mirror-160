from typing import TypeVar, Type, Generic

import pymongo
from pymongo.results import UpdateResult, InsertManyResult, InsertOneResult, DeleteResult

from ..entity.objeto_mongo_abstract import ObjetoMongoAbstract
from ..mongo_manager import SingletonMeta
from bson import ObjectId

T_O = TypeVar('T_O', bound=ObjetoMongoAbstract)


class RepositoryBase(Generic[T_O], metaclass=SingletonMeta):

    def __init__(self, collection, clase: Type[T_O]) -> None:
        __metaclass__ = SingletonMeta
        from ..mongo_manager import mongo_manager_gl
        self.__collection = mongo_manager_gl.collection(collection)
        self.__clase = clase

    @property
    def collection(self) -> pymongo.collection.Collection:
        """
        @return: Pymongo collection | Coleccion Pymongo
        """
        return self.__collection

    @property
    def clase(self):
        """
        @return: Class used in the repository to convert data o objects| Clase del repositorio
        """
        return self.__clase

    def count_many(self, filter_dict: dict = None) -> int:
        if filter_dict is None:
            filter_dict = {}
        return self.collection.count_documents(filter_dict)

    def count_all(self) -> int:
        return self.collection.count_documents({})

    def find_one(self, filter_dict: dict = None) -> T_O:
        if filter_dict is None:
            filter_dict = {}
        return self.clase.generar_object_from_dict(self.collection.find_one(filter_dict))

    def find_many(self, filter_dict: dict = None, skip=0, limit=1000) -> list[T_O]:
        if filter_dict is None:
            filter_dict = {}
        return self.clase.generar_objects_from_list_dicts(self.collection.find(filter_dict).skip(skip).limit(limit))

    def find_all(self, skip=0, limit=1000) -> list[T_O]:
        return self.clase.generar_objects_from_list_dicts(self.collection.find().skip(skip).limit(limit))

    def find_by_id(self, id_mongo) -> T_O:
        return self.clase.generar_object_from_dict(self.collection.find_one({'_id': ObjectId(id_mongo)}))

    def delete_object(self, objeto: T_O) -> DeleteResult:
        if objeto.id is not None:
            return self.delete_by_id(objeto.id)

    def delete_by_id(self, id_mongo) -> DeleteResult:
        return self.collection.delete_one({'_id': ObjectId(id_mongo)})

    def insert_one(self, objeto: T_O) -> InsertOneResult:
        return self.collection.insert_one(objeto.get_dict_no_id())

    def insert_many(self, lista_objetos: list[T_O]) -> InsertManyResult:
        return self.collection.insert_many(self.clase.generar_list_dicts_from_list_objects(lista_objetos))

    def insert_or_replace_id(self, objeto: T_O):
        if objeto.id is None:
            return self.insert_one(objeto)
        else:
            return self.replace_by_id(objeto.id, objeto)

    def replace_by_id(self, id_mongo, objeto: T_O) -> UpdateResult:
        return self.collection.replace_one({"_id": id_mongo}, objeto.get_dict())

    def update_by_id(self, id_mongo, objeto_dict: dict) -> UpdateResult:
        return self.collection.update_one({"_id": id_mongo}, {"$set": objeto_dict})

    def update_many(self,  filter_dict: dict = None, objeto_dict: dict = None) -> UpdateResult:
        if objeto_dict is None:
            return None
        if filter_dict is None:
            filter_dict = {}
        self.collection.update_many(filter_dict, {"$set": objeto_dict})