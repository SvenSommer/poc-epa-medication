#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
import hashlib
import copy
import json

from fhir.resources import construct_fhir_element
from datetime import datetime, timezone

from controller.data import FHIRDataBase
from exceptions import ResourceIdFail


class BundleManager(object):

    def __init__(self) -> None:
        self.model_cls = None
    
    def get_total_count(self, res_type):
        total_count = FHIRDataBase(res_type=res_type).count()
        return total_count

    def search(self, res_type, offset, count):
        entries = []
        resultset = FHIRDataBase(res_type=res_type).search(offset, count)
        total_count = self.get_total_count(res_type=res_type)
        for data, _type in resultset:
            entries.append({'res_type': _type, 'data': data})
            # entries.append(construct_fhir_element(_type, data))
        model = self.model_cls()
        model.entries = entries
        model.total = total_count
        model.offset = offset
        model.count = count
        return model
    
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

