from controller.fhir.epaFhirRessource import ePAFHIRRessource

class MedicationRequestController(ePAFHIRRessource):
    def get_unique_identifier(self, medication_request):
        return self.fhir_helper.get_identifier_by_system(medication_request,"MedicationRequest", "https://gematik.de/fhir/epa-medication/sid/rx-prescription-process-identifier")
    
    def getRxIdentifier(self, medication_request):
        return self.fhir_helper.get_identifier_by_system(medication_request,"MedicationRequest", "https://gematik.de/fhir/epa-medication/sid/rx-prescription-process-identifier")
