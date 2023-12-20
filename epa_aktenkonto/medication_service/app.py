from flask import Flask, request, jsonify
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

def send_response(message, status_code=200):
    return jsonify({"message": message}), status_code

def extract_parameters(fhir_data, required_params):
    if not fhir_data.get('parameter'):
        return None

    parameters = {param.get('name'): param.get('resource') for param in fhir_data.get('parameter', [])}
    if not all(param in parameters for param in required_params):
        return None

    return parameters

def validate_fhir_data(fhir_data, required_types):
    received_types = {param.get('name') for param in fhir_data.get('parameter', [])}
    return required_types.issubset(received_types)

@app.route('/', methods=['GET'])
def index():
    return "Medication Service: running"

@app.route('/$provide-prescription', methods=['POST'])
def provide_prescription():
    fhir_data = request.json

    if not validate_fhir_data(fhir_data, {'MedicationRequest', 'Medication', 'Organization', 'Practitioner'}):
        return send_response("Invalid FHIR data", 400)

    try:
        params = extract_parameters(fhir_data, ['MedicationRequest', 'Medication', 'Organization', 'Practitioner'])
        if not params:
            raise ValueError("Required parameters not found")

        # TODO: Process prescription logic here
        logging.info(f"RxPrescriptionProcessIdentifier: {params['MedicationRequest'].get('identifier')[0].get('value')}")
        logging.info(f"MedicationRequest Status: {params['MedicationRequest'].get('status')}")
       
        return send_response("OperationOutcome (success)")
    except DuplicatePrescriptionError:
        return send_response("Duplicate prescription", 409)
    except Exception as e:
        return send_response(str(e), 500)

@app.route('/$cancel-prescription', methods=['POST'])
def cancel_prescription():
    fhir_data = request.json

    if not validate_fhir_data(fhir_data, {'RxPrescriptionProcessIdentifier'}):
        return send_response("Invalid FHIR data", 400)

    try:
        params = extract_parameters(fhir_data, ['RxPrescriptionProcessIdentifier'])
        if not params:
            raise ValueError("RxPrescriptionProcessIdentifier not found in Parameters")

        # TODO: Process cancellation logic here

        return send_response("Prescription cancelled successfully")
    except Exception as e:
        return send_response(str(e), 500)

@app.route('/$provide-dispensation', methods=['POST'])
def provide_dispensation():
    fhir_data = request.json

    if not validate_fhir_data(fhir_data, {'MedicationDispense', 'Medication', 'Organization'}):
        return send_response("Invalid FHIR data", 400)

    try:
        params = extract_parameters(fhir_data, ['MedicationDispense', 'Medication', 'Organization'])
        if not params:
            raise ValueError("Required parameters not found")

        # TODO: Process the dispensation logic here
        logging.info(f"RxPrescriptionProcessIdentifier: {params['MedicationDispense'].get('extension')[0].get('valueIdentifier').get('value')}")
        logging.info(f"MedicationDispense Status: {params['MedicationDispense'].get('status')}")

        return send_response("Dispensation provided successfully")
    except Exception as e:
        return send_response(str(e), 500)

@app.route('/$cancel-dispensation', methods=['POST'])
def cancel_dispensation():
    fhir_data = request.json

    if not validate_fhir_data(fhir_data, {'RxPrescriptionProcessIdentifier'}):
        return send_response("Invalid FHIR data", 400)

    try:
        params = extract_parameters(fhir_data, ['RxPrescriptionProcessIdentifier'])
        if not params:
            raise ValueError("RxPrescriptionProcessIdentifier not found in Parameters")

        # TODO:  Implement the logic to cancel or reverse the dispensation here

        return send_response("Dispensation cancelled successfully")
    
    except Exception as e:
        return send_response(str(e), 500)

class DuplicatePrescriptionError(Exception):
    pass

if __name__ == '__main__':
    app.run(debug=True)
