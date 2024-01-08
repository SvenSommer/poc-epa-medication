#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import copy
import uuid

from datetime import datetime, timezone
from fhir.resources import construct_fhir_element


class BaseModelMetaClass(type):

    def __new__(cls, name, bases, attrs, **kwargs):
        new_class = super().__new__(cls, name, bases, attrs)
        manager = getattr(new_class, 'manager', None)
        if manager:
            manager.model_cls = new_class
        return new_class


class BaseModel(metaclass=BaseModelMetaClass):
    
    @property
    def hash(self):
        r = copy.deepcopy(self.fhir())
        r.meta = None
        m = hashlib.sha256()
        m.update(str('{}'.format(r.json())).encode())
        return m.hexdigest()
    
    def fhir(self):
        resource = construct_fhir_element(self.res_type, self.data)
        resource.id = str(self.id)
        resource.meta.lastUpdated = self.updated
        return resource
    
    def json(self):
        return self.fhir().json()
    
    def dict(self):
        return self.fhir().dict()

    def save(self):
        if self.id is None:
            self.id = str(uuid.uuid4())
            self.updated = datetime.now(timezone.utc)
            self.manager.create(model=self)
            return self.fhir()
        return None
