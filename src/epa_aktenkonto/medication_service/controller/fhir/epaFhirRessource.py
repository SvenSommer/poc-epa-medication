from controller.fhir.fhirHelper import FHIRHelper
import hashlib

class ePAFHIRRessource:
    def __init__(self):
        self.fhir_helper = FHIRHelper()

    def get_unique_identifier(self, ressource):
        pass

    def store(self, ressource):
        pass

    def _generate_hash(self, input_str):
        return hashlib.sha256(input_str.encode()).hexdigest()