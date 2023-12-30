import { createSection } from "./accordionManager.js";

let organisationCounter = 0;
function addOrganisation() {
    const accordion = document.getElementById('organisationAccordion');
    const newItem = createAccordionItem({ id: ++organisationCounter });
    accordion.appendChild(newItem);
    updateAccordionSummary(organisationCounter);
}


function createAccordionItem(data = {}) {
    const item = document.createElement('div');
    item.className = 'card';
    item.innerHTML = `
        <!-- Accordion Header -->
        <div class="card organization-card" role="tab" id="heading${data.id}">
            <h5 class="mb-0">
                <button class="btn btn-link collapsed" data-toggle="collapse" data-target="#collapse${data.id}" aria-expanded="false" aria-controls="collapse${data.id}">
                    <span id="OrganisationSummaryText${data.id}">Organisation ${data.id || 'New'}</span> <!-- Summary text placeholder -->
                </button>
            </h5>
        </div>

        <!-- Accordion Body -->
        <div id="collapse${data.id}" class="collapse" role="tabpanel" aria-labelledby="heading${data.id}" data-parent="#organisationAccordion">
            <div class="card-body">
                <!-- Organisation Identifer Section -->
                ${getOrganisationIdentifierSection(data)}       
                <!-- Organisation Details Section -->
                ${getOrganisationContactSection(data)}           
            </div>
        </div>
    `

    return item;
}

function getOrganisationIdentifierSection(data) { 
    const inputs = [
        { id: 'orgTelematikId', label: 'Telematik ID', value: '2-2.58.00000040' },
        { id: 'orgTypeCode', label: 'Organization Type Code', value: '1.2.276.0.76.4.51' },
        { id: 'orgTypeDisplay', label: 'Organization Type Display', value: 'Zahnarztpraxis' },
    ];

    return createSection('organizationIdentifierDetails', 'Organization Identifiers', inputs, data);
}

function getOrganisationContactSection(data) { 
    const inputs = [
        { id: 'orgName', label: 'Organization Name', value: 'Zahnarztpraxis Dr. Mustermann' },
        { id: 'orgAlias', label: 'Organization Alias', value: 'Zahnarztpraxis am Bahnhof' },
        { id: 'contactName', label: 'Contact Name', value: 'Empfang Zahnarztpraxis Dr. Mustermann' },
        { id: 'phone', label: 'Phone', value: '030 1234567' }
    ];

    return createSection('organizationContactDetails', 'Organization Contact Informations', inputs, data);
}

function updateAccordionSummary(id) {
    var orgTelematikId = document.getElementById('orgTelematikId' + id).value;
    var orgTypeDisplay = document.getElementById('orgTypeDisplay' + id).value;
    var orgName = document.getElementById('orgName' + id).value;
    var phone = document.getElementById('phone' + id).value;

    var summaryText = `
        ${orgTelematikId}, 
        ${orgTypeDisplay}, 
        ${orgName}, 
        ${phone}
    `;

    // Assuming you want to update a specific element with the organization summary
    // Replace 'organizationSummary' with the actual ID of the element where the summary should be displayed
    document.getElementById(`OrganisationSummaryText${id}`).innerHTML = summaryText;
}



export { addOrganisation }