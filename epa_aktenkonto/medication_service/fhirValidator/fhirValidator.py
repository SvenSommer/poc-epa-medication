class FHIRValidator:
    def __init__(self):
        pass
    def validate_fhir_data(self, fhir_data, required_types):
        if 'parameter' not in fhir_data:
            return False
         
        for param in fhir_data['parameter']:
            if param['name'] == 'RxPrescription':
                received_types = {part['name'] for part in param['part']}
                return required_types.issubset(received_types)
        
        return False
    
    

        