#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import reduce
from operator import getitem
from fhir.resources.medication import Medication

from models.base import BaseModel
from models.searchparams import SearchParamsFactory
from managers.resourcemanager import ResourceManager


class ResourceModel(BaseModel):
    manager = ResourceManager()

    def __init__(self, res_type, data=None) -> None:
        super().__init__()
        self.id = None
        self.res_type = res_type
        self.updated = None
        self.data = data

    def searchparams(self):
        return SearchParamsFactory().prosess(self.fhir())


