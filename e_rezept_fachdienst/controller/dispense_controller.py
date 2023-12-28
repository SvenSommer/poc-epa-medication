from fhir.resources.parameters import Parameters, ParametersParameter
import logging


class DispenseController:
    def __init__(self, medication_creator, organization_creator, medication_dispense_creator):
        self.medication_creator = medication_creator
        self.organization_creator = organization_creator
        self.medication_dispense_creator = medication_dispense_creator

    def create_medication_dispense_params(self, rxPrescriptionProcessIdentifiers, when_handed_over):
        try:
            params = Parameters.construct()
            params.parameter = []
            for identifier in rxPrescriptionProcessIdentifiers:
                rx_prescription_param = self.construct_rx_dispensation_parameters(identifier, when_handed_over)
                params.parameter.append(rx_prescription_param)

            return params

        except Exception as e:
            logging.error(f"Error in create_medication_dispenses: {e}")
            raise

    def construct_rx_dispensation_parameters(self, rxPrescriptionProcessIdentifier, when_handed_over):
        medication = self.medication_creator.get_example_medication_ingredient(rxPrescriptionProcessIdentifier)
        organization = self.organization_creator.get_example_farmacy_organization()
        medication_dispense = self.medication_dispense_creator.create_medication_dispense(
                rxPrescriptionProcessIdentifier, medication.id, "Patient/67890", organization.id, "MedicationRequest/123", when_handed_over, "Take one tablet daily", True
            )

        rx_dispensation_part = [
                ParametersParameter.construct(name="RxPrescriptionProcessIdentifier", valueIdentifier=rxPrescriptionProcessIdentifier),
                ParametersParameter.construct(name="MedicationDispense", resource=medication_dispense),
                ParametersParameter.construct(name="Medication", resource=medication),
                ParametersParameter.construct(name="Organization", resource=organization),
            ]

        rx_dispensation_param = ParametersParameter.construct(name="RxDispensation", part=rx_dispensation_part)
        return rx_dispensation_param