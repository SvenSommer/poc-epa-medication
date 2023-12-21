from flask import Flask, render_template,request, jsonify
import logging

from database_controller import Database

# Initialize logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

db = Database()


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
    return render_template('index.html')

@app.route('/get-fhir-data/<resource_type>', methods=['GET'])
def get_fhir_data_by_type(resource_type):
    if db.connect():
        resources = db.get_all_resources(resource_type)
        db.close()
        return jsonify(resources)
    else:
        return jsonify({"status": f"Medication Service: running - Database Connection Failed"}), 500
    

    
@app.route('/get-fhir-data/<resource_type>/<resource_id>', methods=['GET'])
def get_fhir_data_by_id(resource_type, resource_id):
    if db.connect():
        resource = db.get_resource(resource_type, resource_id)
        db.close()
        return jsonify(resource)
    else:
        return jsonify({"status": f"Medication Service: running - Database Connection Failed"}), 500

@app.route('/get-fhir-data', methods=['GET'])
def get_fhir_data():
    if db.connect():
        organisations_resources = db.get_all_resources('organization')
        medication_resources = db.get_all_resources('medication')
        practitioners_resources = db.get_all_resources('practitioner')
        medication_request_resources = db.get_all_resources('medicationrequest')
        medication_dispense_resources = db.get_all_resources('medicationdispense')
        db.close()
        response = {"Organisations": organisations_resources, 
                    "Medications": medication_resources, 
                    "Practitioners": practitioners_resources, 
                    "MedicationRequests": medication_request_resources, 
                    "MedicationDispenses": medication_dispense_resources}
        return jsonify(response)
    else:
        return jsonify({"status": f"Medication Service: running - Database Connection Failed"}), 500
    

@app.route('/$provide-prescription', methods=['POST'])
def provide_prescription():
    fhir_data = request.json

    # List of resource types to process
    resource_types = ['MedicationRequest', 'Medication', 'Organization', 'Practitioner']

    if not validate_fhir_data(fhir_data, set(resource_types)):
        return send_response("Invalid FHIR data", 400)

    try:
        params = extract_parameters(fhir_data, resource_types)
        if not params:
            raise ValueError("Required parameters not found")

        # Process prescription logic here (if any)
        logging.info(f"RxPrescriptionProcessIdentifier: {params.get('MedicationRequest', {}).get('identifier', [{}])[0].get('value')}")
        logging.info(f"MedicationRequest Status: {params.get('MedicationRequest', {}).get('status')}")

        # Create or Update resources in a loop
        db.connect()
        for resource_type in resource_types: 
            if resource_type in params:
                db.create_or_update_resource(resource_type, params[resource_type])
                logging.info(f"{resource_type}: {params[resource_type].get('name')}")

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

    # List of resource types to process
    resource_types = ['MedicationDispense', 'Medication', 'Organization']

    if not validate_fhir_data(fhir_data, set(resource_types)):
        return send_response("Invalid FHIR data", 400)

    try:
        params = extract_parameters(fhir_data, resource_types)
        if not params:
            raise ValueError("Required parameters not found")

        # Process the dispensation logic here (if any)
        # Example logging, adjust according to your data structure
        logging.info(f"RxPrescriptionProcessIdentifier: {params.get('MedicationDispense', {}).get('extension', [{}])[0].get('valueIdentifier', {}).get('value')}")
        logging.info(f"MedicationDispense Status: {params.get('MedicationDispense', {}).get('status')}")

        # Create or Update resources in a loop
        db.connect()
        for resource_type in resource_types:
            if resource_type in params:
                db.create_or_update_resource(resource_type, params[resource_type])
                logging.info(f"{resource_type}: {params[resource_type].get('name')}")

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
