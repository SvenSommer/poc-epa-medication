class FHIRValidator:
    def __init__(self):
        pass

    def validate_fhir_data(self, fhir_data, required_types, wrapper_name):
        if 'parameter' not in fhir_data:
            return False

        for param in fhir_data['parameter']:
            if 'part' in param:  
                if param['name'] == wrapper_name:
                    received_types = {part['name'] for part in param['part']}
                    return required_types.issubset(received_types)
            else: 
                if param['name'] in required_types:
                    return True  

        return False