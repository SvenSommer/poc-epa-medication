from controller.fhir.epaFhirRessource import ePAFHIRRessource

class OrganizationController(ePAFHIRRessource):


    def get_unique_identifier(self, organization):
        return self.fhir_helper.get_identifier_by_system(
            organization,
            "Organization",
            "https://gematik.de/fhir/sid/telematik-id",
        )
