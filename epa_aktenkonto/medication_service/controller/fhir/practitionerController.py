from controller.fhir.epaFhirRessource import ePAFHIRRessource
from controller.fhir.fhirHelper import FHIRHelper

class PractitionerController(ePAFHIRRessource):
    def __init__(self, db_writer):
        self.db_writer = db_writer
        self.fhir_helper = FHIRHelper()

    def get_unique_identifier(self, practitioner):
        identifer =  self.fhir_helper.get_identifier_by_system(
            practitioner,
            "Practitioner",
            "https://gematik.de/fhir/sid/telematik-id",
        )

        if identifer is None:
            raise ValueError("Practitioner has no unique identifier")
        
        return identifer
    
    def store(self, practitioner):
        unique_ressource_identifier = self.get_unique_identifier(practitioner)            
        self.db_writer.create_or_update_resource("Practitioner", practitioner, unique_ressource_identifier)
        return unique_ressource_identifier
    

