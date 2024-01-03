from uuid import uuid4
from fhir.resources.medicationrequest import MedicationRequest
from fhir.resources.identifier import Identifier
from fhir.resources.quantity import Quantity
from fhir.resources.reference import Reference
from fhir.resources.dosage import Dosage
from fhir.resources.meta import Meta
from datetime import datetime

from fhir_creators.models.medicationRequestInfo import MedicationRequestInfo


class MedicationRequestCreator:
    @staticmethod
    def create_medication_request(medication_request_info: MedicationRequestInfo) -> MedicationRequest:
        medication_request = MedicationRequest(
            id=str(uuid4()),
            meta=Meta(
                profile=[
                    "https://gematik.de/fhir/epa-medication/StructureDefinition/epa-medication-request"
                ]
            ),
            identifier=[
                Identifier(
                    system="https://gematik.de/fhir/epa-medication/sid/rx-prescription-process-identifier",
                    value=medication_request_info.rxPrescriptionProcessIdentifier,
                ),
            ],
            dispenseRequest={
                "quantity": Quantity(
                    system="http://unitsofmeasure.org", code="{Package}", value=1
                )
            },
            status="active",
            intent="order",
            medicationReference=Reference(reference="urn:uuid:" + medication_request_info.medication_reference),
            subject=Reference(reference="urn:uuid:" + medication_request_info.patient_reference),
            authoredOn=medication_request_info.authoredOn,
            dosageInstruction=[Dosage(text=medication_request_info.dosage_instruction_text)],
            substitution={"allowedBoolean": medication_request_info.substitution_allowed},
        )

        return medication_request
    
    @staticmethod
    def get_example_medication_request(rxPrescriptionProcessIdentifier):
        medication_request_info = MedicationRequestInfo(
            medication_reference="123",
            rxPrescriptionProcessIdentifier=rxPrescriptionProcessIdentifier,
            patient_reference="789",
            authoredOn=datetime.now(),
            dosage_instruction_text="1-0-1",
            substitution_allowed=True,
        )
        return MedicationRequestCreator.create_medication_request(medication_request_info)

if __name__ == "__main__":
    import os
    request_info = MedicationRequestInfo(
        medication_reference="123",
        rxPrescriptionProcessIdentifier="160.768.272.480.500_20231220",
        patient_reference="789",
        authoredOn=datetime.now(),
        dosage_instruction_text="1-0-1",
        substitution_allowed=True,
    )
    medication_request = MedicationRequestCreator.create_medication_request(request_info)
    path = "../resources_created/fsh-generated/resources"
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + "/medication_request.json", "w") as file:
        file.write(medication_request.json(indent=4))

    print(medication_request.json(indent=4))