from fhir.resources.parameters import Parameters, ParametersParameter
from fhir_creators.models.dispensationInfo import DispensationInfo
import logging


class DispenseController:
    def __init__(self, medication_creator, organization_creator, medication_dispense_creator):
        self.medication_creator = medication_creator
        self.organization_creator = organization_creator
        self.medication_dispense_creator = medication_dispense_creator

    def create_medication_dispense_params(self, dispensation_infos):
        try:
            params = Parameters.construct()
            params.parameter = []
            for dispensation_info in dispensation_infos:
                rx_param = self.construct_rx_dispensation_parameters(dispensation_info)
                params.parameter.append(rx_param)

            return params

        except Exception as e:
            logging.error(f"Error in create_medication_dispenses: {e}")
            raise

    def construct_rx_dispensation_parameters(self, dispensation_infos: DispensationInfo):
        logging.info(dispensation_infos)
        medication = self.medication_creator.create_medication(dispensation_infos.medication_info)
        organization = self.organization_creator.create_organization(dispensation_infos.organization_info)
        medication_dispense = self.medication_dispense_creator.create_medication_dispense(dispensation_infos.medication_dispense_info)

        rx_dispensation_part = [
                ParametersParameter.construct(name="RxPrescriptionProcessIdentifier", valueIdentifier=dispensation_infos.rxPrescriptionProcessIdentifier),
                ParametersParameter.construct(name="MedicationDispense", resource=medication_dispense),
                ParametersParameter.construct(name="Medication", resource=medication),
                ParametersParameter.construct(name="Organization", resource=organization),
            ]

        rx_dispensation_param = ParametersParameter.construct(name="RxDispensation", part=rx_dispensation_part)
        return rx_dispensation_param