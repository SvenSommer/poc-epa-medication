from fhir.resources.medication import Medication
from fhir.resources.extension import Extension
from fhir.resources.identifier import Identifier
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.ratio import Ratio
from fhir.resources.quantity import Quantity
from fhir.resources.meta import Meta
from typing import List
from fhir_creators.models.ingredient import Ingredient
import uuid


class MedicationCreator:
    @staticmethod
    def create_medication(
        medication_id: str,
        rxPrescriptionProcessIdentifier: str,
        #Refactor to use a medication_coding object
        medication_coding_code: str,
        medication_coding_display: str,
        medication_coding_system: str,
        #Refactor to use a form_coding object
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
    
    # Lets rewrite this function to pass a list of ingredients
    @staticmethod
    def create_medication_with_ingredients(
        medication_id: str,
        rxPrescriptionProcessIdentifier: str,
        #Refactor to use a medication_coding object
        medication_coding_code: str,
        medication_coding_display: str,
        medication_coding_system: str,
        #Refactor to use a form_coding object
        form_coding_system: str,
        form_coding_code: str,
        form_coding_display: str,
        ingredients: List[Ingredient]
        ) -> Medication:
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

            medication.ingredient = [ingredient.to_fhir() for ingredient in ingredients]

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
    def get_example_medication_ingredient(rxPrescriptionProcessIdentifier):
        medication_with_ingredients = MedicationCreator.create_medication_with_ingredients(
            medication_id=str(uuid.uuid4()),
            rxPrescriptionProcessIdentifier=rxPrescriptionProcessIdentifier,
            medication_coding_code="L01DB01",
            medication_coding_display="Doxorubicin",
            medication_coding_system="http://fhir.de/CodeSystem/bfarm/atc",
            form_coding_system="http://standardterms.edqm.eu",
            form_coding_code="11210000",
            form_coding_display="Solution for infusion",
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
