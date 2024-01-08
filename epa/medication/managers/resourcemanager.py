#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
import hashlib
import copy

from fhir.resources import construct_fhir_element
from datetime import datetime, timezone

from controller.data import FHIRDataBase
from exceptions import ResourceIdFail


class ResourceManager(object):

    def __init__(self) -> None:
        self.model_cls = None

    def get(self, res_type, id):
        data = FHIRDataBase(res_type=res_type).get_instance(id=id)
        if data is None:
            raise ResourceIdFail()
        model = self.model_cls(res_type, data)
        return model

    def create(self, model):
        FHIRDataBase(res_type=model.res_type).create(id=model.id,
                                               updated=model.updated,
                                               data_json=model.json(),
                                               data_hash=model.hash)
        return True
    
    def search(self, res_type, offset, count):
        entries = []
        resultset = FHIRDataBase(res_type=res_type).search(offset, count)
        for data, _type in resultset:
            entries.append(construct_fhir_element(_type, data))
        return entries
    
    def get_all(self):
        entries = {
            "Organisations": [],
            "Medications": [],
            "Practitioners": [],
            "MedicationRequests": [],
            "MedicationDispenses": []
        }
        resultset = FHIRDataBase(res_type=None).get_all()
        for data, _type in resultset:
            entries['{}s'.format(_type)].append(construct_fhir_element(_type, data).dict())
        return entries