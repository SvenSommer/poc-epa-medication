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

let prescriptionCounter = 0;
function addPrescriptionItem() {
    const accordion = document.getElementById('prescriptionAccordion');
    const newItem = createAccordionItem({ id: ++prescriptionCounter });
    accordion.appendChild(newItem);
    updateAccordionSummary(prescriptionCounter);
}

function getPrescriptionDetailsSection(data) {
    const prescriptionIdentifier = IdentifierUtils.generatePrescriptionIdentifier();
    const currentDateTime = DateTimeUtils.getCurrentDateTimeFormatted();

    const inputs = [
        { id: 'rxPrescriptionProcessIdentifier', label: 'Rx Prescription Process Identifier', value: prescriptionIdentifier },
        { id: 'patientReference', label: 'Patient Reference', value: '789' },
        { id: 'authoredOn', label: 'Authored On', value: currentDateTime },
        { id: 'dosageInstructionText', label: 'Dosage Instruction Text', value: '1-0-1' },
        { id: 'substitutionAllowed', label: 'Substitution Allowed', value: true, type: 'checkbox' }
    ];

    return createSection('prescriptionDetails', 'Prescription Details', inputs, data);
}

function getMedicationCodingSection(data) {
    const inputs = [
        { id: 'medicationCode', label: 'Code', value: '08671219' },
        { id: 'medicationDisplay', label: 'Display', value: 'Aciclovir 800 - 1 A Pharma® 35 Tbl. N1' },
        { id: 'medicationSystem', label: 'System', value: 'http://fhir.de/CodeSystem/ifa/pzn' }
    ];

    return createSection('medicationCoding', 'Medication Coding', inputs, data);
}

function getMedicationFormSection(data) {
    const inputs = [
        { id: 'formCode', label: 'Code', value: 'TAB' },
        { id: 'formDisplay', label: 'Display', value: 'Tablette' },
        { id: 'formSystem', label: 'System', value: 'https://fhir.kbv.de/CodeSystem/KBV_CS_SFHIR_KBV_DARREICHUNGSFORM' }
    ];

    return createSection('formCoding', 'Form Coding', inputs, data);
}


function createAccordionItem(data = {}) {
    const item = document.createElement('div');
    item.className = 'card';
    item.innerHTML = `
        <!-- Accordion Header -->
        <div class="card prescription-card" role="tab" id="heading${data.id}">
            <h5 class="mb-0">
                <button class="btn btn-link collapsed" data-toggle="collapse" data-target="#collapse${data.id}" aria-expanded="false" aria-controls="collapse${data.id}">
                    <span id="prescriptionSummaryText${data.id}">Prescription ${data.id || 'New'}</span> <!-- Summary text placeholder -->
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

function attachEventListenersToAccordionItem(item, id) {
    const removeButton = item.querySelector(`#removeButton${id}`);
    removeButton?.addEventListener('click', () => item.remove());

    const collapseElement = item.querySelector(`#collapse${id}`);
    console.log(collapseElement);
    collapseElement?.addEventListener('hidden.bs.collapse', () => {
        console.log(`Collapse for ${id} hidden`);
        updateAccordionSummary(id);
    });
}

function updateAccordionSummary(id) {
    var rxIdentifier = document.getElementById('rxPrescriptionProcessIdentifier' + id).value;
    var medicationCode = document.getElementById('medicationCode' + id).value;
    var medicationDisplay = document.getElementById('medicationDisplay' + id).value;
    var formDisplay = document.getElementById('formDisplay' + id).value;
    var dosageText = document.getElementById('dosageInstructionText' + id).value;

    var summaryText = `
        ${rxIdentifier}, 
        ${medicationDisplay} (${medicationCode}), ${formDisplay}, 
        ${dosageText}
    `;

    document.getElementById(`prescriptionSummaryText${id}`).innerHTML = summaryText;
}


export { addPrescriptionItem };