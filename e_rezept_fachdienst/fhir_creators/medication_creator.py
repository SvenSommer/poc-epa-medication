from fhir.resources.medication import Medication, MedicationIngredient
from fhir.resources.extension import Extension
from fhir.resources.identifier import Identifier
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.ratio import Ratio
from fhir.resources.quantity import Quantity
from fhir.resources.meta import Meta


import uuid


class MedicationCreator:
    @staticmethod
    def create_medication(
        medication_id: str,
        rxPrescriptionProcessIdentifier: str,
        medication_coding_code: str,
        medication_coding_display: str,
        medication_coding_system: str,
        form_coding_system: str,
        form_coding_code: str,
        form_coding_display: str = None,
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

        medication.identifier = [{"value": medication_id}]
        medication.code = CodeableConcept(
            coding=[
                Coding(
                    system=medication_coding_system,
                    code=medication_coding_code,
                    display=medication_coding_display,
                )
            ]
        )
        if form_coding_system is not None and form_coding_code is not None:
            medication.form = CodeableConcept(
                coding=[
                    Coding(
                        system=form_coding_system,
                        code=form_coding_code,
                        display = form_coding_display
                    )
                ]
            )
        medication.status = "active"

        return medication
    
    @staticmethod
    def create_medication_with_ingredients(
        medication_id: str,
        rxPrescriptionProcessIdentifier: str,
        medication_coding_code: str,
        medication_coding_display: str,
        medication_coding_system: str,
        form_coding_system: str,
        form_coding_code: str,
        form_coding_display: str,
        ingredient_item_code: str,
        ingredient_item_display: str,
        ingredient_item_system: str,
        ingredient_amount_numerator_value: float,
        ingredient_amount_numerator_unit: str,
        ingredient_amount_numerator_code: str,
        ingredient_amount_denominator_value: float,
        ingredient_amount_denominator_unit: str,
        ingredient_amount_denominator_code: str,
    ) -> Medication:
        # Create the base medication instance
        medication = MedicationCreator.create_medication(
            medication_id=medication_id,
            rxPrescriptionProcessIdentifier=rxPrescriptionProcessIdentifier,
            medication_coding_code=medication_coding_code,
            medication_coding_display=medication_coding_display,
            medication_coding_system=medication_coding_system,
            form_coding_system=form_coding_system,
            form_coding_code=form_coding_code,
            form_coding_display=form_coding_display,
        )

        # Create ingredient
        ingredient = MedicationIngredient(
            itemCodeableConcept=CodeableConcept(
                coding=[
                    Coding(
                        system=ingredient_item_system,
                        code=ingredient_item_code,
                        display=ingredient_item_display,
                    )
                ]
            ),
            strength=Ratio(
                numerator=Quantity(
                    value=ingredient_amount_numerator_value,
                    unit=ingredient_amount_numerator_unit,
                    system="http://unitsofmeasure.org",
                    code=ingredient_amount_numerator_code,
                ),
                denominator=Quantity(
                    value=ingredient_amount_denominator_value,
                    unit=ingredient_amount_denominator_unit,
                    system="http://unitsofmeasure.org",
                    code=ingredient_amount_denominator_code,
                )
            ),
            isActive=True,
        )

        # Add ingredient to medication
        medication.ingredient = [ingredient]

        return medication


    @staticmethod
    def get_example_medication_pzn(rxPrescriptionProcessIdentifier):

        medication_id = str(uuid.uuid4())
        medication = MedicationCreator.create_medication(
            medication_id=medication_id,
            rxPrescriptionProcessIdentifier=rxPrescriptionProcessIdentifier,
            medication_coding_code="08671219",
            medication_coding_display="Aciclovir 800 - 1 A Pharma® 35 Tbl. N1",
            medication_coding_system="http://fhir.de/CodeSystem/ifa/pzn",
            form_coding_system="https://fhir.kbv.de/CodeSystem/KBV_CS_SFHIR_KBV_DARREICHUNGSFORM",
            form_coding_code="TAB",
            form_coding_display="Tablette"
        )
        return medication
    
    @staticmethod
    def get_example_medication_ask(rxPrescriptionProcessIdentifier):

        medication_id = str(uuid.uuid4())
        medication = MedicationCreator.create_medication(
            medication_id=medication_id,
            rxPrescriptionProcessIdentifier=rxPrescriptionProcessIdentifier,
            medication_coding_code="5682",
            medication_coding_display="Ibuprofen",
            medication_coding_system="http://fhir.de/CodeSystem/ask",
            form_coding_system=None,
            form_coding_code=None,
            form_coding_display=None
        )
        return medication

    @staticmethod
    def get_example_medication_ingedient(rxPrescriptionProcessIdentifier):
        medication_with_ingredients = creator.create_medication_with_ingredients(
            medication_id=str(uuid.uuid4()),
            rxPrescriptionProcessIdentifier=rxPrescriptionProcessIdentifier,
            medication_coding_code="L01DB01",
            medication_coding_display="Doxorubicin",
            medication_coding_system="http://fhir.de/CodeSystem/bfarm/atc",
            form_coding_system="http://standardterms.edqm.eu",
            form_coding_code="11210000",
            form_coding_display="Solution for infusion",
            ingredient_item_code="L01DB01",
            ingredient_item_display="Doxorubicin",
            ingredient_item_system="http://fhir.de/CodeSystem/bfarm/atc",
            ingredient_amount_numerator_value=85.0,
            ingredient_amount_numerator_unit="mg",
            ingredient_amount_numerator_code="mg",
            ingredient_amount_denominator_value=250.0,
            ingredient_amount_denominator_unit="mL",
            ingredient_amount_denominator_code="mL"
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
