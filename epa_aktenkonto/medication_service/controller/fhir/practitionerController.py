from controller.fhir.epaFhirRessource import ePAFHIRRessource
from controller.fhir.fhirHelper import FHIRHelper

class PractitionerController(ePAFHIRRessource):
    def __init__(self):
        self.fhir_helper = FHIRHelper()

    def get_unique_identifier(self, practitioner):
        return self.fhir_helper.get_identifier_by_system(
            practitioner,
            "Practitioner",
            "https://gematik.de/fhir/sid/telematik-id",
        )
    

