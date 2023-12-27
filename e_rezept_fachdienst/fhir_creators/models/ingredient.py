from fhir.resources.medication import  Medication, MedicationIngredient
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.ratio import Ratio
from fhir.resources.quantity import Quantity


class Ingredient:
    def __init__(
        self,
        item_code: str,
        item_display: str,
        item_system: str,
        amount_numerator_value: float,
        amount_numerator_unit: str,
        amount_numerator_code: str,
        amount_denominator_value: float,
        amount_denominator_unit: str,
        amount_denominator_code: str,
    ):
        self.item_code = item_code
        self.item_display = item_display
        self.item_system = item_system
        self.amount_numerator_value = amount_numerator_value
        self.amount_numerator_unit = amount_numerator_unit
        self.amount_numerator_code = amount_numerator_code
        self.amount_denominator_value = amount_denominator_value
        self.amount_denominator_unit = amount_denominator_unit
        self.amount_denominator_code = amount_denominator_code

    def to_fhir(self) -> MedicationIngredient:
        return MedicationIngredient(
            itemCodeableConcept=CodeableConcept(
                coding=[
                    Coding(
                        system=self.item_system,
                        code=self.item_code,
                        display=self.item_display,
                    )
                ]
            ),
            strength=Ratio(
                numerator=Quantity(
                    value=self.amount_numerator_value,
                    unit=self.amount_numerator_unit,
                    system="http://unitsofmeasure.org",
                    code=self.amount_numerator_code,
                ),
                denominator=Quantity(
                    value=self.amount_denominator_value,
                    unit=self.amount_denominator_unit,
                    system="http://unitsofmeasure.org",
                    code=self.amount_denominator_code,
                )
            ),
            isActive=True,
        )