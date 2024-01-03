from datetime import datetime


class MedicationDispenseInfo:
    def __init__(
        self,
        rxPrescriptionProcessIdentifier: str,
        medication_reference: str,
        patient_identifier: str,
        performer_organization_reference: str,
        authorizing_prescription_reference: str,
        when_handed_over: datetime,
        dosage_instruction_text: str,
        substitution_allowed: bool
    ):
        self.rxPrescriptionProcessIdentifier = rxPrescriptionProcessIdentifier
        self.medication_reference = medication_reference
        self.patient_identifier = patient_identifier
        self.performer_organization_reference = performer_organization_reference
        self.authorizing_prescription_reference = authorizing_prescription_reference
        self.when_handed_over = when_handed_over
        self.dosage_instruction_text = dosage_instruction_text
        self.substitution_allowed = substitution_allowed