from fhir.resources.medication import Medication
from fhir.resources.extension import Extension
from fhir.resources.identifier import Identifier
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.meta import Meta
from typing import List, Optional
from fhir_creators.models.codingObject import CodingObject
from fhir_creators.models.ingredient import Ingredient
import uuid

class MedicationCreator:
    @staticmethod
    def create_medication(
        medication_id: str,
        rxPrescriptionProcessIdentifier: str,
        medication_coding: CodingObject,
        form_coding: Optional[CodingObject] = None,
    ) -> Medication:
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
        medication = Medication(id=medication_id, meta=meta, extension=extension)
        medication.identifier = [Identifier(value=medication_id)]
        medication.code = CodeableConcept(coding=[medication_coding.to_coding()])
        if form_coding:
            medication.form = CodeableConcept(coding=[form_coding.to_coding()])
        medication.status = "active"

        return medication

    @staticmethod
    def create_medication_with_ingredients(
        medication_id: str,
        rxPrescriptionProcessIdentifier: str,
        medication_coding: CodingObject,
        form_coding: Optional[CodingObject],
        ingredients: List[Ingredient]
    ) -> Medication:
        medication = MedicationCreator.create_medication(
            medication_id=medication_id,
            rxPrescriptionProcessIdentifier=rxPrescriptionProcessIdentifier,
            medication_coding=medication_coding,
            form_coding=form_coding,
        )
        medication.ingredient = [ingredient.to_fhir() for ingredient in ingredients]
        return medication

    @staticmethod
    def get_example_medication(rxPrescriptionProcessIdentifier):
        return [
            MedicationCreator.create_medication(
                medication_id=str(uuid.uuid4()),
                rxPrescriptionProcessIdentifier=rxPrescriptionProcessIdentifier,
                medication_coding=CodingObject(
                    code="08671219",
                    display="Aciclovir 800 - 1 A Pharma® 35 Tbl. N1",
                    system="http://fhir.de/CodeSystem/ifa/pzn"
                ),
                form_coding=CodingObject(
                    code="TAB",
                    display="Tablette",
                    system="https://fhir.kbv.de/CodeSystem/KBV_CS_SFHIR_KBV_DARREICHUNGSFORM"
                )
            ),
            MedicationCreator.create_medication(
                medication_id=str(uuid.uuid4()),
                rxPrescriptionProcessIdentifier="456",
                medication_coding=CodingObject(
                    code="5682",
                    display="Ibuprofen",
                    system="http://fhir.de/CodeSystem/ask"
                ),
                form_coding=None
            )
        ]

    @staticmethod
    def get_example_medication_ingredient(rxPrescriptionProcessIdentifier):
        medication_with_ingredients = MedicationCreator.create_medication_with_ingredients(
            medication_id=str(uuid.uuid4()),
            rxPrescriptionProcessIdentifier=rxPrescriptionProcessIdentifier,
            medication_coding=CodingObject(
                code="L01DB01",
                display="Doxorubicin",
                system="http://fhir.de/CodeSystem/bfarm/atc"
            ),
            form_coding=CodingObject(
                code="11210000",
                display="Solution for infusion",
                system="http://standardterms.edqm.eu"
            ),
            ingredients=[
                Ingredient(
                    item_code="L01DB01",
                    item_display="Doxorubicin",
                    item_system="http://fhir.de/CodeSystem/bfarm/atc",
                    amount_numerator_value=85.0,
                    amount_numerator_unit="mg",
                    amount_numerator_code="mg",
                    amount_denominator_value=250.0,
                    amount_denominator_unit="mL",
                    amount_denominator_code="mL"
                ),
                Ingredient(
                    item_code="SODIUM CHLORIDE",
                    item_display="Sodium Chloride",
                    item_system="http://fhir.de/CodeSystem/bfarm/atc",
                    amount_numerator_value=0.9,
                    amount_numerator_unit="mg",
                    amount_numerator_code="mg",
                    amount_denominator_value=250.0,
                    amount_denominator_unit="mL",
                    amount_denominator_code="mL"
                )
            ]
        )
        return medication_with_ingredients



if __name__ == "__main__":
    import os
    creator = MedicationCreator()
    medication = creator.get_example_medication_pzn()
    path = "../resources_created/fsh-generated/resources"
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + "/medication.json", "w") as file:
        file.write(medication.json(indent=4))

    print(medication.json(indent=4))
