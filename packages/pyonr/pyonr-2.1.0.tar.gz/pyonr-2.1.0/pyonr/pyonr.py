import os
from typing import Any
from ast import literal_eval

from .errors import *
from .decoder import PYONDecoder
from .encoder import PYONEncoder
from .converter import convert, PYON, JSON, OBJ, STR
from .builtins import is_pyon, is_json

class Read:
    def __init__(self, filepath:str, encoding:str='utf-8'):
        self.filepath = filepath
        self.encoding = encoding

        with open(filepath, 'r', encoding=self.encoding) as file:
            PYONDecoder(file.read(), self.encoding).decode()

    def write(self, obj):
        filepath = self.filepath
        
        with open(filepath, 'w', encoding=self.encoding) as file:
            file.write(PYONEncoder(obj, self.encoding).encode())

    @property
    def read(self) -> Any:
        filepath = self.filepath

        with open(filepath, 'r', encoding=self.encoding) as file:
            return PYONDecoder(file.read(), self.encoding).decode()


    
    def __repr__(self) -> str:
        args = []
        args.append(f'filepath={self.filepath}')
        args.append(f'encoding={self.encoding}')

        return f'{self.__class__.__qualname__}({", ".join(args)})'

    def __str__(self) -> str:
        return convert(PYON, STR, self.read)

class ReadV2:
    def __init__(self, filepath:str, encoding:str='utf-8'):
        self.filepath = filepath
        self.encoding = encoding

        with open(filepath, 'r', encoding=self.encoding) as file:
            PYONDecoder(file.read(), self.encoding).decode() # validate filedata once

        self.fileR = open(filepath, 'r', encoding=encoding)
        self.fileW = open(filepath, 'w', encoding=encoding)

    def write(self, obj):
        self.fileW.write(PYONEncoder(obj, self.encoding).encode())

    @property
    def read(self) -> Any:
        return PYONDecoder(self.fileR.read(), self.encoding).decode()
    
    def __repr__(self) -> str:
        args = []
        args.append(f'filepath={self.filepath}')
        args.append(f'encoding={self.encoding}')

        return f'{self.__class__.__qualname__}({", ".join(args)})'

    def __str__(self) -> str:
        return convert(PYON, STR, self.read)

def read(fp:str, version:int=2, encoding:str='utf-8') -> Read:
    '''
    Read pyon file

    Parameters:
    -----------

    fp: str
        filepath to pyon file

    version: int = 2
        which version of pyon.Read is used to intract with the file
        
        `use version 2 if invalid version was given`

    encoding: str = 'utf-8'
        encoding
        
    '''
    if version is 1:
        return Read(fp, encoding)

    return ReadV2(fp, encoding)