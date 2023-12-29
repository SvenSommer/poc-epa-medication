from datetime import datetime


class MedicationRequestInfo:
    def __init__(
        self,
        medication_reference: str,
        rxPrescriptionProcessIdentifier: str,
        patient_reference: str,
        authoredOn: datetime,
        dosage_instruction_text: str,
        substitution_allowed: bool
    ):
        self.medication_reference = medication_reference
        self.rxPrescriptionProcessIdentifier = rxPrescriptionProcessIdentifier
        self.patient_reference = patient_reference
        self.authoredOn = authoredOn
        self.dosage_instruction_text = dosage_instruction_text
        self.substitution_allowed = substitution_allowed