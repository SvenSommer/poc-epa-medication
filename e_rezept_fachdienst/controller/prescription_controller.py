from fhir.resources.parameters import Parameters, ParametersParameter
from tzlocal import get_localzone
import logging
from datetime import datetime


class PrescriptionController:
    def __init__(self, medication_creator, organization_creator, practitioner_creator, medication_request_creator):
        self.medication_creator = medication_creator
        self.organization_creator = organization_creator
        self.practitioner_creator = practitioner_creator
        self.medication_request_creator = medication_request_creator

    def create_medication_requests_params(self, rxPrescriptionProcessIdentifiers):
        try:
            params = Parameters.construct()
            params.parameter = []
            for identifier in rxPrescriptionProcessIdentifiers:
                rx_prescription_param = self.contruct_rx_prescription_parameter(identifier)
                params.parameter.append(rx_prescription_param)

            return params
        except Exception as e:
            logging.error(f"Error in create_medication_request: {e}")
            raise

    def contruct_rx_prescription_parameter(self, rxPrescriptionProcessIdentifier):
        medication = self.medication_creator.get_example_medication_ingredient(rxPrescriptionProcessIdentifier)
        organization = self.organization_creator.get_example_farmacy_organization()
        practitioner = self.practitioner_creator.get_example_practitioner()
        medication_request = self.medication_request_creator.create_medication_request(
                medication.id,
                rxPrescriptionProcessIdentifier,
                "Patient/67890",
                datetime.now(get_localzone()).replace(microsecond=0).isoformat(),
                "Take one tablet daily",
                True
            )

        rx_prescription_part = [
                ParametersParameter.construct(name="RxPrescriptionProcessIdentifier", valueIdentifier=rxPrescriptionProcessIdentifier),
                ParametersParameter.construct(name="MedicationRequest", resource=medication_request),
                ParametersParameter.construct(name="Medication", resource=medication),
                ParametersParameter.construct(name="Organization", resource=organization),
                ParametersParameter.construct(name="Practitioner", resource=practitioner),
            ]

        rx_prescription_param = ParametersParameter.construct(name="RxPrescription", part=rx_prescription_part)
        return rx_prescription_param