import { createSection } from "./accordionManager.js";
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

    const newItem = createAccordionItem(data);
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
                <button class="btn btn-link collapsed" data-toggle="collapse" data-target="#${data.purpose}collapse${data.id}" aria-expanded="false" aria-controls="${data.purpose}collapse${data.id}">
                    <span id="${data.purpose}SummaryText${data.id}">Prescription ${data.id || 'New'}</span> <!-- Summary text placeholder -->
                </button>
                ${data.status === 'sent' ? 
                    `<input type="checkbox" class="checkbox-button" id="checkbox${data.id}" data-rxPrescriptionProcessIdentifier="${data.rxPrescriptionProcessIdentifier}" data-purpose="${data.purpose}">` :
                    `<button class="btn btn-danger remove-button" id="removeButton${data.id}">
                        <i class="fas fa-trash"></i>
                    </button>`
                }
            </h5>
        </div>

        <!-- Accordion Body -->
        <div id="${data.purpose}collapse${data.id}" class="collapse" role="tabpanel" aria-labelledby="heading${data.id}" data-parent="#prescriptionAccordion">
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
    document.getElementById(`${data.purpose}SummaryText${data.id}`).innerHTML = summaryText;
}

export {addReceiptItem };