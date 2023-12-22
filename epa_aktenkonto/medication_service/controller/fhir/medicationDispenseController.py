from controller.fhir.epaFhirRessource import ePAFHIRRessource
from controller.fhir.fhirHelper import FHIRHelper
import logging

class MedicationDispenseController(ePAFHIRRessource):
    def __init__(self, db_reader, db_writer): 
        self.db_reader = db_reader
        self.db_writer = db_writer
        self.fhir_helper = FHIRHelper()

    def get_unique_identifier(self, medication_dispense):
        return self.fhir_helper.get_identifier_by_system(medication_dispense,"MedicationDispense", "https://gematik.de/fhir/epa-medication/sid/rx-prescription-process-identifier")
        # + "_" + whenHanededOver?!
    
    def getRxIdentifier(self, medication_dispense):
        rx_identifier = self.fhir_helper.extract_first_extension_value(
            medication_dispense, 
            "MedicationDispense",
            "https://gematik.de/fhir/epa-medication/StructureDefinition/rx-prescription-process-identifier-extension"
        )

        if rx_identifier is None:
            raise ValueError("Rx identifier not found in MedicationDispense extension")

        return rx_identifier
    
    def update_status(self, rx_identifier, new_status):
        medication_dispenses = self.db_reader.get_resource_by_rx_identifier("MedicationDispense", rx_identifier)
        if not medication_dispenses:
            logging.info(f"MedicationDispenses with unique_ressource_identifier: '{rx_identifier}' not found")   
            return None
        for medication_dispense in medication_dispenses:
            medication_dispense_tuple = medication_dispense[0]
            if not medication_dispense_tuple or not isinstance(medication_dispense_tuple, tuple) or not medication_dispense_tuple[0]:
                raise ValueError("Invalid format for MedicationDispense data")

            medication_dispense = medication_dispense_tuple[0]

            if 'MedicationDispense' in medication_dispense:
                medication_dispense_data = medication_dispense['MedicationDispense']
                medication_dispense_data["status"] = new_status
            else:
                raise ValueError("MedicationDispense data not found in the expected format")
            
            # Consider updating meta.versionId and meta.lastUpdated here
            # ...

        return medication_dispense
    

