class PrescriptionInfo:
    def __init__(self, rxPrescriptionProcessIdentifier, medication_request_info, medication_info, organization_info, practitioner_info):
        self.rxPrescriptionProcessIdentifier = rxPrescriptionProcessIdentifier
        self.medication_request_info = medication_request_info
        self.medication_info = medication_info
        self.organization_info = organization_info
        self.practitioner_info = practitioner_info