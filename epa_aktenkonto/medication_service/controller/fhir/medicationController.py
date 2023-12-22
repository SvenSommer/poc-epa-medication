import hashlib
import json
import logging
from controller.fhir.epaFhirRessource import ePAFHIRRessource

class MedicationController(ePAFHIRRessource):
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
        
        logging.info("FHIR resource: %s", json.dumps(medication, indent=4))
        raise ValueError("Medication has no unique identifier")


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
