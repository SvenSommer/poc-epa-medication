import logging
from controller.fhir.fhirHelper import FHIRHelper
from controller.fhir.medicationController import MedicationController
from controller.fhir.medicationDispenseController import MedicationDispenseController
from controller.fhir.organizationController import OrganizationController
from controller.fhir.practitionerController import PractitionerController

class DispensationController:
    def __init__(self, db_reader, db_writer):
        self.db_reader = db_reader
        self.db_writer = db_writer
        self.fhir_helper = FHIRHelper()  
        self.medication_dispense_controller = MedicationDispenseController()
        self.medication_controller = MedicationController()
        self.organization_controller = OrganizationController()
        self.practitioner_controller = PractitionerController()

    def handle_provide_dispensation(self, fhir_data):
        try:
            request_rx_identifier = self._handle_medicationDispense(fhir_data)
            medication_rx_identifier = self._store_medication(fhir_data)

            self._store_Organization(fhir_data)
            self._store_Practitioner(fhir_data)

        except Exception as e:
            logging.error(e)
            raise e