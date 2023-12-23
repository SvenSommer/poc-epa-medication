from controller.fhir.epaFhirRessource import ePAFHIRRessource
from controller.fhir.fhirHelper import FHIRHelper
import logging

class MedicationDispenseController(ePAFHIRRessource):
    def __init__(self, db_reader, db_writer): 
        self.db_reader = db_reader
        self.db_writer = db_writer
        self.fhir_helper = FHIRHelper()

    def get_unique_identifier(self, medication_dispense):
        logging.info("get_unique_identifier")
        logging.info(medication_dispense)
        return self.fhir_helper.get_identifier_by_system(medication_dispense,"MedicationDispense", "https://gematik.de/fhir/epa-medication/sid/epa-medication-dispense-unique-identifier")

    def set_unique_identifier(self, medication_dispense):
        rx_identifier = self.getRxIdentifier(medication_dispense)
        return rx_identifier + "_" + str(medication_dispense["MedicationDispense"]["id"])
       
    
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
            logging.info(f"MedicationDispenses with unique_resource_identifier: '{rx_identifier}' not found")   
            return None

        for medication_dispense in medication_dispenses:
            logging.info(f"Updating MedicationDispense with unique_resource_identifier: '{rx_identifier}'")
            medication_dispense_updated = self.set_new_status(medication_dispense, new_status)
            unique_ressource_identifier = self.get_unique_identifier(medication_dispense_updated)
            self.db_writer.create_or_update_resource("MedicationDispense", medication_dispense_updated, unique_ressource_identifier, rx_identifier)

        return True

    
    def set_new_status(self, medication_dispense, new_status):
        if not isinstance(medication_dispense, tuple) or not medication_dispense:
            logging.error(f"MedicationDispense data is not a tuple or is empty: {medication_dispense}")
            raise ValueError("Invalid format for MedicationDispense data - expected a non-empty tuple")

        medication_dispense_data = medication_dispense[0]
        if not isinstance(medication_dispense_data, dict) or 'MedicationDispense' not in medication_dispense_data:
            logging.error(f"MedicationDispense data is not in expected dictionary format or missing 'MedicationDispense' key: {medication_dispense_data}")
            raise ValueError("MedicationDispense data not found in the expected format")

        nested_medication_dispense_data = medication_dispense_data['MedicationDispense']
        nested_medication_dispense_data["status"] = new_status
        medication_dispense_data['MedicationDispense'] = nested_medication_dispense_data


        # Consider updating meta.versionId and meta.lastUpdated here
        # ...

        return medication_dispense_data
    
    def store(self, medication_dispense):
        rx_identifier = self.getRxIdentifier(medication_dispense)
        unique_ressource_identifier = self.set_unique_identifier(medication_dispense)
        if self.db_reader.find_resource_by_unique_ressource_identifier("MedicationDispense", unique_ressource_identifier):
            raise DuplicateMedicationDispenseError("MedicationDispense already exists")
        self.add_unique_identifer(medication_dispense, unique_ressource_identifier)
        self.db_writer.create_or_update_resource("MedicationDispense", medication_dispense, unique_ressource_identifier, rx_identifier)
        return rx_identifier
    
    def add_unique_identifer(self, medication_dispense, unique_ressource_identifier):
        if 'MedicationDispense' in medication_dispense:
            medication_dispense_data = medication_dispense['MedicationDispense']
            identifier = medication_dispense_data.get('identifier', [])
            identifier.append({
                "system": "https://gematik.de/fhir/epa-medication/sid/epa-medication-dispense-unique-identifier",
                "value": unique_ressource_identifier
            })
            medication_dispense_data['identifier'] = identifier
        else:
            raise ValueError("MedicationDispense data not found in the expected format")

class DuplicateMedicationDispenseError(Exception):
    pass