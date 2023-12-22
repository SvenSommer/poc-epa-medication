import logging
from controller.fhir.fhirHelper import FHIRHelper
from controller.fhir.medicationController import MedicationController
from controller.fhir.medicationRequestController import MedicationRequestController
from controller.fhir.organizationController import OrganizationController
from controller.fhir.practitionerController import PractitionerController

class PrescriptionController:
    def __init__(self, db_reader, db_writer):
        self.sb_reader = db_reader
        self.db_writer = db_writer
        self.fhir_helper = FHIRHelper()  
        self.medication_request_controller = MedicationRequestController()
        self.medication_controller = MedicationController()
        self.organization_controller = OrganizationController()
        self.practitioner_controller = PractitionerController()


    def handle_prescription(self, fhir_data):
        try:
            request_rx_identifier = self._handle_medicationRequest(fhir_data)
            medication_rx_identifier = self._handle_medication(fhir_data)
            if request_rx_identifier != medication_rx_identifier:
                raise DifferentRxPrescriptionProcessIdentifierError("Request and Medication have different rx_identifier")

            self._handle_Organization(fhir_data)
            
            self.db_writer.close()
        except Exception as e:
            logging.error(e)
            raise e

    def _handle_medicationRequest(self, fhir_data):
        medication_request = self.fhir_helper.extract_parameters_by_type(fhir_data, "MedicationRequest")
        rx_identifier =  self.medication_request_controller.getRxIdentifier(medication_request)
        unique_ressource_identifier = self.medication_request_controller.get_unique_identifier(medication_request)
        if self.sb_reader.find_resource_by_unique_ressource_identifier("MedicationRequest", unique_ressource_identifier):
            raise DuplicateMedicationRequestError("MedicationRequest already exists")
        self.db_writer.create_or_update_resource("MedicationRequest", medication_request, unique_ressource_identifier, rx_identifier)
        return rx_identifier

    def _handle_medication(self, fhir_data):
        medication = self.fhir_helper.extract_parameters_by_type(fhir_data, "Medication")
        rx_identifier = self.medication_controller.getRxIdentifier(medication)
        unique_ressource_identifier = self.medication_controller.get_unique_identifier(medication)

        self.db_writer.create_or_update_resource("Medication", medication, unique_ressource_identifier, rx_identifier)
        return rx_identifier
    
    def _handle_Organization(self, fhir_data):
        organization = self.fhir_helper.extract_parameters_by_type(fhir_data, "Organization")
        unique_ressource_identifier = self.organization_controller.get_unique_identifier(organization)
        if unique_ressource_identifier is None:
            raise ValueError("Organization has no unique identifier")
        self.db_writer.create_or_update_resource("Organization", organization, unique_ressource_identifier)
        return unique_ressource_identifier
    
    def _handle_Practitioner(self, fhir_data):
        practitioner = self.fhir_helper.extract_parameters_by_type(fhir_data, "Practitioner")
        unique_ressource_identifier = self.practitioner_controller.get_unique_identifier(practitioner)
        if unique_ressource_identifier is None:
            raise ValueError("Practitioner has no unique identifier")
        self.db_writer.create_or_update_resource("Practitioner", practitioner, unique_ressource_identifier)
        return unique_ressource_identifier



class DuplicateMedicationRequestError(Exception):
    pass

class DifferentRxPrescriptionProcessIdentifierError(Exception):
    pass