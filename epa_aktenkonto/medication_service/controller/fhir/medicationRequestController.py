from controller.fhir.epaFhirRessource import ePAFHIRRessource
from controller.fhir.fhirHelper import FHIRHelper

class MedicationRequestController(ePAFHIRRessource):
    def __init__(self, db_reader, db_writer):
        self.db_reader = db_reader
        self.db_writer = db_writer
        self.fhir_helper = FHIRHelper()  

        
    def get_unique_identifier(self, medication_request):
        return self.fhir_helper.get_identifier_by_system(medication_request,"MedicationRequest", "https://gematik.de/fhir/epa-medication/sid/rx-prescription-process-identifier")
    
    def getRxIdentifier(self, medication_request):
        return self.fhir_helper.get_identifier_by_system(medication_request,"MedicationRequest", "https://gematik.de/fhir/epa-medication/sid/rx-prescription-process-identifier")

    def update_status(self, rx_identifier, new_status):
        medication_request = self.db_reader.get_resource_by_unique_ressource_identifier("MedicationRequest", rx_identifier)
        if not medication_request:
            raise ValueError(f"MedicationRequest with unique_ressource_identifier: '{rx_identifier}' not found")
        medication_request_updated = self.set_new_status(medication_request, new_status)
        unique_ressource_identifier = self.get_unique_identifier(medication_request_updated)
        return self.db_writer.create_or_update_resource("MedicationRequest", medication_request_updated, unique_ressource_identifier, rx_identifier)

    def set_new_status(self, medication_requests, new_status):
        medication_request_tuple = medication_requests[0]
        if not medication_request_tuple or not isinstance(medication_request_tuple, tuple) or not medication_request_tuple[0]:
            raise ValueError("Invalid format for MedicationRequest data")

        medication_request = medication_request_tuple[0]

        if 'MedicationRequest' in medication_request:
            medication_request_data = medication_request['MedicationRequest']
            medication_request_data["status"] = new_status
        else:
            raise ValueError("MedicationRequest data not found in the expected format")
        
        # Consider updating meta.versionId and meta.lastUpdated here
        # ...

        return medication_request

    def store(self, medication_request):
        rx_identifier =  self.getRxIdentifier(medication_request)
        unique_ressource_identifier = self.get_unique_identifier(medication_request)
        if self.db_reader.find_resource_by_unique_ressource_identifier("MedicationRequest", unique_ressource_identifier):
            raise DuplicateMedicationRequestError("MedicationRequest already exists")
        self.db_writer.create_or_update_resource("MedicationRequest", medication_request, unique_ressource_identifier, rx_identifier)
        return rx_identifier
    
class DuplicateMedicationRequestError(Exception):
    pass