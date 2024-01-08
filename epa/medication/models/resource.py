#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models.base import BaseModel
from managers.resourcemanager import ResourceManager

class ResourceModel(BaseModel):
    manager = ResourceManager()

    def __init__(self, res_type, data=None) -> None:
        super().__init__()
        self.id = None
        self.res_type = res_type
        self.updated = None
        self.data = data
