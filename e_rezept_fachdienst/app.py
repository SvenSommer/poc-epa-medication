from flask import Flask, request, render_template, jsonify
import json
import os
import logging
import requests
from datetime import datetime
from tzlocal import get_localzone
from requests.exceptions import RequestException
from fhir.resources import FHIRAbstractModel
from controller.prescription_controller import PrescriptionController
from controller.dispense_controller import DispenseController
from controller.cancel_controller import CancelController


from fhir_creators.medication_creator import MedicationCreator
from fhir_creators.medication_request_creator import MedicationRequestCreator
from fhir_creators.organisation_creator import OrganizationCreator
from fhir_creators.practitioner_creator import PractitionerCreator
from fhir_creators.medication_dispense_creator import MedicationDispenseCreator

from fhir_creators.models.medicationInfo import MedicationInfo
from fhir_creators.models.medicationRequestInfo import MedicationRequestInfo
from fhir_creators.models.medicationDispenseInfo import MedicationDispenseInfo
from fhir_creators.models.organizationInfo import OrganizationInfo
from fhir_creators.models.practitionerInfo import PractitionerInfo
from fhir_creators.models.prescriptionInfo import PrescriptionInfo
from fhir_creators.models.dispensationInfo import DispensationInfo

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
FHIR_OPERATION_URL = os.getenv("FHIR_OPERATION_URL", "http://127.0.0.1:5000")

def send_fhir_request(params_resource, operation):
    endpoint = f"/${operation}"
    try:
        fhir_data = fhir_model_to_json(params_resource)
        response = requests.post(f"{FHIR_OPERATION_URL}{endpoint}", json=fhir_data, verify=True)
        response.raise_for_status()
    except RequestException as err:
        logging.error(f"HTTP request error for {operation}: {err}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error in {operation}: {e}")
        raise

    logging.info(f"Response from {endpoint}: {response.json()}")
    return response.json()


def fhir_model_to_json(model: FHIRAbstractModel) -> dict:
    return json.loads(model.json())

def handle_error(e):
    logging.error("An error occurred: %s", e)
    return e.response.json()



medication_creator = MedicationCreator()
organization_creator = OrganizationCreator()
practitioner_creator = PractitionerCreator()
medication_request_creator = MedicationRequestCreator()
medication_dispense_creator = MedicationDispenseCreator()

prescription_service = PrescriptionController(medication_creator, organization_creator, practitioner_creator, medication_request_creator)
cancel_service = CancelController()
dispense_service = DispenseController(medication_creator, organization_creator, medication_dispense_creator)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/control", methods=["GET"])
def control():
    return render_template("control.html")

@app.route('/send_prescription', methods=['POST'])
def api_send_prescription():
    try:
        prescriptions_data = request.json.get('prescriptions', [])
        if not prescriptions_data:
            return jsonify({"error": "Missing prescription data"}), 400

        prescription_infos = []
        for prescription_data in prescriptions_data:
            rxPrescriptionProcessIdentifier = prescription_data.get('rxPrescriptionProcessIdentifier', '')
            medication_request_info = MedicationRequestInfo(**prescription_data['medication_request_info'])
            medication_info = MedicationInfo(**prescription_data['medication_info'])
            organization_info = OrganizationInfo(**prescription_data['organization_info'])
            practitioner_info = PractitionerInfo(**prescription_data['practitioner_info'])

            prescription_infos.append(PrescriptionInfo(
                rxPrescriptionProcessIdentifier,
                medication_request_info,
                medication_info,
                organization_info,
                practitioner_info
            ))

        params_resource = prescription_service.create_medication_requests_params(prescription_infos)
        return send_fhir_request(params_resource, "provide-prescription")
    except Exception as e:
        return handle_error(e)


@app.route('/cancel_prescription', methods=['POST'])
def api_cancel_prescription():
    try:
        medications = request.json.get('medications', [])
        if not medications:
            return jsonify({"error": "Missing medication data"}), 400

        identifiers = []
        for med in medications:
            identifiers.append(med.get('rxPrescriptionProcessIdentifier', ''))


        params_resource = cancel_service.create_cancel_resources_params(identifiers)
        return send_fhir_request(params_resource, "cancel-prescription")
    except Exception as e:
        return handle_error(e)

@app.route('/send_dispensation', methods=['POST'])
def api_send_dispensation():
    try:
        dispensations_data = request.json.get('dispensations', [])
        if not dispensations_data:
            return jsonify({"error": "Missing dispensation data"}), 400

        dispensation_infos = []
        for dispensation_data in dispensations_data:

            rxPrescriptionProcessIdentifier = dispensation_data.get('rxPrescriptionProcessIdentifier', '')
            medication_dispense_info = MedicationDispenseInfo(**dispensation_data['medication_dispense_info'])
            medication_info = MedicationInfo(**dispensation_data['medication_info'])
            organization_info = OrganizationInfo(**dispensation_data['organization_info'])

            dispensation_infos.append(DispensationInfo(
                rxPrescriptionProcessIdentifier,
                medication_dispense_info,
                medication_info,
                organization_info
            ))

        params_resource = dispense_service.create_medication_dispense_params(dispensation_infos)
        

        return send_fhir_request(params_resource, "provide-dispensation")
    except Exception as e:
        return handle_error(e)
    
@app.route('/cancel_dispensation', methods=['POST'])
def api_cancel_dispensation():
    try:
        medications = request.json.get('medications', [])
        if not medications:
            return jsonify({"error": "Missing medication data"}), 400

        identifiers = []
        for med in medications:
            identifiers.append(med.get('rxPrescriptionProcessIdentifier', ''))

        params_resource = cancel_service.create_cancel_resources_params(identifiers)
        return send_fhir_request(params_resource, "cancel-dispensation")
    except Exception as e:
        return handle_error(e)

if __name__ == "__main__":
    app.run(debug=True, port=5001)