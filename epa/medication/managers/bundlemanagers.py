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
from models.searchparams import SearchParam


class BundleManager(object):

    def __init__(self) -> None:
        self.model_cls = None
        self._total_count = 0
    
    def get_total_count(self, res_type):
        return self._total_count

    def search(self, res_type, offset, count, **searchparams):
        _searchparams = []
        for param_name, value in searchparams.items():
            _searchparams.append(SearchParam(name=param_name, value=value))
        entries = []
        self.total_count, resultset = FHIRDataBase(res_type=res_type).search(offset, count, searchparams=_searchparams)
        for data, _type in resultset:
            entries.append({'res_type': _type, 'data': data, 'search': 'match'})
        model = self.model_cls()
        model.entries = entries
        model.total = self.total_count
        model.offset = offset
        model.count = count
        model.search_params = _searchparams

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

