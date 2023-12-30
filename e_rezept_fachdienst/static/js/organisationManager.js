import { createSection } from "./accordionManager.js";

function getDefaultDoctorOrganisationData() {
    return {
        id: 1,
        organisationName: 'practitionerOrganisation',
        organizationIdentifierDetails: {
            sectionTitle: 'Organization Identifiers',
            summaryOrder: ['doctorOrgTelematikId', 'doctorOrgTypeDisplay'],
            inputs: [
                { id: 'doctorOrgTelematikId', label: 'Telematik ID', value: '2-2.58.00000040' },
                { id: 'doctorOrgTypeCode', label: 'Organization Type Code', value: '1.2.276.0.76.4.51' },
                { id: 'doctorOrgTypeDisplay', label: 'Organization Type Display', value: 'Zahnarztpraxis' }
            ]
        },
        organizationContactDetails: {
            sectionTitle: 'Organization Contact Informations',
            summaryOrder: ['doctorOrgName', 'doctorOrgPhone'], // specify the IDs for the summary
            inputs: [
                { id: 'doctorOrgName', label: 'Organization Name', value: 'Zahnarztpraxis Dr. Mustermann' },
                { id: 'doctorOrgAlias', label: 'Organization Alias', value: 'Zahnarztpraxis am Bahnhof' },
                { id: 'doctorOrgContactName', label: 'Contact Name', value: 'Empfang Zahnarztpraxis Dr. Mustermann' },
                { id: 'doctorOrgPhone', label: 'Phone', value: '030 1234567' }
            ]
        }
    };
}

function getDefaultFarmacyOrganisationData() {
    return {
        id: 1,
        organisationName: 'farmacyOrganisation',
        organizationIdentifierDetails: {
            sectionTitle: 'Organization Identifiers',
            summaryOrder: ['farmacyOrgTelematikId', 'farmacyOrgTypeDisplay'], // specify the IDs for the summary
            inputs: [
                { id: 'farmacyOrgTelematikId', label: 'Telematik ID', value: '1-2.58.00000040' },
                { id: 'farmacyOrgTypeCode', label: 'Organization Type Code', value: '2.2.276.0.76.4.51' },
                { id: 'farmacyOrgTypeDisplay', label: 'Organization Type Display', value: 'Apotheke' }
            ]
        },
        organizationContactDetails: {
            sectionTitle: 'Organization Contact Informations',
            summaryOrder: ['farmacyOrgName', 'farmacyOrgPhone'], // specify the IDs for the summary
            inputs: [
                { id: 'farmacyOrgName', label: 'Organization Name', value: 'Apotheke am Park' },
                { id: 'farmacyOrgAlias', label: 'Organization Alias', value: 'Apotheke zu grünen Lunge' },
                { id: 'farmacyOrgContactName', label: 'Contact Name', value: 'Schalter 1' },
                { id: 'farmacyOrgPhone', label: 'Phone', value: '030 75165484' }
            ]
        }
    };
}



function addOrganisation( data = {}) {
    const accordion = document.getElementById(data.organisationName + "Accordion");
    const newItem = createAccordionItem(data);
    accordion.appendChild(newItem);
    updateAccordionSummary(data);
}

function createAccordionItem(data = {}) {
    const item = document.createElement('div');
    item.className = 'card';
    item.innerHTML = `
        <!-- Accordion Header -->
        <div class="card-header" role="tab" id="heading${data.organisationName}${ data.id}">
            <h5 class="mb-0">
                <button class="btn btn-link collapsed" data-toggle="collapse" data-target="#collapse${data.organisationName}${ data.id}" aria-expanded="false" aria-controls="collapse${data.organisationName}${ data.id}">
                    <span id="${data.organisationName}SummaryText${ data.id}">Organisation ${ data.id}</span>
                </button>
            </h5>
        </div>
        <!-- Accordion Body -->
        <div id="collapse${data.organisationName}${ data.id}" class="collapse" role="tabpanel" aria-labelledby="heading${data.organisationName}${ data.id}" data-parent="#${data.organisationName}Accordion"}">
            <div class="card-body">
                ${getOrganisationIdentifierSection(data)}       
                ${getOrganisationContactSection(data)}           
            </div>
        </div>
    `;

    return item;
}


function getOrganisationIdentifierSection(data) {
    const inputs = data.organizationIdentifierDetails.inputs;
    return createSection('IdentifierDetails', 'Organization Identifiers', inputs, data);
}

function getOrganisationContactSection(data) {
    const inputs = data.organizationContactDetails.inputs;
    return createSection('organizationContactDetails', 'Organization Contact Informations', inputs, data);
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
    document.getElementById(`${data.organisationName}SummaryText${data.id}`).innerHTML = summaryText;
}

export { addOrganisation, getDefaultDoctorOrganisationData, getDefaultFarmacyOrganisationData }