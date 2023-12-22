class FHIRValidator:
    def __init__(self):
        pass
    def validate_fhir_data(self, fhir_data, required_types):
        received_types = {param.get("name") for param in fhir_data.get("parameter", [])}
        return required_types.issubset(received_types)