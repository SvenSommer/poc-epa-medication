import logging
from controller.fhir.fhirHelper import FHIRHelper
from controller.fhir.medicationController import MedicationController
from controller.fhir.medicationRequestController import MedicationRequestController
from controller.fhir.organizationController import OrganizationController
from controller.fhir.practitionerController import PractitionerController
from controller.fhir.medicationDispenseController import MedicationDispenseController

class PrescriptionController:
    def __init__(self, db_reader, db_writer):
        self.fhir_helper = FHIRHelper()  
        self.medication_request_controller = MedicationRequestController(db_reader, db_writer)
        self.medication_controller = MedicationController(db_reader, db_writer)
        self.organization_controller = OrganizationController(db_writer)
        self.practitioner_controller = PractitionerController(db_writer)
        self.medication_dispense_controller = MedicationDispenseController(db_reader, db_writer)


    def handle_provide_prescription(self, fhir_data):
        try:
            self._store_medicationRequest(fhir_data)
            self._store_medication(fhir_data)
            self._store_Organization(fhir_data)
            self._store_Practitioner(fhir_data)

        except Exception as e:
            logging.error(e)
            raise e
        
    def handle_cancel_prescription(self, fhir_data):
        try:
            rx_identifier = self.fhir_helper.extract_value_identifier_by_name(fhir_data, "RxPrescriptionProcessIdentifier")
            self.medication_request_controller.update_status(rx_identifier, "cancelled")
            self.medication_dispense_controller.update_status(rx_identifier, "cancelled")
            self.medication_controller.update_status(rx_identifier, "incative")

        except Exception as e:
            logging.error(e)
            raise e


    def _store_medicationRequest(self, fhir_data):
        medication_request = self.fhir_helper.extract_parameters_by_type(fhir_data, "MedicationRequest")
        return self.medication_request_controller.store(medication_request)

    def _store_medication(self, fhir_data):
        medication = self.fhir_helper.extract_parameters_by_type(fhir_data, "Medication")
        return self.medication_controller.store(medication)

    def _store_Organization(self, fhir_data):
        organization = self.fhir_helper.extract_parameters_by_type(fhir_data, "Organization")
        return self.organization_controller.store(organization)

    def _store_Practitioner(self, fhir_data):
        practitioner = self.fhir_helper.extract_parameters_by_type(fhir_data, "Practitioner")
        return self.practitioner_controller.store(practitioner)