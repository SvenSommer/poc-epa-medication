#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import uuid

from datetime import datetime
from flask import Blueprint, request, jsonify

from settings import SUPORTED_RESOURCE_TYPES
from models.bundles import SearchSetBundleModel
from models.resource import ResourceModel
from exceptions import FHIRException, UnknownResourceType

logging.basicConfig(level=logging.INFO)

fhir_api = Blueprint('fhir_api', __name__)


@fhir_api.errorhandler(FHIRException)
def handle_fhir_error(error):
    return jsonify(error.operation_outcome), error.status_code


@fhir_api.route("/fhir/<resource_type>", methods=["GET"])
def search_resource(resource_type):
    if not resource_type in SUPORTED_RESOURCE_TYPES:
        raise UnknownResourceType()
    # Paginationsparameter
    offset = int(request.args.get('_offset', 0))
    count = int(request.args.get('_count', 25))

    search_params = {}

    model = SearchSetBundleModel.manager.search(resource_type, offset=offset, count=count)
    model.base_url = f"/fhir/{resource_type}"

    return jsonify(model.dict())

    
@fhir_api.route("/fhir/<resource_type>", methods=["POST"])
def create_resource(resource_type):
    if not resource_type in SUPORTED_RESOURCE_TYPES:
        raise UnknownResourceType()
    data = request.json
    model = ResourceModel(res_type=resource_type, data=data)
    model.save()
    return jsonify(model.dict())


@fhir_api.route("/fhir/<resource_type>/<id>", methods=["GET"])
def get_resource(resource_type, id):
    if not resource_type in SUPORTED_RESOURCE_TYPES:
        raise UnknownResourceType()
    model = ResourceModel.manager.get(res_type=resource_type, id=id)
    return jsonify(model.dict())


# @fhir_api.route("/fhir/$provide-prescription", methods=["POST"])
# def provide_prescription():
#     data = request.json
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