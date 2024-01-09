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
                                               data_hash=model.hash,
                                               searchparams=model.searchparams())
        return True
