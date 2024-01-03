import json
import logging
from controller.fhir.epaFhirRessource import ePAFHIRRessource
from controller.fhir.fhirHelper import FHIRHelper
from controller.fhir.provenanceController import ProvenanceController

class MedicationController(ePAFHIRRessource):
    def __init__(self, db_reader, db_writer):
        self.db_reader = db_reader
        self.db_writer = db_writer
        self.fhir_helper = FHIRHelper()
        self.provenance_controller = ProvenanceController(db_reader, db_writer)

    def getRxIdentifier(self, medication):
        rx_identifier = self.fhir_helper.extract_first_extension_value(
            medication, 
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
        #TODO: remove all identifiers before hashing the whole resource
        return self._generate_hash(json.dumps(medication))


    def _extract_pzn(self, medication):
        medication_data = medication.get("Medication", {})
        coding = medication_data.get("code", {}).get("coding", [])
        for code in coding:
            if code.get("system") == "http://fhir.de/CodeSystem/ifa/pzn":

                return code.get("code")
        return None
    
    def find_medications_by_unique_ressource_identififier(self, unique_ressource_identifier):
        return self.db_reader.get_resource_by_unique_ressource_identifier("Medication", unique_ressource_identifier)


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
            if isinstance(medication, tuple) and isinstance(medication[0], dict):
                medication = medication[0]
            medication = self.set_new_status(medication, new_status)
            unique_ressource_identifier = self.get_unique_identifier(medication)
            self.db_writer.create_or_update_resource("Medication", medication, unique_ressource_identifier, rx_identifier)

    def set_new_status(self, medication, new_status):
        if not isinstance(medication, dict):
            raise ValueError("Invalid format for Medication data")
            
        medication["status"] = new_status  # Directly assigning the new_status to the medication

        # Optionally update meta.versionId and meta.lastUpdated here
        # ...

        return medication

    
    def store(self, new_medication):
        rx_identifier = self.getRxIdentifier(new_medication)
        unique_resource_identifier = self.get_unique_identifier(new_medication)

        existing_medications = self.find_medications_by_unique_ressource_identififier(unique_resource_identifier)
        if existing_medications:
            new_medication_id = new_medication.get("Medication", {}).get("id")
            existing_medication_id = existing_medications[0][0].get("Medication", {}).get("id")
            provenance = self.provenance_controller.create(existing_medication_id, new_medication_id)
            self.db_writer.create_or_update_resource("Provenance", provenance, new_medication_id, rx_identifier)
           # self.set_new_status(existing_medications[0], 'active')
           # self.db_writer.create_or_update_resource("Medication", existing_medications[0][0], unique_resource_identifier, rx_identifier)
        else:
            self.add_unique_identifer(new_medication, unique_resource_identifier)
            self.db_writer.create_or_update_resource("Medication", new_medication, unique_resource_identifier, rx_identifier)
        return rx_identifier

    def add_unique_identifer(self, medication, unique_ressource_identifier):
        try:
            identifier = medication.get('identifier', [])
            identifier.append({
                "system": "https://gematik.de/fhir/epa-medication/sid/epa-medication-unique-identifier",
                "value": unique_ressource_identifier
            })
            medication['identifier'] = identifier
        except Exception as e:
            raise ValueError("Medication data not found in the expected format, error: " + str(e))

