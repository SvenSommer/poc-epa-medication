from uuid import uuid4
from fhir.resources.medicationrequest import MedicationRequest
from fhir.resources.extension import Extension
from fhir.resources.identifier import Identifier
from fhir.resources.quantity import Quantity
from fhir.resources.reference import Reference
from fhir.resources.dosage import Dosage
from fhir.resources.meta import Meta
from datetime import datetime
from tzlocal import get_localzone
import os

class MedicationRequestCreator:
    @staticmethod
    def create_medication_request(
        medication_reference: str,
        rxPrescriptionProcessIdentifier: str,
        patient_reference: str,
        dosage_instruction_text: str,
        substitution_allowed: bool,
    ) -> MedicationRequest:
        
        current_date_formatted = datetime.now().strftime("%d.%m.%Y")
        identifier_value = current_date_formatted

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
                    value=rxPrescriptionProcessIdentifier,
                ),
            ],
            dispenseRequest={
                "quantity": Quantity(
                    system="http://unitsofmeasure.org", code="{Package}", value=1
                )
            },
            status="active",
            intent="order",
            medicationReference=Reference(reference="urn:uuid:" +medication_reference),
            subject=Reference(reference="urn:uuid:" +patient_reference),
            authoredOn=datetime.now(get_localzone()).isoformat(),
            dosageInstruction=[Dosage(text=dosage_instruction_text)],
            substitution={"allowedBoolean": substitution_allowed},
        )

        return medication_request
    

if __name__ == "__main__":
    medication_request = MedicationRequestCreator.create_medication_request(
        medication_reference="123",
        rxPrescriptionProcessIdentifier="160.768.272.480.500_20231220",
        patient_reference="789",
        dosage_instruction_text="1-0-1",
        substitution_allowed=True,
    )
    #check if path exists 
    path = "../resources_created/fsh-generated/resources"
    #if not create it
    #save the medication_request to the file
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + "/medication_request.json", "w") as file:
        file.write(medication_request.json(indent=4))

    print(medication_request.json(indent=4))