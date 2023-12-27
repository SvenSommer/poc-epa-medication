from flask import Flask, request, render_template, jsonify
import json
import os
import logging
import requests
from datetime import datetime
from tzlocal import get_localzone
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

app = Flask(__name__)
# FHIR Server Constants
FHIR_OPERATION_URL = os.getenv("FHIR_OPERATION_URL", "http://127.0.0.1:5000")

def create_medication_request(rxPrescriptionProcessIdentifier):
    try:
        medication = MedicationCreator.get_example_medication_ingredient(rxPrescriptionProcessIdentifier)
        organization = OrganizationCreator.get_example_farmacy_organization()
        practitioner = PractitionerCreator.get_example_practitioner()
        medication_request = MedicationRequestCreator.create_medication_request(
            medication.id, 
            rxPrescriptionProcessIdentifier,
            "Patient/67890", 
            datetime.now(get_localzone()).replace(microsecond=0).isoformat(),
            "Take one tablet daily", 
            True
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

    return response.json()

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
    return response.json()

def create_medication_dispense(rxPrescriptionProcessIdentifier, when_handed_over):
    try:
        medication = MedicationCreator.get_example_medication_pzn(rxPrescriptionProcessIdentifier)
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
    
    return response.json()

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

    return response.json()

def fhir_model_to_json(model: FHIRAbstractModel) -> dict:
    return json.loads(model.json())

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/control", methods=["GET"])
def control():
    return render_template("control.html")

@app.route('/send_prescription', methods=['POST'])
def api_send_prescription():
    try:
        rx_prescription_process_identifier = request.json.get('rxPrescriptionProcessIdentifier', '')
        if not rx_prescription_process_identifier:
            return jsonify({"error": "Missing rxPrescriptionProcessIdentifier"}), 400
        prescription_resources = create_medication_request(rx_prescription_process_identifier)
        return send_prescription(prescription_resources)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/cancel_prescription', methods=['POST'])
def api_cancel_prescription():
    rx_prescription_process_identifier = request.json.get('rxPrescriptionProcessIdentifier', '')
    if not rx_prescription_process_identifier:
        return jsonify({"error": "Missing rxPrescriptionProcessIdentifier"}), 400
    try:
        return cancel_prescription(rx_prescription_process_identifier)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/send_dispensation', methods=['POST'])
def api_send_dispensation():
    try:
        rx_prescription_process_identifier = request.json.get('rxPrescriptionProcessIdentifier', '')
        if not rx_prescription_process_identifier:
            return jsonify({"error": "Missing rxPrescriptionProcessIdentifier"}), 400
        dispense_resources = create_medication_dispense(rx_prescription_process_identifier, 
                                                        datetime.now(get_localzone()).replace(microsecond=0).isoformat())
        return send_dispensation(dispense_resources)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/cancel_dispensation', methods=['POST'])
def api_cancel_dispensation():
    rx_prescription_process_identifier = request.json.get('rxPrescriptionProcessIdentifier', '')
    if not rx_prescription_process_identifier:
        return jsonify({"error": "Missing rxPrescriptionProcessIdentifier"}), 400
    try:
        return cancel_dispensation(rx_prescription_process_identifier)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)