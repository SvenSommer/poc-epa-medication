import logging
import json

class FHIRHelper:
    @staticmethod
    def extract_parameters(fhir_data, required_params):
        logging.debug("Extracting parameters with required_params: %s", required_params)
        if not fhir_data.get("parameter"):
            raise ValueError("No parameters in FHIR data found")
        parameters = {
            param.get("name"): param.get("resource")
            for param in fhir_data.get("parameter", [])
        }
        if not all(param in parameters for param in required_params):
            raise ValueError("Required parameters not found")
        return parameters

  
    @staticmethod
    def extract_rx_resources(fhir_data, wrapper_name="RxPrescription"):
        logging.debug("Extracting RxPrescription resources from FHIR data.")
        
        # Validate the presence of 'parameter' in data
        if 'parameter' not in fhir_data:
            raise ValueError("No parameters in FHIR data found")

        rx_resources = [
            param
            for param in fhir_data.get('parameter', [])
            if param.get('name') == wrapper_name
        ]
        
        if not rx_resources:
            logging.debug("FHIR data: %s", json.dumps(fhir_data, indent=4))
            raise ValueError(f"No {wrapper_name} parameters found")

        extracted_rx_resources = []
        for rx_resource in rx_resources:
            resources = {
                part['name']: part['resource']
                for part in rx_resource.get('part', []) if 'resource' in part
            }
            extracted_rx_resources.append(resources)

        return extracted_rx_resources

    @staticmethod
    def extract_value_identifier_by_name(fhir_data, name):
        logging.debug("Extracting value identifier by name: %s", name)
        if not fhir_data.get("parameter"):
            raise ValueError("No parameters in FHIR data found")

        for param in fhir_data.get("parameter", []):
            if param.get("name") == name and "valueIdentifier" in param:
                return param["valueIdentifier"].get("value")
            
        logging.debug("FHIR data: %s", json.dumps(fhir_data, indent=4))
        raise ValueError(f"No value identifier with name {name} found")

        
    @staticmethod
    def get_identifier_by_system(resource_data, system_url):
        logging.debug("Searching for identifier with system URL: %s", system_url)

        if "identifier" not in resource_data:
            raise ValueError(f"Resource data does not contain 'identifier' field")

        identifiers = resource_data.get("identifier", [])
        for identifier in identifiers:
            if identifier.get("system") == system_url:
                if 'value' not in identifier or not identifier['value']:
                    raise ValueError(f"Identifier with system '{system_url}' found but no value present")
                return identifier['value']

        raise ValueError(f"No identifier with system '{system_url}' found")
    
    @staticmethod
    def extract_extensions(resource_data, extension_url=None):
        if "extension" not in resource_data:
            logging.debug("FHIR resource: %s", json.dumps(resource_data, indent=4))
            logging.warning("Resource data does not contain 'extension' field")
            return []
        
        all_extensions = resource_data["extension"]
        logging.debug("Found %d extensions in the resource data", len(all_extensions))

        if extension_url:
            filtered_extensions = [ext for ext in all_extensions if ext.get("url") == extension_url]
            logging.debug("Found %d extensions with URL: %s", len(filtered_extensions), extension_url)
            return filtered_extensions

        return all_extensions

    @staticmethod
    def extract_first_extension_value(resource_data, extension_url):
        if "extension" not in resource_data:
            logging.warning("No 'extension' field found in the resource data")
            return None

        for ext in resource_data["extension"]:
            if ext.get("url") == extension_url:
                logging.debug("Found extension with URL: %s", extension_url)
                value_identifier = ext.get("valueIdentifier")
                if value_identifier and 'value' in value_identifier:
                    return value_identifier['value']

        logging.warning("No extension with URL: %s found, or 'value' field missing", extension_url)
        return None