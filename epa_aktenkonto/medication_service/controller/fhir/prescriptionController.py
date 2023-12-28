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


    def handle_provide_prescriptions(self, fhir_data):
        try:
            resources = self.fhir_helper.extract_rx_resources(fhir_data, "RxPrescription")
            for resource in resources:
                self.medication_request_controller.store(resource.get('MedicationRequest'))
                self.medication_controller.store(resource.get('Medication'))
                self.organization_controller.store(resource.get('Organization'))
                self.practitioner_controller.store(resource.get('Practitioner'))

        except Exception as e:
            logging.error(e)
            raise e
        
    def handle_cancel_prescription(self, fhir_data):
        try:
            rx_identifier = self.fhir_helper.extract_value_identifier_by_name(fhir_data, "RxPrescriptionProcessIdentifier")
            logging.info("Canceling prescription with rx_identifier: %s", rx_identifier)
            self.medication_request_controller.update_status(rx_identifier, "cancelled")
            self.medication_dispense_controller.update_status(rx_identifier, "cancelled")
            self.medication_controller.update_status(rx_identifier, "inactive")

        except Exception as e:
            logging.error(e)
            raise e
