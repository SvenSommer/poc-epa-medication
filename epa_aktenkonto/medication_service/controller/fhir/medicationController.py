import json
import logging
from controller.fhir.epaFhirRessource import ePAFHIRRessource
from controller.fhir.fhirHelper import FHIRHelper

class MedicationController(ePAFHIRRessource):
    def __init__(self, db_reader, db_writer):
        self.db_reader = db_reader
        self.db_writer = db_writer
        self.fhir_helper = FHIRHelper()

    def getRxIdentifier(self, medication):
        rx_identifier = self.fhir_helper.extract_first_extension_value(
            medication, 
            "Medication",
            "https://gematik.de/fhir/epa-medication/StructureDefinition/rx-prescription-process-identifier-extension"
        )

        if rx_identifier is None:
            raise ValueError("Rx identifier not found in Medication extension")

        return rx_identifier
    
    def get_unique_identifier(self, medication):
        pzn = self._extract_pzn(medication)
        ingredients = self._extract_ingredients(medication)

        # Fall 1: PZN angegeben
        if pzn:
            # Fall 3: Kombination von PZN und Wirkstoffen
            if ingredients:
                combined_str = f"{pzn},{''.join(sorted(ingredients))}"
                return self._generate_hash(combined_str)
            # Nur PZN vorhanden
            return self._generate_hash(pzn)

        # Fall 2: Nur Wirkstoffe angegeben
        if ingredients:
            ingredients_str = ",".join(sorted(ingredients))
            return self._generate_hash(ingredients_str)

        # Fall 4: Freitext angegeben
        free_text = medication.get("code", {}).get("text")
        if free_text:
            return self._generate_hash(free_text)
        
        logging.error("Medication has no unique identifier. Will hash the whole resource")
        return self._generate_hash(json.dumps(medication))


    def _extract_pzn(self, medication):
        medication_data = medication.get("Medication", {})
        coding = medication_data.get("code", {}).get("coding", [])
        for code in coding:
            if code.get("system") == "http://fhir.de/CodeSystem/ifa/pzn":

                return code.get("code")
        return None


    def _extract_ingredients(self, medication):
        ingredients = medication.get("ingredient", [])
        return [
            f"{ingredient['item'].get('coding', [{}])[0].get('code')}{ingredient.get('strength')}"
            for ingredient in ingredients if 'item' in ingredient and 'coding' in ingredient['item']
        ]
    
    def update_status(self, rx_identifier, new_status):
        medications = self.db_reader.get_resource_by_rx_identifier("Medication", rx_identifier)
        if not medications:
            raise ValueError(f"Medication with RxPrescriptionProcessIdentifier: '{rx_identifier}' not found")   
        for medication in medications:
            medication = self.set_new_status(medication, new_status)
            unique_ressource_identifier = self.get_unique_identifier(medication)
            self.db_writer.create_or_update_resource("Medication", medication, unique_ressource_identifier, rx_identifier)

    def set_new_status(self, medication, new_status):
        if isinstance(medication, tuple) and isinstance(medication[0], dict):
            medication_data = medication[0]
        else:
            raise ValueError("Invalid format for Medication data")

        if 'Medication' in medication_data:
            medication_data['Medication']["status"] = new_status
        else:
            raise ValueError("Medication data not found in the expected format")

        # Optionally update meta.versionId and meta.lastUpdated here
        # ...

        return medication_data

    
    def store(self, medication):
        rx_identifier = self.getRxIdentifier(medication)
        logging.info("Storing Medication with rx_identifier: %s", rx_identifier)
        unique_ressource_identifier = self.get_unique_identifier(medication)

        self.add_unique_identifer(medication, unique_ressource_identifier)

        self.db_writer.create_or_update_resource("Medication", medication, unique_ressource_identifier, rx_identifier)
        return rx_identifier

    def add_unique_identifer(self, medication, unique_ressource_identifier):
        if 'Medication' in medication:
            medication_data = medication['Medication']
            identifier = medication_data.get('identifier', [])
            identifier.append({
                "system": "https://gematik.de/fhir/epa-medication/sid/epa-medication-unique-identifier",
                "value": unique_ressource_identifier
            })
            medication_data['identifier'] = identifier
        else:
            raise ValueError("Medication data not found in the expected format")

