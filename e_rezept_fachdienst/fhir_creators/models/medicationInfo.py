from e_rezept_fachdienst.fhir_creators.models.codingObject import CodingObject
from e_rezept_fachdienst.fhir_creators.models.ingredient import Ingredient


from typing import List, Optional


class MedicationInfo:
    def __init__(
        self,
        rxPrescriptionProcessIdentifier: str,
        medication_coding: CodingObject,
        form_coding: Optional[CodingObject] = None,
        ingredients: Optional[List[Ingredient]] = None
    ):
        self.rxPrescriptionProcessIdentifier = rxPrescriptionProcessIdentifier
        self.medication_coding = medication_coding
        self.form_coding = form_coding
        self.ingredients = ingredients