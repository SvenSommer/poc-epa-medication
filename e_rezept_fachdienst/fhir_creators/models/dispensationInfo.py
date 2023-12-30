class DispensationInfo:
    def __init__(self, rxPrescriptionProcessIdentifier, medication_dispense_info, medication_info, organization_info):
        self.rxPrescriptionProcessIdentifier = rxPrescriptionProcessIdentifier
        self.medication_dispense_info = medication_dispense_info
        self.medication_info = medication_info
        self.organization_info = organization_info