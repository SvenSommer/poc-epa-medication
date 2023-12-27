from controller.fhir.epaFhirRessource import ePAFHIRRessource
from controller.fhir.fhirHelper import FHIRHelper
class OrganizationController(ePAFHIRRessource):
    def __init__(self, db_writer):
        self.db_writer = db_writer
        self.fhir_helper = FHIRHelper()

    def get_unique_identifier(self, organization):
        identifier =  self.fhir_helper.get_identifier_by_system(
            organization,
            "https://gematik.de/fhir/sid/telematik-id",
        )

        if identifier is None:
            raise ValueError("Organization has no unique identifier")
        
        return identifier
    
    def store(self, organization):
        unique_ressource_identifier = self.get_unique_identifier(organization)
        self.db_writer.create_or_update_resource("Organization", organization, unique_ressource_identifier)
        return unique_ressource_identifier
