from controller.fhir.epaFhirRessource import ePAFHIRRessource
from controller.fhir.fhirHelper import FHIRHelper

import logging

class MedicationRequestController(ePAFHIRRessource):
    def __init__(self, db_reader, db_writer):
        self.db_reader = db_reader
        self.db_writer = db_writer
        self.fhir_helper = FHIRHelper()  

        
    def get_unique_identifier(self, medication_request):
        return self.fhir_helper.get_identifier_by_system(medication_request, "https://gematik.de/fhir/epa-medication/sid/rx-prescription-process-identifier")
    
    def getRxIdentifier(self, medication_request):
        return self.fhir_helper.get_identifier_by_system(medication_request, "https://gematik.de/fhir/epa-medication/sid/rx-prescription-process-identifier")

    def update_status(self, rx_identifier, new_status):
        medication_request = self.find_medicationRequest_by_unique_ressource_identifier(rx_identifier)
        if not medication_request:
            raise MedicationRequestNotFoundError(f"MedicationRequest with unique_ressource_identifier: '{rx_identifier}' not found")
        medication_request_updated = self.set_new_status(medication_request, new_status)
        unique_ressource_identifier = self.get_unique_identifier(medication_request_updated)
        return self.db_writer.create_or_update_resource("MedicationRequest", medication_request_updated, unique_ressource_identifier, rx_identifier)

    def set_new_status(self, medication_requests, new_status):
        logging.info("Setting new status for medication_request: %s", medication_requests)
        for medication_request in medication_requests:
            try:
                logging.info("Setting new status for medication_request: %s", medication_request)

                if isinstance(medication_request, tuple):
                    medication_request_data = medication_request[0]
                else:
                    medication_request_data = medication_request

                medication_request_data["status"] = new_status

                # Consider updating meta.versionId and meta.lastUpdated here
                # ...

            except KeyError:
                raise ValueError("MedicationRequest data not found in the expected format")

        return medication_request_data
    
    def find_medicationRequest_by_unique_ressource_identifier(self, unique_ressource_identifier):
        return self.db_reader.get_resource_by_unique_ressource_identifier("MedicationRequest", unique_ressource_identifier)

    def store(self, medication_request):
        rx_identifier =  self.getRxIdentifier(medication_request)
        unique_ressource_identifier = self.get_unique_identifier(medication_request)
        if self.find_medicationRequest_by_unique_ressource_identifier(unique_ressource_identifier):
            raise DuplicateMedicationRequestError("MedicationRequest already exists")
        self.db_writer.create_or_update_resource("MedicationRequest", medication_request, unique_ressource_identifier, rx_identifier)
        return rx_identifier
    
class DuplicateMedicationRequestError(Exception):
    pass

class MedicationRequestNotFoundError(Exception):
    pass