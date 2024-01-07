#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import uuid

from datetime import datetime
from flask import Blueprint, request, jsonify

from fhir.resources.bundle import Bundle, BundleLink
from fhir.resources.bundle import BundleEntry

from settings import SUPORTED_RESOURCE_TYPES
from managers.resourcemanager import ResourceManager
from exceptions import FHIRException, UnknownResourceType

logging.basicConfig(level=logging.INFO)

fhir_api = Blueprint('fhir_api', __name__)


@fhir_api.errorhandler(FHIRException)
def handle_fhir_error(error):
    return jsonify(error.operation_outcome), error.status_code


def create_pagination_links(offset, count, total, base_url, search_params):
    links = []

    # Link zu den aktuellen Ergebnissen
    self_url = f"{base_url}?_offset={offset}&_count={count}"
    for param, value in search_params.items():
        self_url += f"&{param}={value}"
    links.append(BundleLink(relation="self", url=self_url))

    # Link zur nächsten Seite
    if offset + count < total:
        next_url = f"{base_url}?_offset={offset + count}&_count={count}"
        for param, value in search_params.items():
            next_url += f"&{param}={value}"
        links.append(BundleLink(relation="next", url=next_url))

    # Link zur vorherigen Seite
    if offset > 0:
        prev_offset = max(0, offset - count)
        prev_url = f"{base_url}?_offset={prev_offset}&_count={count}"
        for param, value in search_params.items():
            prev_url += f"&{param}={value}"
        links.append(BundleLink(relation="previous", url=prev_url))

    return links


def get_fullurl(resource_type, id):
    return '/fhir/{}/{}'.format(resource_type, id)


@fhir_api.route("/fhir/<resource_type>", methods=["GET"])
def search_resource(resource_type):
    if not resource_type in SUPORTED_RESOURCE_TYPES:
        raise UnknownResourceType()
    # Paginationsparameter
    offset = int(request.args.get('_offset', 0))
    count = int(request.args.get('_count', 25))

    base_url = '/fhir/{}'.format(resource_type)
    search_params = {}

    manager = ResourceManager()
    total = manager.get_total_count(resource_type)
    entries = manager.search(resource_type, offset=offset, count=count)

    bundle_entries = [BundleEntry(resource=resource, fullUrl=get_fullurl(resource.resource_type, resource.id)) for resource in entries]
    bundle = Bundle(type="searchset", entry=bundle_entries)
    bundle.total = total
    bundle.link = create_pagination_links(offset, count, total, base_url, search_params)
    return jsonify(bundle.dict())

    
    
@fhir_api.route("/fhir/<resource_type>", methods=["POST"])
def create_resource(resource_type):
    if not resource_type in SUPORTED_RESOURCE_TYPES:
        raise UnknownResourceType()
    data = request.json
    resource = ResourceManager().create(resource_type, data)
    return jsonify(resource.dict())


@fhir_api.route("/fhir/<resource_type>/<id>", methods=["GET"])
def get_resource(resource_type, id):
    if not resource_type in SUPORTED_RESOURCE_TYPES:
        raise UnknownResourceType()
    resource = ResourceManager().get(resource_type, id)
    return jsonify(resource.dict())



# @fhir_api.route("/fhir/$provide-prescription", methods=["POST"])
# def provide_prescription():
#     return "provide_prescription"


# @fhir_api.route("/fhir/$cancel-prescription", methods=["POST"])
# def cancel_prescription():
#     return "cancel_prescription"


# @fhir_api.route("/fhir/$provide-dispensation", methods=["POST"])
# def provide_dispensation():
#     return "provide_dispensation"


# @fhir_api.route("/fhir/$cancel-dispensation", methods=["POST"])
# def cancel_dispensation():
#     return "cancel_dispensation"