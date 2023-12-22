function createSummaryElement(text, className) {
    const element = document.createElement('div');
    element.classList.add(className);
    element.textContent = text;
    return element;
}

function createAccordionItem(key, data, container) {
    const accordion = document.createElement('button');
    accordion.className = 'accordion';
    accordion.textContent = `${key} (${data.length} Elemente)`;
    container.appendChild(accordion);
    return accordion;
}

function createPanel(container) {
    const panel = document.createElement('div');
    panel.className = 'panel';
    container.appendChild(panel);
    return panel;
}

function createSummaryForResource(key, resourceData) {
    let summary = document.createElement('div');
    summary = handleSummaryCreation(key, resourceData, summary);
    summary.className = 'summary-div';
    return summary;
}

function handleSummaryCreation(key, resourceData, summary) {
    switch (key) {
        case 'MedicationDispenses':
            return buildMedicationDispensesSummary(resourceData.MedicationDispense, summary);
        case 'MedicationRequests':
            return buildMedicationRequestsSummary(resourceData.MedicationRequest, summary);
        case 'Organisations':
            return buildOrganisationsSummary(resourceData.Organization, summary);
        case 'Medications':
            return buildMedicationsSummary(resourceData.Medication, summary);
        case 'Practitioners':
            return buildPractitionersSummary(resourceData.Practitioner, summary);
        default:
            summary.textContent = JSON.stringify(resourceData, null, 2);
            return summary;
    }
}

function buildMedicationDispensesSummary(resourceData, summary) {
    const rxIdentifier = resourceData.extension.find(ext => ext.url.includes('rx-prescription-process-identifier-extension'))?.valueIdentifier?.value;
    const whenHandedOver = resourceData.whenHandedOver;
    const status = resourceData.status;
    const wasSubstituted = resourceData.substitution?.wasSubstituted;

    summary.appendChild(createSummaryElement(`Rx Identifier: ${rxIdentifier}`, 'summary-property'));
    summary.appendChild(createSummaryElement(`Handed Over: ${whenHandedOver}`, 'summary-property'));
    summary.appendChild(createSummaryElement(`Status: ${status}`, 'summary-property'));
    summary.appendChild(createSummaryElement(`Substituted: ${wasSubstituted}`, 'summary-property'));

    return summary;
}

function buildMedicationRequestsSummary(resourceData, summary) {
    const rxIdentifier = resourceData.identifier.find(ident => ident.system.includes('rx-prescription-process-identifier'))?.value;
    const dosageInstruction = resourceData.dosageInstruction?.[0]?.text;
    const quantity_value = resourceData.dispenseRequest?.quantity?.value;
    const quantity_code = resourceData.dispenseRequest?.quantity?.code;
    const authoredOn = resourceData.authoredOn;
    const status = resourceData.status;
    const substitutionAllowed = resourceData.substitution?.allowedBoolean;

    summary.appendChild(createSummaryElement(`Rx Identifier: ${rxIdentifier}`, 'summary-property'));
    summary.appendChild(createSummaryElement(`Authored On: ${authoredOn}`, 'summary-property'));
    summary.appendChild(createSummaryElement(`Quantity: ${quantity_value} ${quantity_code}`, 'summary-property'));
    summary.appendChild(createSummaryElement(`Dosage Instruction: ${dosageInstruction}`, 'summary-property'));
    summary.appendChild(createSummaryElement(`Status: ${status}`, 'summary-property'));
    summary.appendChild(createSummaryElement(`Substitution Allowed: ${substitutionAllowed}`, 'summary-property'));

    return summary;
}

function buildOrganisationsSummary(resourceData, summary) {
    const telematikId = resourceData.identifier.find(ident => ident.system.includes('telematik-id'))?.value;
    const name = resourceData.name;
    const type = resourceData.type?.[0]?.coding?.[0]?.display;

    summary.appendChild(createSummaryElement(`Telematik ID: ${telematikId}`, 'summary-property'));
    summary.appendChild(createSummaryElement(`Type: ${type}`, 'summary-property'));
    summary.appendChild(createSummaryElement(`Name: ${name}`, 'summary-property'));

    return summary;
}

function buildMedicationsSummary(resourceData, summary) {
    const rxIdentifier = resourceData.extension.find(ext => ext.url.includes('rx-prescription-process-identifier-extension'))?.valueIdentifier?.value;
    const code = resourceData.code?.coding?.[0]?.code;
    const display = resourceData.code?.coding?.[0]?.display;
    const status = resourceData.status;
    summary.appendChild(createSummaryElement(`Rx Identifier: ${rxIdentifier}`, 'summary-property'));
    console.log(resourceData.identifier)
    if (resourceData.identifier) {
        const unique_identifier = resourceData.identifier.find(ident => ident?.system?.includes('epa-medication-unique-identifier'))?.value;
        summary.appendChild(createSummaryElement(`Unique Identifier: ${unique_identifier}`, 'summary-property'));
    }
    summary.appendChild(createSummaryElement(`Code: ${code}`, 'summary-property'));
    summary.appendChild(createSummaryElement(`Display: ${display}`, 'summary-property'));
    summary.appendChild(createSummaryElement(`Status: ${status}`, 'summary-property'));

    return summary;
}

function buildPractitionersSummary(resourceData, summary) {
    const telematikId = resourceData.identifier.find(ident => ident.system.includes('telematik-id'))?.value;
    const name = resourceData.name?.[0]?.text;
    const qualification = resourceData.qualification
    summary.appendChild(createSummaryElement(`Telematik ID: ${telematikId}`, 'summary-property'));
    summary.appendChild(createSummaryElement(`Name: ${name}`, 'summary-property'));
    for (const qual of qualification) {
        if (qual.code.coding[0]?.display != undefined)
            summary.appendChild(createSummaryElement(`Qualification: ${qual.code.coding[0]?.display}`, 'summary-property'));
    }

    return summary;
}



function initializeAccordion() {
    window.addEventListener('DOMContentLoaded', () => {
        fetch('/get-fhir-data')
            .then(response => response.json())
            .then(data => {
                const container = document.getElementById('accordion-container');
                Object.keys(data).forEach(key => {
                    const accordion = createAccordionItem(key, data[key], container);
                    const panel = createPanel(container);

                    data[key].forEach(item => {
                        const resourceData = item[0];
                        const summary = createSummaryForResource(key, resourceData);
                        panel.appendChild(summary);

                        // Add event listeners
                        summary.addEventListener('click', () => {
                            const codeElement = document.getElementById('json-code');
                            codeElement.textContent = JSON.stringify(resourceData, null, 2);
                            codeElement.removeAttribute('data-highlighted');
                            hljs.highlightElement(codeElement);
                        });
                    });

                    accordion.addEventListener('click', function () {
                        this.classList.toggle('active');
                        const panel = this.nextElementSibling;
                        panel.style.display = panel.style.display === 'block' ? 'none' : 'block';
                    });
                });
            }).catch(err => {
                console.error(err);
            });
    });
}

initializeAccordion();
