
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


function getElementValue(id, isCheckbox = false) {
    const element = document.getElementById(id);
    if (!element) {
        console.warn(`Element with ID '${id}' not found.`);
        return isCheckbox ? false : '';
    }
    return isCheckbox ? element.checked : element.value.trim();
}

function createDefaultData(dataPurpose, prefixType, status, identifier = IdentifierUtils.generatePrescriptionIdentifier()) {
    const currentDateTime = DateTimeUtils.getCurrentDateTimeFormatted();
    const sectionTitle = prefixType.charAt(0).toUpperCase() + prefixType.slice(1) + ' Details';
    const idPrefix = prefixType + 'RxPrescriptionProcessIdentifier';

    return {
        purpose: dataPurpose,
        status: status,
        rxPrescriptionProcessIdentifier: identifier,
        purposeDetails: {
            sectionTitle: sectionTitle,
            summaryOrder: [idPrefix, prefixType + 'DosageInstructionText'],
            inputs: createPurposeDetailsInputs(prefixType, identifier, currentDateTime)
        },
        medicationDetails: createMedicationDetails(prefixType),
        formDetails: createFormDetails(prefixType)
    };
}

function getDispenseDefaultData() {

    return createDefaultData('dispensation', 'dispensation', 'draft');
}

function getPrescriptionDefaultData() {

    return createDefaultData('prescription', 'prescription', 'draft');
}

function gatherSentPrescriptionFromInputFields() {
    let data = gatherDataFromInputFields('prescription-card', 'sentPrescription', 'sent', 'prescription', /#prescriptioncollapse|prescriptioncollapse/g, true);
    console.log("gatherSentPrescriptionFromInputFields:", data);
    return data;
}

function gatherDispensationFromPrescriptionInputFields() {
    var dispensations = Array.from(document.querySelectorAll('.prescription-card')).map(item => {
        var id = item.querySelector('.prescription-card button').getAttribute('data-target').replace(/#prescriptioncollapse|prescriptioncollapse/g, '', '');
        const currentDateTime = DateTimeUtils.getCurrentDateTimeFormatted();

        let dispensation = {
            purpose: 'dispensation',
            status: 'draft',
            rxPrescriptionProcessIdentifier: getElementValue('prescriptionRxPrescriptionProcessIdentifier' + id), 
            purposeDetails: {
                sectionTitle: 'Dispensation Details',
                summaryOrder: ['dispensationRxPrescriptionProcessIdentifier', 'dispensationDosageInstructionText'],
                inputs: [
                    { id: 'dispensationRxPrescriptionProcessIdentifier', label: 'Rx Prescription Process Identifier', value: getElementValue('prescriptionRxPrescriptionProcessIdentifier' + id) },
                    { id: 'dispensationPatientReference', label: 'Patient Reference', value: '789' },
                    { id: 'dispensationAuthorizing_prescription_reference', label: 'Authorizing Prescription Reference', value: '123' },
                    { id: 'dispensationWhen_handed_over', label: 'When Handed Over', value: currentDateTime },
                    { id: 'dispensationDosageInstructionText', label: 'Dosage Instruction Text', value: getElementValue('prescriptionDosageInstructionText' + id) },
                    { id: 'dispensationSubstitutionAllowed', label: 'Substitution Allowed', value: getElementValue('prescriptionSubstitutionAllowed' + id, true) }
                ]
            },
            medicationDetails: {
                sectionTitle: 'Medication Details',
                summaryOrder: ['dispensationMedicationCode', 'dispensationMedicationDisplay'],
                inputs: [
                    { id: 'dispensationMedicationCode', label: 'Code', value: getElementValue('prescriptionMedicationCode' + id) },
                    { id: 'dispensationMedicationDisplay', label: 'Display', value: getElementValue('prescriptionMedicationDisplay' + id) },
                    { id: 'dispensationMedicationSystem', label: 'System', value: getElementValue('prescriptionMedicationSystem' + id) }
                ]
            },
            formDetails: {
                sectionTitle: 'Form Details',
                summaryOrder: ['dispensationFormCode', 'dispensationFormDisplay'],
                inputs: [
                    { id: 'dispensationFormCode', label: 'Code', value: getElementValue('prescriptionFormCode' + id) },
                    { id: 'dispensationFormDisplay', label: 'Display', value: getElementValue('prescriptionFormDisplay' + id) },
                    { id: 'dispensationFormSystem', label: 'System', value: getElementValue('prescriptionFormSystem' + id) }
                ]
            }
        };

        return dispensation;

    });
    return dispensations;
}


function gatherDispensationFromDispensationInputFields() {
    let data = gatherDataFromInputFields('dispensation-card', 'sentDispensation', 'sent', 'dispensation', /#dispensationcollapse|dispensationcollapse/g, true);
    console.log("gatherDispensationFromDispensationInputFields:", data);
    return data;
}

function gatherDataFromInputFields(cardClass, dataPurpose, status, prefixType, regex, deleteItem = false) {
    return Array.from(document.querySelectorAll('.' + cardClass)).map(item => {
        const idSuffix = item.querySelector('.' + cardClass + ' button').getAttribute('data-target').replace(regex, '');
        const data = createDefaultData(dataPurpose, prefixType, status, getElementValue(prefixType + 'RxPrescriptionProcessIdentifier' + idSuffix));

        // Update purpose details
        data.purposeDetails.inputs.forEach(input => {
            input.value = getElementValue(input.id + idSuffix, input.type === 'checkbox');
        });

        // Update medication details
        data.medicationDetails.inputs.forEach(input => {
            input.value = getElementValue(input.id + idSuffix);
        });

        // Update form details
        data.formDetails.inputs.forEach(input => {
            input.value = getElementValue(input.id + idSuffix);
        });

        if (deleteItem) {
            item.remove();
        }

        return data;
    });
}

function createPurposeDetailsInputs(type, identifier, currentDateTime) {
    let inputs = [
        { id: `${type}RxPrescriptionProcessIdentifier`, label: 'Rx Prescription Process Identifier', value: identifier },
        { id: `${type}DosageInstructionText`, label: 'Dosage Instruction Text', value: '1-0-1' }
    ];

    if (type === 'dispensation') {
        inputs = inputs.concat([
            { id: 'dispensationPatientReference', label: 'Patient Reference', value: '789' },
            { id: 'dispensationAuthorizing_prescription_reference', label: 'Authorizing Prescription Reference', value: '123' },
            { id: 'dispensationWhen_handed_over', label: 'When Handed Over', value: currentDateTime },
            { id: 'dispensationSubstitutionAllowed', label: 'Substitution Allowed', value: true, type: 'checkbox' }
        ]);
    } else if (type === 'prescription') {
        inputs = inputs.concat([
            { id: 'prescriptionPatientReference', label: 'Patient Reference', value: '789' },
            { id: 'prescriptionAuthoredOn', label: 'Authored On', value: currentDateTime },
            { id: 'prescriptionSubstitutionAllowed', label: 'Substitution Allowed', value: true, type: 'checkbox' }
        ]);
    }

    return inputs;
}

function createMedicationDetails(type) {
    const idPrefix = type + 'Medication';
    return {
        sectionTitle: 'Medication Details',
        summaryOrder: [idPrefix + 'Code', idPrefix + 'Display', idPrefix + 'FormDisplay'],
        inputs: [
            { id: idPrefix + 'Code', label: 'Code', value: '08671219' },
            { id: idPrefix + 'Display', label: 'Display', value: 'Aciclovir 800 - 1 A Pharma® 35 Tbl. N1' },
            { id: idPrefix + 'System', label: 'System', value: 'http://fhir.de/CodeSystem/ifa/pzn' }
        ]
    };
}

function createFormDetails(type) {
    const idPrefix = type + 'Form';
    return {
        sectionTitle: 'Form Details',
        summaryOrder: [idPrefix + 'Code', idPrefix + 'Display'],
        inputs: [
            { id: idPrefix + 'Code', label: 'Code', value: 'TAB' },
            { id: idPrefix + 'Display', label: 'Display', value: 'Tablette' },
            { id: idPrefix + 'System', label: 'System', value: 'https://fhir.kbv.de/CodeSystem/KBV_CS_SFHIR_KBV_DARREICHUNGSFORM' }
        ]
    };
}










export { getDispenseDefaultData, getPrescriptionDefaultData, gatherSentPrescriptionFromInputFields, gatherDispensationFromPrescriptionInputFields, gatherDispensationFromDispensationInputFields }