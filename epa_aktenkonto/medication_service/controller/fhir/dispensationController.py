import logging
from controller.fhir.fhirHelper import FHIRHelper
from controller.fhir.medicationDispenseController import MedicationDispenseController
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
       

    def handle_provide_dispensation(self, fhir_data):
        try:
            self.handle_medicationDispense(fhir_data)
            self.store_medication(fhir_data)
            self.store_Organization(fhir_data)

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
        
    def handle_medicationDispense(self, fhir_data):
        medication_dispense = self.fhir_helper.extract_parameters_by_type(fhir_data, "MedicationDispense")
        rx_identifier = self.medication_dispense_controller.getRxIdentifier(medication_dispense)
        medication_request = self.medication_request_controller.find_medicationRequest_by_unique_ressource_identifier(rx_identifier)
        if not medication_request:
            raise MedicationRequestMissingError(f"MedicationRequest with rx-prescription-process-identifier: '{rx_identifier}' not found.")
        self.medication_dispense_controller.update_status(rx_identifier, "declined")
        self.medication_controller.update_status(rx_identifier, "inactive")
        self.medication_dispense_controller.store(medication_dispense)
        
    def store_medication(self, fhir_data):
        medication = self.fhir_helper.extract_parameters_by_type(fhir_data, "Medication")
        return self.medication_controller.store(medication)
    
    def store_Organization(self, fhir_data):
        organization = self.fhir_helper.extract_parameters_by_type(fhir_data, "Organization")
        return self.organization_controller.store(organization)
    

class MedicationRequestMissingError(Exception):
    pass