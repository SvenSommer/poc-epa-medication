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
    def extract_parameters_by_type(fhir_data, resource_type):
        logging.debug("Extracting parameters by type with resource_type: %s", resource_type)
        if not fhir_data.get("parameter"):
            raise ValueError("No parameters in FHIR data found")

        parameters_of_type = {
            param.get("name"): param.get("resource")
            for param in fhir_data.get("parameter", [])
            if param.get("resource", {}).get("resourceType") == resource_type
        }

        if not parameters_of_type:
            raise ValueError(f"No parameters of type {resource_type} found")

        return parameters_of_type
    
    @staticmethod
    def get_identifier_by_system(fhir_resource, resource_type, system_url):
        logging.debug("Searching for identifier with system URL: %s in resource type: %s", system_url, resource_type)

        # Log the entire FHIR resource (be cautious with large data)
        logging.debug("FHIR resource: %s", json.dumps(fhir_resource, indent=4))

        # Check if the specified resource type is present in the FHIR resource
        if resource_type not in fhir_resource:
            logging.error("FHIR resource does not contain '%s'", resource_type)
            raise ValueError(f"FHIR resource does not contain '{resource_type}'")

        resource_data = fhir_resource[resource_type]

        if "identifier" not in resource_data:
            logging.warning("No 'identifier' field found in the '%s'", resource_type)
            raise ValueError(f"'{resource_type}' does not contain 'identifier' field")

        # Log the number of identifiers found
        identifiers = resource_data.get("identifier", [])
        logging.debug("Number of identifiers in '%s': %d", resource_type, len(identifiers))

        # Loop through all identifiers in the specified resource
        for identifier in identifiers:
            logging.debug("Checking identifier: %s", identifier)

            if identifier.get("system") == system_url:
                logging.debug("Found matching system URL in identifier")
                if 'value' not in identifier or not identifier['value']:
                    logging.error("Identifier with system '%s' found but no value present in '%s'", system_url, resource_type)
                    raise ValueError(f"Identifier with system '{system_url}' found but no value present in '{resource_type}'")
                return identifier['value']

        logging.error("No identifier with system '%s' found in '%s'", system_url, resource_type)
        raise ValueError(f"No identifier with system '{system_url}' found in '{resource_type}'")

    @staticmethod
    def extract_extensions(fhir_resource, resource_type, extension_url=None):
        logging.debug("Extracting extensions from resource type: %s", resource_type)

        # Check if the specified resource type is present in the FHIR resource
        if resource_type not in fhir_resource:
            logging.error("FHIR resource does not contain '%s'", resource_type)
            raise ValueError(f"FHIR resource does not contain '{resource_type}'")

        resource_data = fhir_resource[resource_type]

        # Check if the 'extension' field is present in the resource data
        if "extension" not in resource_data:
            logging.debug("FHIR resource: %s", json.dumps(fhir_resource, indent=4))
            logging.warning("No 'extension' field found in the '%s' resource", resource_type)
            return []

        # Extract all extensions
        all_extensions = resource_data["extension"]
        logging.debug("Found %d extensions in the '%s' resource", len(all_extensions), resource_type)

        # If a specific extension URL is provided, filter extensions by that URL
        if extension_url:
            filtered_extensions = [ext for ext in all_extensions if ext.get("url") == extension_url]
            logging.debug("Found %d extensions with URL: %s in '%s'", len(filtered_extensions), extension_url, resource_type)
            return filtered_extensions

        return all_extensions

    @staticmethod
    def extract_first_extension_value(fhir_resource, resource_type, extension_url):
        logging.debug("Extracting first extension value from resource type: %s with URL: %s", resource_type, extension_url)

        # Check if the specified resource type is present in the FHIR resource
        if resource_type not in fhir_resource:
            logging.error("FHIR resource does not contain '%s'", resource_type)
            raise ValueError(f"FHIR resource does not contain '{resource_type}'")

        resource_data = fhir_resource[resource_type]

        # Check if the 'extension' field is present in the resource data
        if "extension" not in resource_data:
            logging.warning("No 'extension' field found in the '%s' resource", resource_type)
            return None

        # Find the first extension with the specified URL
        for ext in resource_data["extension"]:
            if ext.get("url") == extension_url:
                logging.debug("Found extension with URL: %s", extension_url)
                value_identifier = ext.get("valueIdentifier")
                if value_identifier and 'value' in value_identifier:
                    return value_identifier['value']

        logging.warning("No extension with URL: %s found in '%s', or 'value' field missing", extension_url, resource_type)
        return None