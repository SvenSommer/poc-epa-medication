
const DateTimeUtils = {
    getCurrentDateTimeFormatted() {
        const now = new Date();
        return now.toISOString().slice(0, 19).replace('T', ' '); // YYYY-MM-DD HH:MM:SS
    },
    getCurrentDateFormatted() {
        const now = new Date();
        return now.toISOString().slice(0, 10).replace(/-/g, ''); // YYYYMMDD
    }
};
const IdentifierUtils = {
    generateBaseIdentifier() {
        const prefix = "160.";
        const segments = new Array(4).fill(null).map(() => Math.floor(Math.random() * 900 + 100));
        return prefix + segments.join('.') + '_';
    },
    generatePrescriptionIdentifier() {
        return this.generateBaseIdentifier() + DateTimeUtils.getCurrentDateFormatted();
    }
};
function getDispenseDefaultData() {
    const dispenseIdentifier = IdentifierUtils.generateBaseIdentifier();
    const currentDateTime = DateTimeUtils.getCurrentDateTimeFormatted();

    return {
        purpose: 'dispensation',
        status: 'draft',
        rxPrescriptionProcessIdentifier: dispenseIdentifier, 
        purposeDetails: {
            sectionTitle: 'Dispensation Details',
            summaryOrder: ['dispensationRxPrescriptionProcessIdentifier', 'dispensationDosageInstructionText'],
            inputs: [
                { id: 'dispensationRxPrescriptionProcessIdentifier', label: 'Rx Prescription Process Identifier', value: dispenseIdentifier },
                { id: 'dispensationPatientReference', label: 'Patient Reference', value: '789' },
                { id: 'dispensationAuthorizing_prescription_reference', label: 'Authorizing Prescription Reference', value: '123' },
                { id: 'dispensationWhen_handed_over', label: 'When Handed Over', value: currentDateTime },
                { id: 'dispensationDosageInstructionText', label: 'Dosage Instruction Text', value: '1-0-1' },
                { id: 'dispensationSubstitutionAllowed', label: 'Substitution Allowed', value: true, type: 'checkbox' }
            ]
        },
        medicationDetails: {
            sectionTitle: 'Medication Details',
            summaryOrder: ['dispensationMedicationCode', 'dispensationMedicationDisplay', 'dispensationFormDisplay'],
            inputs: [
                { id: 'dispensationMedicationCode', label: 'Code', value: '08671219' },
                { id: 'dispensationMedicationDisplay', label: 'Display', value: 'Aciclovir 800 - 1 A Pharma® 35 Tbl. N1' },
                { id: 'dispensationMedicationSystem', label: 'System', value: 'http://fhir.de/CodeSystem/ifa/pzn' }
            ]
        },
        formDetails: {
            sectionTitle: 'Form Details',
            summaryOrder: ['dispensationFormCode', 'dispensationFormDisplay'],
            inputs: [
                { id: 'dispensationFormCode', label: 'Code', value: 'TAB' },
                { id: 'dispensationFormDisplay', label: 'Display', value: 'Tablette' },
                { id: 'dispensationFormSystem', label: 'System', value: 'https://fhir.kbv.de/CodeSystem/KBV_CS_SFHIR_KBV_DARREICHUNGSFORM' }
            ]
        }
    };
}
function getPrescriptionDefaultData() {
    const prescriptionIdentifier = IdentifierUtils.generatePrescriptionIdentifier();
    const currentDateTime = DateTimeUtils.getCurrentDateTimeFormatted();

    return {
        purpose: 'prescription',
        status: 'draft',
        rxPrescriptionProcessIdentifier: prescriptionIdentifier, 
        purposeDetails: {
            sectionTitle: 'Prescription Details',
            summaryOrder: ['prescriptionRxPrescriptionProcessIdentifier', 'prescriptionDosageInstructionText'],
            inputs: [
                { id: 'prescriptionRxPrescriptionProcessIdentifier', label: 'Rx Prescription Process Identifier', value: prescriptionIdentifier },
                { id: 'prescriptionPatientReference', label: 'Patient Reference', value: '789' },
                { id: 'prescriptionAuthoredOn', label: 'Authored On', value: currentDateTime },
                { id: 'prescriptionDosageInstructionText', label: 'Dosage Instruction Text', value: '1-0-1' },
                { id: 'prescriptionSubstitutionAllowed', label: 'Substitution Allowed', value: true, type: 'checkbox' }
            ],
        },
        medicationDetails: {
            sectionTitle: 'Medication Details',
            summaryOrder: ['prescriptionMedicationCode', 'prescriptionMedicationDisplay', 'prescriptionFormDisplay'],
            inputs: [
                { id: 'prescriptionMedicationCode', label: 'Code', value: '08671219' },
                { id: 'prescriptionMedicationDisplay', label: 'Display', value: 'Aciclovir 800 - 1 A Pharma® 35 Tbl. N1' },
                { id: 'prescriptionMedicationSystem', label: 'System', value: 'http://fhir.de/CodeSystem/ifa/pzn' }
            ]
        },
        formDetails: {
            sectionTitle: 'Form Details',
            summaryOrder: ['prescriptionFormCode', 'prescriptionFormDisplay'],
            inputs: [
                { id: 'prescriptionFormCode', label: 'Code', value: 'TAB' },
                { id: 'prescriptionFormDisplay', label: 'Display', value: 'Tablette' },
                { id: 'prescriptionFormSystem', label: 'System', value: 'https://fhir.kbv.de/CodeSystem/KBV_CS_SFHIR_KBV_DARREICHUNGSFORM' }
            ]
        }
    };
}

function getValue(id, logError = false) {
    const element = document.getElementById(id);
    if (!element) {
        const message = `Element with ID '${id}' not found.`;
        logError ? console.error(message) : console.warn(message);
        return '';
    }

    const value = element.value.trim();
    if (value === '') {
        const message = `Value for element with ID '${id}' is empty.`;
        logError ? console.error(message) : console.warn(message);
    }

    return value;
}

function getCheckedValue(id) {
    const element = document.getElementById(id);
    if (!element) {
        const message = `Element with ID '${id}' not found.`;
        logError ? console.error(message) : console.warn(message);
        return '';
    }
    return element.checked || false;
}


function gatherSentPrescriptionFromInputFields() {
    var prescriptions = Array.from(document.querySelectorAll('.prescription-card')).map(item => {
        var id = item.querySelector('.prescription-card button').getAttribute('data-target').replace(/#prescriptioncollapse|prescriptioncollapse/g, '');

        let prescription = {
            purpose: 'sentPrescription',
            status: 'sent',
            rxPrescriptionProcessIdentifier: getValue('prescriptionRxPrescriptionProcessIdentifier' + id),
            purposeDetails: {
                sectionTitle: 'Prescription Details',
                summaryOrder: ['prescriptionRxPrescriptionProcessIdentifier', 'prescriptionDosageInstructionText'],
                inputs: [
                    { id: 'prescriptionRxPrescriptionProcessIdentifier', label: 'Rx Prescription Process Identifier', value: getValue('prescriptionRxPrescriptionProcessIdentifier' + id) },
                    { id: 'prescriptionPatientReference', label: 'Patient Reference', value: getValue('prescriptionPatientReference' + id) },
                    { id: 'prescriptionAuthoredOn', label: 'Authored On', value: getValue('prescriptionAuthoredOn' + id) },
                    { id: 'prescriptionDosageInstructionText', label: 'Dosage Instruction Text', value: getValue('prescriptionDosageInstructionText' + id) },
                    { id: 'prescriptionSubstitutionAllowed', label: 'Substitution Allowed', value: getCheckedValue('prescriptionSubstitutionAllowed' + id), type: 'checkbox' }
                ],
            },
            medicationDetails: {
                sectionTitle: 'Medication Details',
                summaryOrder: ['prescriptionMedicationCode', 'prescriptionMedicationDisplay', 'prescriptionFormDisplay'],
                inputs: [
                    { id: 'prescriptionMedicationCode', label: 'Code', value: getValue('prescriptionMedicationCode' + id) },
                    { id: 'prescriptionMedicationDisplay', label: 'Display', value: getValue('prescriptionMedicationDisplay' + id) },
                    { id: 'prescriptionMedicationSystem', label: 'System', value: getValue('prescriptionMedicationSystem' + id) }
                ]
            },
            formDetails: {
                sectionTitle: 'Form Details',
                summaryOrder: ['prescriptionFormCode', 'prescriptionFormDisplay'],
                inputs: [
                    { id: 'prescriptionFormCode', label: 'Code', value: getValue('prescriptionFormCode' + id) },
                    { id: 'prescriptionFormDisplay', label: 'Display', value: getValue('prescriptionFormDisplay' + id) },
                    { id: 'prescriptionFormSystem', label: 'System', value: getValue('prescriptionFormSystem' + id) }
                ]
            }
        };

        item.remove();
        return prescription;
    });
    return prescriptions;
}

function gatherDispensationFromPrescriptionInputFields() {
    var dispensations = Array.from(document.querySelectorAll('.prescription-card')).map(item => {
        var id = item.querySelector('.prescription-card button').getAttribute('data-target').replace(/#prescriptioncollapse|prescriptioncollapse/g, '');
        const currentDateTime = DateTimeUtils.getCurrentDateTimeFormatted();

        let dispensation = {
            purpose: 'dispensation',
            status: 'draft',
            rxPrescriptionProcessIdentifier: getValue('prescriptionRxPrescriptionProcessIdentifier' + id), 
            purposeDetails: {
                sectionTitle: 'Dispensation Details',
                summaryOrder: ['dispensationRxPrescriptionProcessIdentifier', 'dispensationDosageInstructionText'],
                inputs: [
                    { id: 'dispensationRxPrescriptionProcessIdentifier', label: 'Rx Prescription Process Identifier', value: getValue('prescriptionRxPrescriptionProcessIdentifier' + id) },
                    { id: 'dispensationPatientReference', label: 'Patient Reference', value: '789' },
                    { id: 'dispensationAuthorizing_prescription_reference', label: 'Authorizing Prescription Reference', value: '123' },
                    { id: 'dispensationWhen_handed_over', label: 'When Handed Over', value: currentDateTime },
                    { id: 'dispensationDosageInstructionText', label: 'Dosage Instruction Text', value: getValue('prescriptionDosageInstructionText' + id) },
                    { id: 'dispensationSubstitutionAllowed', label: 'Substitution Allowed', value: getCheckedValue('prescriptionSubstitutionAllowed' + id), type: 'checkbox' }
                ]
            },
            medicationDetails: {
                sectionTitle: 'Medication Details',
                summaryOrder: ['dispensationMedicationCode', 'dispensationMedicationDisplay'],
                inputs: [
                    { id: 'dispensationMedicationCode', label: 'Code', value: getValue('prescriptionMedicationCode' + id) },
                    { id: 'dispensationMedicationDisplay', label: 'Display', value: getValue('prescriptionMedicationDisplay' + id) },
                    { id: 'dispensationMedicationSystem', label: 'System', value: getValue('prescriptionMedicationSystem' + id) }
                ]
            },
            formDetails: {
                sectionTitle: 'Form Details',
                summaryOrder: ['dispensationFormCode', 'dispensationFormDisplay'],
                inputs: [
                    { id: 'dispensationFormCode', label: 'Code', value: getValue('prescriptionFormCode' + id) },
                    { id: 'dispensationFormDisplay', label: 'Display', value: getValue('prescriptionFormDisplay' + id) },
                    { id: 'dispensationFormSystem', label: 'System', value: getValue('prescriptionFormSystem' + id) }
                ]
            }
        };

        return dispensation;

    });
    return dispensations;
}

function gatherDispensationFromDispensationInputFields() {
    let dispensations = Array.from(document.querySelectorAll('.dispensation-card')).map(item => {
        var id = item.querySelector('.dispensation-card button').getAttribute('data-target').replace(/#dispensationcollapse|dispensationcollapse/g, '');

        let dispensation = {
            purpose: 'sentDispensation',
            status: 'sent',
            rxPrescriptionProcessIdentifier: getValue('dispensationRxPrescriptionProcessIdentifier' + id), 
            purposeDetails: {
                sectionTitle: 'Dispensation Details',
                summaryOrder: ['dispensationRxPrescriptionProcessIdentifier', 'dispensationDosageInstructionText'],
                inputs: [
                    { id: 'dispensationRxPrescriptionProcessIdentifier', label: 'Rx Prescription Process Identifier', value: getValue('dispensationRxPrescriptionProcessIdentifier' + id) },
                    { id: 'dispensationPatientReference', label: 'Patient Reference', value: getValue('dispensationPatientReference' + id) },
                    { id: 'dispensationAuthorizing_prescription_reference', label: 'Authorizing Prescription Reference', value: getValue('dispensationAuthorizing_prescription_reference' + id) },
                    { id: 'dispensationWhen_handed_over', label: 'When Handed Over', value: getValue('dispensationWhen_handed_over' + id) },
                    { id: 'dispensationDosageInstructionText', label: 'Dosage Instruction Text', value: getValue('dispensationDosageInstructionText' + id) },
                    { id: 'dispensationSubstitutionAllowed', label: 'Substitution Allowed', value: getCheckedValue('dispensationSubstitutionAllowed' + id), type: 'checkbox' }
                ]
            },
            medicationDetails: {
                sectionTitle: 'Medication Details',
                summaryOrder: ['dispensationMedicationCode', 'dispensationMedicationDisplay'],
                inputs: [
                    { id: 'dispensationMedicationCode', label: 'Code', value: getValue('dispensationMedicationCode' + id) },
                    { id: 'dispensationMedicationDisplay', label: 'Display', value: getValue('dispensationMedicationDisplay' + id) },
                    { id: 'dispensationMedicationSystem', label: 'System', value: getValue('dispensationMedicationSystem' + id) }
                ]
            },
            formDetails: {
                sectionTitle: 'Form Details',
                summaryOrder: ['dispensationFormCode', 'dispensationFormDisplay'],
                inputs: [
                    { id: 'dispensationFormCode', label: 'Code', value: getValue('dispensationFormCode' + id) },
                    { id: 'dispensationFormDisplay', label: 'Display', value: getValue('dispensationFormDisplay' + id) },
                    { id: 'dispensationFormSystem', label: 'System', value: getValue('dispensationFormSystem' + id) }
                ]
            }
        };
        item.remove();
        return dispensation;
    });
    return dispensations;
}




export { getDispenseDefaultData, getPrescriptionDefaultData, gatherSentPrescriptionFromInputFields, gatherDispensationFromPrescriptionInputFields, gatherDispensationFromDispensationInputFields }