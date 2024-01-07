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

    def hash_resource(self, resource):
        r = copy.deepcopy(resource)
        r.meta = None
        m = hashlib.sha256()
        m.update(str('{}'.format(r.json())).encode())
        return m.hexdigest()
    
    def get(self, res_type, id):
        data = FHIRDataBase(res_type=res_type).get_instance(id=id)
        if data is None:
            raise ResourceIdFail()
        resource = construct_fhir_element(res_type, data)
        return resource
    
    def create(self, res_type, data):
        resource = construct_fhir_element(res_type, data)
        resource.id = str(uuid.uuid4())
        resource.meta.lastUpdated = datetime.now(timezone.utc)
        FHIRDataBase(res_type=res_type).create(id=resource.id,
                                               updated=resource.meta.lastUpdated,
                                               data_json=resource.json(),
                                               data_hash=self.hash_resource(resource=resource))
        return resource
    
    def get_total_count(self, res_type):
        total_count = FHIRDataBase(res_type=res_type).count()
        return total_count

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

