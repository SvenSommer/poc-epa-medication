from fhir.resources.parameters import Parameters, ParametersParameter
import logging


class CancelController:
    def __init__(self) -> None:
        pass

    def create_cancel_resources_params(self, rxPrescriptionProcessIdentifiers):
        try:
            params = Parameters.construct()
            params.parameter = []
            for identifier in rxPrescriptionProcessIdentifiers:
                rx_prescription_param = ParametersParameter.construct(
                    name="RxPrescriptionProcessIdentifier",
                    valueIdentifier={"value": identifier}
                )
                params.parameter.append(rx_prescription_param)

            return params

        except Exception as e:
            logging.error(f"Error in create_cancel_resources: {e}")
            raise