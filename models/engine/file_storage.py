#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """serializes instances to a JSON file & deserializes back to instances"""

    # string - path to the JSON file
    __file_path = "file.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """returns the dictionary __objects"""
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except Exception:
            pass

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()

    def get(self, cls, id):
        """
        Retrieve an object based on the class and its ID
        """
        all_cls = self.all(cls)
        for value in all_cls.values():
            if value.id == id:
                return value
        return None

    def count(self, cls=None):
        """
        Count the number of objects in storage matching the given class.
        """
        if cls:
            count = len(self.all(cls))
        else:
            count = 0
            for clas in classes.values():
                count += len(self.all(clas))
        return count

    def get(self, cls, id):
        """Retrieves a single object of the provided class by its ID.

        Args:
            cls: The class of the object to retrieve
            id: The unique identifier of the object.

        Returns:
            The requested object if found, otherwise None.
        """
        if cls is not None:
            res = list(
                filter(
                    lambda x: type(x) is cls and x.id == id,
                    self.__objects.values()
                )
            )
            if res:
                return res[0]
        return None

    def count(self, cls=None):
        """Retrieves the total count of objects in a given class.

        If no class is specified, counts all objects.

        Args:
            cls (type, optional): The class of objects to count. Defaults to
                None (count all objects).

        Returns:
            int: The total count of objects.
        """
        return len(self.all(cls))
