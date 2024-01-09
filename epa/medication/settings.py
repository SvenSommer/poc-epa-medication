#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

DB_NAME = os.getenv('DB_NAME', 'fhir')
DB_USER = os.getenv('DB_USER', 'fhir')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'fhir')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')

SUPORTED_RESOURCE_TYPES = ['Medication', 'MedicationRequest', 'MedicationDispense', 'Practitioner', 'PractitionerRole', 'Organization']

