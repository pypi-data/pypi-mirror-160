"""
Copyright 2022 Andrey Plugin (9keepa@gmail.com)
Licensed under the Apache License v2.0
http://www.apache.org/licenses/LICENSE-2.0
"""
from dataclasses import dataclass
from typing import Union, List, Dict, TypedDict
import pickle
import zlib


class IBase:
    def to_dict(self) -> Dict:
        return self.__dict__


@dataclass
class MessageProtocol(IBase):
    status_code: int = 200
    payload: Union[List, Dict, None] = None
    action: str = str()
    message: str = str()


@dataclass
class IRenderData:
    html: bytes
    expiration_date: int
    status_code: int
    javascript: Union[None, int, str] = None

    @staticmethod
    def pickle_loads(data):
        return pickle.loads(data)

    @staticmethod
    def compress_zlib(data: str) -> bytes:
        return zlib.compress(data.encode("utf8"))

    def pickle_dump(self) -> bytes:
        return pickle.dumps(self)

    def decompress_field(self, name):
        if self.__dict__[name]:
            return zlib.decompress(self.__dict__[name]).decode("utf8")
        return None

    def to_dict(self):
        return {
            "html": self.decompress_field("html"),
            "javascript": self.javascript,
            "expiration_date": self.expiration_date,
            "status_code": self.status_code
        }


@dataclass
class IWebWaitRequest:
    name: str
    value: List[str]

    def to_dict(self):
        return {
            "name": self.name,
            "value": self.value
        }


class WebWaitDescriptor:

    def __set_name__(self, owner, name):
        self.private_name = "_" + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        if isinstance(value, dict):
            setattr(obj, self.private_name, IWebWaitRequest(
                name=value['name'],
                value=value['value']
            ))
        else:
            setattr(obj, self.private_name, None)


@dataclass
class IRenderRequestFlask:
    url: Union[str, None]
    wait: Union[float, int, None]
    expiration_date: int
    jscript: Union[str, None]
    web_wait: Union[IWebWaitRequest, None]

    web_wait = WebWaitDescriptor()

    def to_dict(self):
        return {
            "url": self.url,
            "wait": self.wait,
            "expiration_date": self.expiration_date,
            "jscript": self.jscript,
            "web_wait": self.web_wait.to_dict() if self.web_wait else None
        }

@dataclass
class IRenderRequestSelenium(IRenderRequestFlask):
    id: str