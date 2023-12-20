import json
import os
import logging
import requests
from requests.exceptions import RequestException
from fhir.resources import FHIRAbstractModel
from fhir.resources.parameters import Parameters, ParametersParameter

# Import your resource creators
from fhir_creators.medication_creator import MedicationCreator
from fhir_creators.medication_request_creator import MedicationRequestCreator
from fhir_creators.organisation_creator import OrganizationCreator
from fhir_creators.practitioner_creator import PractitionerCreator
from fhir_creators.medication_dispense_creator import MedicationDispenseCreator

# Initialize logging
logging.basicConfig(level=logging.INFO)

# FHIR Server Constants
FHIR_OPERATION_URL = os.getenv("FHIR_OPERATION_URL", "http://127.0.0.1:5000")

def create_medication_request(rxPrescriptionProcessIdentifier):
    try:
        medication = MedicationCreator.get_example_medication()
        organization = OrganizationCreator.get_example_farmacy_organization()
        practitioner = PractitionerCreator.get_example_practitioner()
        medication_request = MedicationRequestCreator.create_medication_request(
            medication.id, rxPrescriptionProcessIdentifier, "Patient/67890", "Take one tablet daily", True
        )

        params = Parameters.construct()
        params.parameter = [
            ParametersParameter.construct(name="Medication", resource=medication),
            ParametersParameter.construct(name="Organization", resource=organization),
            ParametersParameter.construct(name="Practitioner", resource=practitioner),
            ParametersParameter.construct(name="MedicationRequest", resource=medication_request),
        ]

        return params
    except Exception as e:
        logging.error(f"Error in create_medication_request: {e}")
        raise

def send_prescription(params_resource):
    endpoint = f"/$provide-prescription"
    fhir_data = fhir_model_to_json(params_resource)
    try:
        response = requests.post(f"{FHIR_OPERATION_URL}{endpoint}", json=fhir_data, verify=True)
        response.raise_for_status()
        logging.info(f"Response from {endpoint}: {response.json()}")
    except RequestException as err:
        logging.error(f"HTTP request error in send_prescription: {err}")
    except Exception as e:
        logging.error(f"Error in send_prescription: {e}")

def cancel_prescription(rxPrescriptionProcessIdentifier):
    payload = {
        "resourceType": "Parameters",
        "parameter": [{"name": "RxPrescriptionProcessIdentifier", "valueIdentifier": {"value": rxPrescriptionProcessIdentifier}}],
    }
    try:
        response = requests.post(
            f"{FHIR_OPERATION_URL}/$cancel-prescription", json=payload, verify=True
        )
        response.raise_for_status()
        logging.info(f"Cancel Prescription Response: {response.json()}")
    except RequestException as err:
        logging.error(f"HTTP request error in cancel_prescription: {err}")
    except Exception as e:
        logging.error(f"Error in cancel_prescription: {e}")

def create_medication_dispense(rxPrescriptionProcessIdentifier, when_handed_over):
    try:
        medication = MedicationCreator.get_example_medication()
        organization = OrganizationCreator.get_example_farmacy_organization()
        medication_dispense = MedicationDispenseCreator.create_medication_dispense(
            rxPrescriptionProcessIdentifier, medication.id, "Patient/67890", organization.id, "MedicationRequest/123", when_handed_over, "Take one tablet daily", True
        )

        params = Parameters.construct()
        params.parameter = [
            ParametersParameter.construct(name="Medication", resource=medication),
            ParametersParameter.construct(name="Organization", resource=organization),
            ParametersParameter.construct(name="MedicationDispense", resource=medication_dispense),
        ]

        return params
    except Exception as e:
        logging.error(f"Error in create_medication_dispense: {e}")
        raise

def send_dispensation(params_resource):
    endpoint = f"/$provide-dispensation"
    fhir_data = fhir_model_to_json(params_resource)
    try:
        response = requests.post(f"{FHIR_OPERATION_URL}{endpoint}", json=fhir_data, verify=True)
        response.raise_for_status()
        logging.info(f"Response from {endpoint}: {response.json()}")
    except RequestException as err:
        logging.error(f"HTTP request error in send_dispense: {err}")
    except Exception as e:
        logging.error(f"Error in send_dispense: {e}")

def cancel_dispensation(rxPrescriptionProcessIdentifier):
    payload = {
        "resourceType": "Parameters",
        "parameter": [{"name": "RxPrescriptionProcessIdentifier", "valueIdentifier": {"value": rxPrescriptionProcessIdentifier}}],
    }
    try:
        response = requests.post(
            f"{FHIR_OPERATION_URL}/$cancel-dispensation", json=payload, verify=True
        )
        response.raise_for_status()
        logging.info(f"Cancel Dispensation Response: {response.json()}")
    except RequestException as err:
        logging.error(f"HTTP request error in cancel_dispensation: {err}")
    except Exception as e:
        logging.error(f"Error in cancel_dispensation: {e}")

def fhir_model_to_json(model: FHIRAbstractModel) -> dict:
    return json.loads(model.json())



if __name__ == "__main__":
    try:
        rxPrescriptionProcessIdentifier = "160.768.272.480.500_20231220"
    
        prescription_resources = create_medication_request(rxPrescriptionProcessIdentifier)
        send_prescription(prescription_resources)
        cancel_prescription(rxPrescriptionProcessIdentifier)

        dispense_resources = create_medication_dispense(rxPrescriptionProcessIdentifier, "2023-12-20T18:23:00+01:00")
        send_dispensation(dispense_resources)
        cancel_dispensation(rxPrescriptionProcessIdentifier)
    except Exception as e:
        logging.error(f"Main execution error: {e}")
