#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fhir.resources.bundle import Bundle, BundleLink
from fhir.resources.bundle import BundleEntry
from fhir.resources import construct_fhir_element

from models.base import BaseModel
from managers.bundlemanagers import BundleManager

class SearchSetBundleModel(BaseModel):
    manager = BundleManager()

    def __init__(self) -> None:
        super().__init__()
        self.entries = []
        self.res_type = 'Bundle'
        self.base_url = '/'
        self.total = 0
        self.offset = 0
        self.count = 25
        self.search_params = {}

    def get_fullurl(self, resource_type, id):
        return '{}/{}'.format(self.base_url, id)

    def create_pagination_links(self):
        links = []

        # Link zu den aktuellen Ergebnissen
        self_url = f"{self.base_url}?_offset={self.offset}&_count={self.count}"
        for param, value in self.search_params.items():
            self_url += f"&{param}={value}"
        links.append(BundleLink(relation="self", url=self_url))

        # Link zur nächsten Seite
        if self.offset + self.count < self.total:
            next_url = f"{self.base_url}?_offset={self.offset + self.count}&_count={self.count}"
            for param, value in self.search_params.items():
                next_url += f"&{param}={value}"
            links.append(BundleLink(relation="next", url=next_url))

        # Link zur vorherigen Seite
        if self.offset > 0:
            prev_offset = max(0, self.offset - self.count)
            prev_url = f"{self.base_url}?_offset={prev_offset}&_count={self.count}"
            for param, value in self.search_params.items():
                prev_url += f"&{param}={value}"
            links.append(BundleLink(relation="previous", url=prev_url))

        return links
    
    def fhir(self):
        bundle_entries = []
        for data in self.entries:
            resource = construct_fhir_element(data.get('res_type'), data.get('data'))
            fullUrl = self.get_fullurl(data.get('res_type'), resource.id)
            bundle_entries.append(BundleEntry(resource=resource, fullUrl=fullUrl))
        bundle = Bundle(type="searchset", entry=bundle_entries)
        bundle.total = self.total
        bundle.link = self.create_pagination_links()
        return bundle
    
    def save(self):
        return False

