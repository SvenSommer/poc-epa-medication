from fhir.resources.parameters import Parameters, ParametersParameter
from fhir_creators.models.prescriptionInfo import PrescriptionInfo
import logging



class PrescriptionController:
    def __init__(self, medication_creator, organization_creator, practitioner_creator, medication_request_creator):
        self.medication_creator = medication_creator
        self.organization_creator = organization_creator
        self.practitioner_creator = practitioner_creator
        self.medication_request_creator = medication_request_creator

    def create_medication_requests_params(self, prescription_infos):
        try:
            params = Parameters.construct()
            params.parameter = []
            for prescription_info in prescription_infos:
                rx_prescription_param = self.construct_rx_prescription_parameter(prescription_info)
                params.parameter.append(rx_prescription_param)

            return params
        except Exception as e:
            logging.error(f"Error in create_medication_requests_params: {e}")
            raise


    def construct_rx_prescription_parameter(self, prescription_info: PrescriptionInfo):
        medication = self.medication_creator.create_medication(prescription_info.medication_info)
        prescription_info.medication_request_info.medication_reference = medication.id
        medication_request = self.medication_request_creator.create_medication_request(prescription_info.medication_request_info)
        organization = self.organization_creator.create_organization(prescription_info.organization_info)
        practitioner = self.practitioner_creator.build_practitioner(prescription_info.practitioner_info)

        rx_prescription_part = [
            ParametersParameter.construct(name="RxPrescriptionProcessIdentifier", valueIdentifier=prescription_info.rxPrescriptionProcessIdentifier),
            ParametersParameter.construct(name="MedicationRequest", resource=medication_request),
            ParametersParameter.construct(name="Medication", resource=medication),
            ParametersParameter.construct(name="Organization", resource=organization),
            ParametersParameter.construct(name="Practitioner", resource=practitioner),
        ]

        rx_prescription_param = ParametersParameter.construct(name="RxPrescription", part=rx_prescription_part)
        return rx_prescription_param