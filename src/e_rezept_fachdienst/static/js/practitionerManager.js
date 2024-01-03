import { createSection } from "./accordionManager.js";

let practitionerCounter = 0;
function addPractitioner() {
    const accordion = document.getElementById('practitionerAccordion');
    const newItem = createAccordionItem({ id: ++practitionerCounter });
    accordion.appendChild(newItem);
    updateAccordionSummary(practitionerCounter);
}

function createAccordionItem(data = {}) {
    const item = document.createElement('div');
    item.className = 'card';
    item.innerHTML = `
        <!-- Accordion Header -->
        <div class="card practitioner-card" role="tab" id="heading${data.id}">
            <h5 class="mb-0">
                <button class="btn btn-link collapsed" data-toggle="collapse" data-target="#collapse${data.id}" aria-expanded="false" aria-controls="collapse${data.id}">
                    <span id="PractitionerSummaryText${data.id}">Practitioner ${data.id || 'New'}</span> <!-- Summary text placeholder -->
                </button>
            </h5>
        </div>

        <!-- Accordion Body -->
        <div id="collapse${data.id}" class="collapse" role="tabpanel" aria-labelledby="heading${data.id}" data-parent="#practitionerAccordion">
            <div class="card-body">
                <!-- Practitioner Identifer Section -->
                ${getPractitionerIdentifierSection(data)}       
                <!-- Practitioner Details Section -->
                ${getPractitionerContactSection(data)}           
            </div>
        </div>
    `

    return item;
}

function getPractitionerIdentifierSection(data) {
    const inputs = [
        { id: 'practTelematikId', label: 'Telematik ID', value: '1-1.58.00000040' },
        { id: 'practAnr', label: 'ANR', value: '123456789' }
    ];

    return createSection('practitionerIdentifierDetails', 'Practitioner Identifier', inputs, data);
}

function getPractitionerContactSection(data) {
    const inputs = [
        { id: 'practNameText', label: 'Name Text', value: 'Dr. Max Manfred Mustermann' },
        { id: 'practFamily', label: 'Family Name', value: 'Mustermann' },
        { id: 'practGiven', label: 'Given Names', value: 'Max, Manfred' }, // Combining the given names into one field
        { id: 'practPrefix', label: 'Prefix', value: 'Dr.' },
        { id: 'practQualifications', label: 'Qualifications', value: 'Various' } // Representing qualifications as a single field for simplicity
    ];

    return createSection('practitionerContactDetails', 'Practitioner Contact Information', inputs, data);
}

function updateAccordionSummary(id) {
    var telematikId = document.getElementById('practTelematikId' + id).value;
    var nameText = document.getElementById('practNameText' + id).value;
    var family = document.getElementById('practFamily' + id).value;
    var prefix = document.getElementById('practPrefix' + id).value;

    var summaryText = `
       ${telematikId}, ${prefix} ${nameText} (${family})`;

    document.getElementById(`PractitionerSummaryText${id}`).innerHTML = summaryText;
}

export { addPractitioner }