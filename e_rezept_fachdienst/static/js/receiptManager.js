import { createSection } from "./accordionManager.js";
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
        purposeDetails: {
            sectionTitle: 'Prescription Details',
            summaryOrder: ['prescriptionRxPrescriptionProcessIdentifier','prescriptionDosageInstructionText'],
            inputs: [
                { id: 'prescriptionRxPrescriptionProcessIdentifier', label: 'Rx Prescription Process Identifier', value: prescriptionIdentifier },
                { id: 'prescriptionPatientReference', label: 'Patient Reference', value: '789' },
                { id: 'prescriptionAuthoredOn', label: 'Authored On', value: currentDateTime },
                { id: 'prescriptionDosageInstructionText', label: 'Dosage Instruction Text', value: '1-0-1' },
                { id: 'prescriptionSubstitutionAllowed', label: 'Substitution Allowed', value: true, type: 'checkbox' }
            ] ,
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

let objectCounter = {};

function addReceiptItem(target, data) {
    if (!target) {
        console.error('No target provided for prescription item');
        return;
    }
    if (!data) {
        console.error('No data provided for prescription item');
        return;
    }

    if (!objectCounter[target]) {
        objectCounter[target] = 0;
    }

    const accordion = document.getElementById(target);
    data.id = ++objectCounter[target];
    console.log(`Adding with id: ${data.id} for target: ${target}`);

    const newItem = createAccordionItem(data);
    newItem.data = data;
    accordion.appendChild(newItem);
    updateAccordionSummary(data);
}




function createAccordionItem(data = {}) {
    const item = document.createElement('div');
    item.className = 'card';
    item.innerHTML = `
        <!-- Accordion Header -->
        <div class="card ${data.purpose}-card" role="tab" id="heading${data.id}">
            <h5 class="mb-0">
                <button class="btn btn-link collapsed" data-toggle="collapse" data-target="#collapse${data.id}" aria-expanded="false" aria-controls="collapse${data.id}">
                    <span id="${data.purpose}SummaryText${data.id}">Prescription ${data.id || 'New'}</span> <!-- Summary text placeholder -->
                </button>
                <button class="btn btn-danger remove-button" id="removeButton${data.id}">
                    <i class="fas fa-trash"></i>
                </button>
            </h5>
        </div>

        <!-- Accordion Body -->
        <div id="collapse${data.id}" class="collapse" role="tabpanel" aria-labelledby="heading${data.id}" data-parent="#prescriptionAccordion">
            <div class="card-body">
                <!-- Prescription Details Section -->
                ${getPrescriptionDetailsSection(data)}
                <!-- Medication Coding Section -->
                ${getMedicationCodingSection(data)}
                <!-- Medication Form Section -->
                ${getMedicationFormSection(data)}
                
            </div>
        </div>
    `;
    attachEventListenersToAccordionItem(item, data.id);
    return item;
}

function getPrescriptionDetailsSection(data) {
    const inputs = data.purposeDetails.inputs;
    return createSection('purposeDetails', data.purposeDetails.sectionTitle, inputs, data);
}


function getMedicationCodingSection(data) {
    const inputs = data.medicationDetails.inputs;
    return createSection('medicationDetails',  data.medicationDetails.sectionTitle, inputs, data);
}

function getMedicationFormSection(data) {
    const inputs = data.formDetails.inputs;
    return createSection('formDetails', data.formDetails.sectionTitle, inputs, data);
}

function attachEventListenersToAccordionItem(item, id) {
    const removeButton = item.querySelector(`#removeButton${id}`);
    removeButton?.addEventListener('click', () => item.remove());

    const collapseElement = item.querySelector(`#collapse${id}`);
    collapseElement?.addEventListener('hidden.bs.collapse', () => {
        console.log(`Collapse for ${id} hidden`);
        updateAccordionSummary(id);
    });
}

function updateAccordionSummary(data) {
    let summaryElements = [];
    for (const sectionKey in data) {
        const section = data[sectionKey];
        if (section.summaryOrder) {
            section.summaryOrder.forEach(inputId => {
                const inputElement = section.inputs.find(input => input.id === inputId);
                if (inputElement) {
                    let elementValue = document.getElementById(inputElement.id + data.id).value;
                    summaryElements.push(elementValue);
                }
            });
        }
    }

    var summaryText = summaryElements.join(', ');
    // document.getElementById(`${data.organisationName}SummaryText${data.id}`).innerHTML = summaryText;
    document.getElementById(`${data.purpose}SummaryText${data.id}`).innerHTML = summaryText;
}

function updateSentPrescriptionsUI(successfulPrescriptions) {
    const sentPrescriptionsContainer = document.getElementById('sentPrescriptions');
    sentPrescriptionsContainer.innerHTML = ''; // Clear existing content

    successfulPrescriptions.forEach((prescription, index) => {
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = 'prescription-' + index;
        checkbox.value = prescription;

        const label = document.createElement('label');
        label.htmlFor = 'prescription-' + index;
        label.appendChild(document.createTextNode(prescription));

        const div = document.createElement('div');
        div.appendChild(checkbox);
        div.appendChild(label);

        sentPrescriptionsContainer.appendChild(div);
    });
}

// Function to handle the cancellation of selected prescriptions
function cancelSelectedPrescriptions() {
    const selectedPrescriptions = [];
    document.querySelectorAll('#sentPrescriptions input[type="checkbox"]:checked').forEach(checkbox => {
        selectedPrescriptions.push(checkbox.value);
    });

    // Logic to cancel the selected prescriptions
    console.log("Canceling prescriptions:", selectedPrescriptions);
    // Implement cancellation logic here
}

// Event listener for the Cancel Prescription button
document.getElementById('cancelPrescription').addEventListener('click', cancelSelectedPrescriptions);

export {addReceiptItem, getPrescriptionDefaultData, getDispenseDefaultData, updateSentPrescriptionsUI };