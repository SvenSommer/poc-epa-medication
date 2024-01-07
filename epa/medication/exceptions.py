#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fhir.resources.operationoutcome import OperationOutcome


class FHIRException(Exception):

    @property
    def status_code(self):
        return "404"

    @property
    def data(self):
        return {}
    
    @property
    def operation_outcome(self):
        return OperationOutcome.parse_raw(self.data).dict()
    

class UnknownResourceType(FHIRException):

    @property
    def status_code(self):
        return "404"

    @property
    def data(self):
        return """
        {
            "resourceType": "OperationOutcome",
            "issue": [
                {
                "severity": "error",
                "code": "processing",
                "details": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/operation-outcome",
                            "code": "MSG_UNKNOWN_TYPE"
                        }
                    ]
                },
                "diagnostics": "Unknown resource type"
                }
            ]
        }
        """


class ResourceIdFail(FHIRException):
    
    @property
    def status_code(self):
        return "404"
    
    @property
    def data(self):
        return """
        {
            "resourceType": "OperationOutcome",
            "issue": [
                {
                "severity": "error",
                "code": "processing",
                "details": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/operation-outcome",
                            "code": "MSG_RESOURCE_ID_FAIL"
                        }
                    ]
                },
                "diagnostics": "Resource is not known"
                }
            ]
        }
        """
