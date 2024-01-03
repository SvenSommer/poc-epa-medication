import logging
from controller.fhir.fhirHelper import FHIRHelper
from controller.fhir.medicationDispenseController import MedicationDispenseController, MedicationDispenseNotFoundError
from controller.fhir.medicationRequestController import MedicationRequestController
from controller.fhir.medicationController import MedicationController
from controller.fhir.organizationController import OrganizationController

class DispensationController:
    def __init__(self, db_reader, db_writer):
        self.fhir_helper = FHIRHelper()  
        self.medication_dispense_controller = MedicationDispenseController(db_reader, db_writer)
        self.medication_controller = MedicationController(db_reader, db_writer)
        self.organization_controller = OrganizationController(db_writer)
        self.medication_request_controller = MedicationRequestController(db_reader, db_writer)
       

    def handle_provide_dispensations(self, fhir_data):
        try:
            resources = self.fhir_helper.extract_rx_resources(fhir_data, "RxDispensation")
            for resource in resources:
                self.handle_medicationDispense(resource.get('MedicationDispense'))
                self.medication_controller.store(resource.get('Medication'))
                self.organization_controller.store(resource.get('Organization'))

        except Exception as e:
            logging.error(e)
            raise e


    def handle_cancel_dispensation(self, fhir_data):
        try:
            rx_identifier = self.fhir_helper.extract_value_identifier_by_name(fhir_data, "RxPrescriptionProcessIdentifier")
            self.medication_dispense_controller.update_status(rx_identifier, "cancelled")
            self.medication_controller.update_status(rx_identifier, "inactive")

        except Exception as e:
            logging.error(e)
            raise e
        
    def handle_medicationDispense(self, medication_dispense):
        try:
            rx_identifier = self.medication_dispense_controller.getRxIdentifier(medication_dispense)
            medication_request = self.medication_request_controller.find_medicationRequest_by_unique_ressource_identifier(rx_identifier)
            if not medication_request:
                raise MedicationRequestMissingError(f"MedicationRequest with rx-prescription-process-identifier: '{rx_identifier}' not found.")
            try:
                self.medication_dispense_controller.update_status(rx_identifier, "declined")
            except MedicationDispenseNotFoundError as e:
                logging.info("MedicationDispense with rx_identifier: %s not found", rx_identifier)
            self.medication_controller.update_status(rx_identifier, "inactive")
            self.medication_dispense_controller.store(medication_dispense)

        except Exception as e:
            logging.error(e)
            raise e

        

class MedicationRequestMissingError(Exception):
    pass