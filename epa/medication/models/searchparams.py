#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib

from fhir.resources.medication import Medication

class SearchParamsFactory(object):

    def __init__(self) -> None:
        self._searchparams = []

    def prosess(self, resource):
        result = []
        if isinstance(resource, Medication):
            for identifier in resource.identifier:
                result.append(SearchParam(name='identifier', value=identifier.value))  
        return result
    
class SearchParam(object):

    def __init__(self, name, value) -> None:
        self.name = name
        self.value = value

    @property
    def hash_value(self):
        hash = hashlib.sha256()
        hash.update(str('{}'.format(self.value)).encode())
        return hash.hexdigest()