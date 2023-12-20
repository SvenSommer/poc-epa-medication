from fhir.resources.medication import Medication
from fhir.resources.extension import Extension
from fhir.resources.identifier import Identifier
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.meta import Meta


class MedicationCreator:
    @staticmethod
    def create_medication(
        medication_id: str,
        rxPrescriptionProcessIdentifier: str,
        pzn_code: str,
        medication_text: str,
        form_code: str,
    ) -> Medication:
        # Erstellen der Meta-Daten
        meta = Meta(
            profile=[
                "https://gematik.de/fhir/epa-medication/StructureDefinition/epa-medication"
            ]
        )
        extension = [
            Extension(
                url="https://gematik.de/fhir/epa-medication/StructureDefinition/rx-prescription-process-identifier-extension",
                valueIdentifier=Identifier(
                    system="https://gematik.de/fhir/epa-medication/sid/rx-prescription-process-identifier",
                    value=rxPrescriptionProcessIdentifier,
                ),
            )
        ]

        # Erstellen des Medication-Objekts
        medication = Medication(id=medication_id, meta=meta, extension=extension)

        # Hinzufügen von Identifier, Code und Form
        medication.identifier = [{"value": medication_id}]
        medication.code = CodeableConcept(
            coding=[
                Coding(
                    system="http://fhir.de/CodeSystem/ifa/pzn",
                    code=pzn_code,
                    display=medication_text,
                )
            ]
        )
        medication.form = CodeableConcept(
            coding=[
                Coding(
                    system="https://fhir.kbv.de/CodeSystem/KBV_CS_SFHIR_KBV_DARREICHUNGSFORM",
                    code=form_code,
                )
            ]
        )

        # Weitere spezifische Felder können hier basierend auf den Anforderungen hinzugefügt werden

        return medication


# Verwendung der Klasse

if __name__ == "__main__":
    import os
    creator = MedicationCreator()
    medication = creator.create_medication(
        medication_id="f694dc19-eeb6-42ad-af4a-2865f8a227d4",
        rxPrescriptionProcessIdentifier="160.768.272.480.500_20231220",
        pzn_code="pzn123",
        medication_text="Beispiel Medikament",
        form_code="tablette",
    )
    path = "../resources_created/fsh-generated/resources"
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + "/medication.json", "w") as file:
        file.write(medication.json(indent=4))

    print(medication.json(indent=4))
