import requests
import json
import os
import logging
from fhir.resources import FHIRAbstractModel
from requests.exceptions import RequestException

# Import your resource creators
from ressource_creators.medication_creator import MedicationCreator
from ressource_creators.medication_request_creator import MedicationRequestCreator
from ressource_creators.organisation_creator import OrganizationCreator
from ressource_creators.practitioner_creator import PractitionerCreator
from fhir.resources.parameters import Parameters, ParametersParameter

# Initialize logging
logging.basicConfig(level=logging.INFO)

def create_medication_request():
    try:
        medication = MedicationCreator.get_example_medication()
        organization = OrganizationCreator.get_example_farmacy_organization()
        practitioner = PractitionerCreator.get_example_practitioner()


        medication_request = MedicationRequestCreator.create_medication_request(
            prior_prescription_id="12345",
            medication_reference=medication.id,
            patient_reference="Patient/67890",
            dosage_instruction_text="Take one tablet daily",
            substitution_allowed=True
        )

        logging.info(f"MedicationRequest ID: {medication_request.id}")
        logging.info(f"Medication ID: {medication.id}")
        logging.info(f"Organization ID: {organization.id}")
        logging.info(f"Practitioner ID: {practitioner.id}")

        return medication_request
    except Exception as e:
        logging.error(f"Error creating medication request: {e}")
        raise

def fhir_model_to_json(model: FHIRAbstractModel) -> dict:
    return json.loads(model.json())

def create_parameters_resource(medication, organization, practitioner, medication_request):
    parameters = Parameters.construct()
    parameters.parameter = [
        ParametersParameter.construct(name="medication", resource=medication),
        ParametersParameter.construct(name="organization", resource=organization),
        ParametersParameter.construct(name="practitioner", resource=practitioner),
        ParametersParameter.construct(name="medicationRequest", resource=medication_request)
    ]
    return parameters

if __name__ == "__main__":
    try:
        medication_request = create_medication_request()

        # Create the Parameters resource
        parameters_resource = create_parameters_resource(
            medication_request,
            medication_request.dispenseRequest.performer,
            medication_request.requester,
            medication_request
        )

        # Convert the Parameters object to a JSON-serializable dictionary
        fhir_data = fhir_model_to_json(parameters_resource)
        print(json.dumps(fhir_data, indent=2))

        # Define the operation endpoint (adjust as necessary)
        operation_url = os.getenv("FHIR_OPERATION_URL", "http://127.0.0.1:5000/provide-prescription/1234567890")

        # Send the POST request
        response = requests.post(operation_url, json=fhir_data, verify=True)


        # Check if the response was successful
        response.raise_for_status()

        logging.info(f"Status Code: {response.status_code}")
        logging.info(f"Response Body: {response.json()}")
    except RequestException as req_err:
        logging.error(f"HTTP request error: {req_err}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")