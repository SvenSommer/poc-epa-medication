from uuid import uuid4
from fhir.resources.medicationdispense import MedicationDispense
from fhir.resources.extension import Extension
from fhir.resources.reference import Reference
from fhir.resources.identifier import Identifier
from fhir.resources.meta import Meta
from datetime import datetime
from tzlocal import get_localzone

class MedicationDispenseCreator:
    @staticmethod
    def create_medication_dispense(
        rxPrescriptionProcessIdentifier: str,
        medication_reference: str,
        patient_identifier: str,
        performer_organization_reference: str,
        authorizing_prescription_reference: str,
        when_handed_over: datetime,
        dosage_instruction_text: str,
        substitution_allowed: bool,
    ) -> MedicationDispense:
        medication_dispense = MedicationDispense(
            id=str(uuid4()),
            meta=Meta(
                profile=[
                    "https://gematik.de/fhir/epa-medication/StructureDefinition/epa-medication-dispense"
                ]
            ),
            extension=[
                Extension(
                    url="https://gematik.de/fhir/epa-medication/StructureDefinition/rx-prescription-process-identifier-extension",
                    valueIdentifier=Identifier(
                        system="https://gematik.de/fhir/epa-medication/sid/rx-prescription-process-identifier",
                        value=rxPrescriptionProcessIdentifier
                    )
                )
            ],
            status="completed",
            medicationReference=Reference(reference="urn:uuid:" + medication_reference),
            subject=Reference(reference="urn:uuid:" + patient_identifier),
            performer=[
                {"actor": Reference(reference="urn:uuid:" + performer_organization_reference)}
            ],
            authorizingPrescription=[
                Reference(reference="urn:uuid:" + authorizing_prescription_reference)
            ],
            whenHandedOver=when_handed_over,
            dosageInstruction=[{"text": dosage_instruction_text}],
            substitution={"wasSubstituted": substitution_allowed}
        )

        return medication_dispense

if __name__ == "__main__":
    import os
    medication_dispense = MedicationDispenseCreator.create_medication_dispense(
        rxPrescriptionProcessIdentifier="160.768.272.480.500_20231220",
        medication_reference="123",
        patient_identifier="789",
        performer_organization_reference="456",
        authorizing_prescription_reference="101112",
        when_handed_over=datetime.now(get_localzone()),
        dosage_instruction_text="1-0-1",
        substitution_allowed=True
    )
    path = "../resources_created/fsh-generated/resources"
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + "/medication_dispense.json", "w") as file:
        file.write(medication_dispense.json(indent=4))

   # print(medication_dispense.json(indent=4))
