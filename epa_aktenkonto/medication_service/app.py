from flask import Flask, render_template, request, jsonify
import logging

from controller.database.database_reader import DatabaseReader
from controller.database.database_writer import DatabaseWriter
from fhirValidator.fhirValidator import FHIRValidator
from controller.fhir.prescriptionController import PrescriptionController
from controller.fhir.medicationRequestController import DuplicateMedicationRequestError
from controller.fhir.dispensationController import DispensationController, MedicationRequestMissingError

# Initialize logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

db_reader = DatabaseReader()
db_writer = DatabaseWriter()
fhir_validator = FHIRValidator()
prescription_controller = PrescriptionController(db_reader,db_writer)
dispensation_controller = DispensationController(db_reader,db_writer)


def send_response(message, status_code=200):
    return jsonify({"message": message, "status_code": status_code}), status_code

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/ressources", methods=["GET"])
def resources():
    return render_template("resources.html")

@app.route("/get-fhir-data/<resource_type>", methods=["GET"])
def get_fhir_data_by_type(resource_type):
    if db_reader.connect():
        resources = db_reader.get_all_resources(resource_type)
        return jsonify(resources)
    else:
        return send_response("Medication Service: running - Database Connection Failed", 500)


@app.route("/get-fhir-data/<resource_type>/<resource_id>", methods=["GET"])
def get_fhir_data_by_id(resource_type, resource_id):
    if db_reader.connect():
        resource = db_reader.get_resource(resource_type, resource_id)
        return jsonify(resource)
    else:
        return send_response("Medication Service: running - Database Connection Failed", 500)

@app.route("/get-fhir-data", methods=["GET"])
def get_fhir_data():
    if db_reader.connect():
        organisations_resources = db_reader.get_all_resources("organization")
        medication_resources = db_reader.get_all_resources("medication")
        practitioners_resources = db_reader.get_all_resources("practitioner")
        medication_request_resources = db_reader.get_all_resources("medicationrequest")
        medication_dispense_resources = db_reader.get_all_resources("medicationdispense")
        provenance_resources = db_reader.get_all_resources("provenance")
        response = {
            "Organisations": organisations_resources,
            "Medications": medication_resources,
            "Practitioners": practitioners_resources,
            "MedicationRequests": medication_request_resources,
            "MedicationDispenses": medication_dispense_resources,
            "Provenances": provenance_resources
        }
        return jsonify(response)
    else:
        return send_response("Medication Service: running - Database Connection Failed", 500)

@app.route("/get-rx-identifier", methods=["GET"])
def get_rx_identifier():
    if db_reader.connect():
        rx_identifier = db_reader.get_rx_identifier()
        return jsonify(rx_identifier)
    else:
        return send_response("Medication Service: running - Database Connection Failed", 500)

@app.route("/$provide-prescription", methods=["POST"])
def provide_prescription():
    fhir_data = request.json
    try:
        exspected_ressource_types = ["MedicationRequest", "Medication", "Organization", "Practitioner"]
        if not fhir_validator.validate_fhir_data(fhir_data, set(exspected_ressource_types)):
            return send_response("Invalid FHIR data", 400)
        
        prescription_controller.handle_provide_prescriptions(fhir_data)
        return send_response("Prescription provided successfully")
    
    except DuplicateMedicationRequestError as e:
        return send_response(str(e), 409)
    except Exception as e:
        logging.error(e)
        return send_response(str(e), 500)


@app.route("/$cancel-prescription", methods=["POST"])
def cancel_prescription():
    fhir_data = request.json

    if not fhir_validator.validate_fhir_data(fhir_data, {"RxPrescriptionProcessIdentifier"}):
        return send_response("Invalid FHIR data", 400)

    try:
        prescription_controller.handle_cancel_prescription(fhir_data)
        return send_response("Prescription cancelled successfully")
    
    except Exception as e:
        logging.error(e)
        return send_response(str(e), 500)


@app.route("/$provide-dispensation", methods=["POST"])
def provide_dispensation():
    fhir_data = request.json
    try:
        exspected_ressource_types = ["MedicationDispense", "Medication", "Organization"]
        if not fhir_validator.validate_fhir_data(fhir_data, set(exspected_ressource_types)):
            return send_response("Invalid FHIR data", 400)
        
        dispensation_controller.handle_provide_dispensation(fhir_data)
        return send_response("Dispensation provided successfully")
    
    except MedicationRequestMissingError as e:
        return send_response(str(e), 422)
    except Exception as e:
        logging.error(e)
        return send_response(str(e), 500)


@app.route("/$cancel-dispensation", methods=["POST"])
def cancel_dispensation():
    fhir_data = request.json

    if not fhir_validator.validate_fhir_data(fhir_data, {"RxPrescriptionProcessIdentifier"}):
        return send_response("Invalid FHIR data", 400)

    try:
        dispensation_controller.handle_cancel_dispensation(fhir_data)
        return send_response("Dispensation cancelled successfully")
    
    except Exception as e:
        logging.error(e)
        return send_response(str(e), 500)


if __name__ == "__main__":
    app.run(debug=True)
