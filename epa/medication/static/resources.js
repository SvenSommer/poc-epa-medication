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
    let summaryWrapper = document.createElement('div');
    summaryWrapper.className = 'summary-wrapper';

    let detailedSummary = document.createElement('div');
    detailedSummary.className = 'detailed-summary';
    detailedSummary.style.display = 'none'; 
    detailedSummary = handleSummaryCreation(key, resourceData, detailedSummary);

    let summaryLine = document.createElement('div');
    summaryLine.className = 'summary-line';
    if (detailedSummary.firstChild) {
        summaryLine.textContent = detailedSummary.firstChild.textContent; 
        detailedSummary.removeChild(detailedSummary.firstChild);
    } else {
        summaryLine.textContent = `Summary for ${key}`; 
    }
    summaryWrapper.appendChild(summaryLine);
    summaryWrapper.appendChild(detailedSummary);

    summaryLine.addEventListener('click', () => {
        detailedSummary.style.display = detailedSummary.style.display === 'none' ? 'block' : 'none';
    });

    return summaryWrapper;
}


function handleSummaryCreation(key, resourceData, summary) {
    switch (key) {
        case 'MedicationRequests':
            return buildMedicationRequestsSummary(resourceData, summary);
        case 'MedicationDispenses':
            return buildMedicationDispensesSummary(resourceData, summary);
        case 'Organisations':
            return buildOrganisationsSummary(resourceData, summary);
        case 'Medications':
            return buildMedicationsSummary(resourceData, summary);
        case 'Practitioners':
            return buildPractitionersSummary(resourceData, summary);
        case 'Provenances':
            return buildProvenancesSummary(resourceData, summary);
        default:
            summary.textContent = JSON.stringify(resourceData, null, 2);
            return summary;
    }
}

function buildMedicationDispensesSummary(resourceData, summary) {
    const rxIdentifier = resourceData.extension.find(ext => ext.url.includes('rx-prescription-process-identifier-extension'))?.valueIdentifier?.value;
    const medicationReference = resourceData.medicationReference?.reference;
    const whenHandedOver = resourceData.whenHandedOver;
    const status = resourceData.status;
    const wasSubstituted = resourceData.substitution?.wasSubstituted;

    summary.appendChild(createSummaryElement(`Rx Identifier: ${rxIdentifier}, Status: ${status}`, 'summary-property'));
    summary.appendChild(createSummaryElement(`Rx Identifier: ${rxIdentifier}`, 'summary-property'));
    if (resourceData.identifier) {
        const unique_identifier = resourceData.identifier.find(ident => ident?.system?.includes('epa-medication-dispense-unique-identifier'))?.value;
        summary.appendChild(createSummaryElement(`Unique Identifier: ${unique_identifier}`, 'summary-property'));
    }
    summary.appendChild(createSummaryElement(`Medication Reference: ${medicationReference}`, 'summary-property'));
    summary.appendChild(createSummaryElement(`Handed Over: ${whenHandedOver}`, 'summary-property'));
    summary.appendChild(createSummaryElement(`Status: ${status}`, 'summary-property'));
    summary.appendChild(createSummaryElement(`Substituted: ${wasSubstituted}`, 'summary-property'));

    return summary;
}

function buildMedicationRequestsSummary(resourceData, summary) {
    const rxIdentifier = resourceData.identifier.find(ident => ident.system.includes('rx-prescription-process-identifier'))?.value;
    const medicationReference = resourceData.medicationReference?.reference;
    const dosageInstruction = resourceData.dosageInstruction?.[0]?.text;
    const quantity_value = resourceData.dispenseRequest?.quantity?.value;
    const quantity_code = resourceData.dispenseRequest?.quantity?.code;
    const authoredOn = resourceData.authoredOn;
    const status = resourceData.status;
    const substitutionAllowed = resourceData.substitution?.allowedBoolean;

    summary.appendChild(createSummaryElement(`Rx Identifier: ${rxIdentifier}, Status: ${status}`, 'summary-property'));
    summary.appendChild(createSummaryElement(`Rx Identifier: ${rxIdentifier}`, 'summary-property'));
    summary.appendChild(createSummaryElement(`Medication Reference: ${medicationReference}`, 'summary-property'));
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

    summary.appendChild(createSummaryElement(`Type: ${type}, Name: ${name}, Telematik ID: ${telematikId}`, 'summary-property'));
    summary.appendChild(createSummaryElement(`Telematik ID: ${telematikId}`, 'summary-property'));
    summary.appendChild(createSummaryElement(`Type: ${type}`, 'summary-property'));
    summary.appendChild(createSummaryElement(`Name: ${name}`, 'summary-property'));

    return summary;
}

function buildMedicationsSummary(resourceData, summary) {
    const rxIdentifier = resourceData.extension.find(ext => ext.url.includes('rx-prescription-process-identifier-extension'))?.valueIdentifier?.value;
    const medicationId = resourceData.id;
    const code = resourceData.code?.coding?.[0]?.code;
    const display = resourceData.code?.coding?.[0]?.display;
    const status = resourceData.status;
    summary.appendChild(createSummaryElement(`Rx Identifier: ${rxIdentifier}, Status: ${status}`, 'summary-property'));
    summary.appendChild(createSummaryElement(`Rx Identifier: ${rxIdentifier}`, 'summary-property'));
    if (resourceData.identifier) {
        const unique_identifier = resourceData.identifier.find(ident => ident?.system?.includes('epa-medication-unique-identifier'))?.value;
        summary.appendChild(createSummaryElement(`Unique Identifier: ${unique_identifier}`, 'summary-property'));
    }
    summary.appendChild(createSummaryElement(`Medication ID: ${medicationId}`, 'summary-property'));
    summary.appendChild(createSummaryElement(`Code: ${code}`, 'summary-property'));
    summary.appendChild(createSummaryElement(`Display: ${display}`, 'summary-property'));
    summary.appendChild(createSummaryElement(`Status: ${status}`, 'summary-property'));

    return summary;
}

function buildPractitionersSummary(resourceData, summary) {
    const telematikId = resourceData.identifier.find(ident => ident.system.includes('telematik-id'))?.value;
    const name = resourceData.name?.[0]?.text;
    const qualification = resourceData.qualification
    summary.appendChild(createSummaryElement(`Name: ${name}, Telematik ID: ${telematikId}`, 'summary-property'));
    summary.appendChild(createSummaryElement(`Telematik ID: ${telematikId}`, 'summary-property'));
    summary.appendChild(createSummaryElement(`Name: ${name}`, 'summary-property'));
    for (const qual of qualification) {
        if (qual.code.coding[0]?.display != undefined)
            summary.appendChild(createSummaryElement(`Qualification: ${qual.code.coding[0]?.display}`, 'summary-property'));
    }

    return summary;
}

function buildProvenancesSummary(resourceData, summary) {
    const recorded = resourceData.recorded;
    const agentReference = resourceData.agent[0]?.who?.reference;
    const entityRole = resourceData.entity[0]?.role;
    const entityReference = resourceData.entity[0]?.what?.reference;
    const targetReferences = resourceData.target.map(target => target.reference);

    summary.appendChild(createSummaryElement(`Role: ${entityRole}, Recorded: ${recorded}`, 'summary-property'));
    summary.appendChild(createSummaryElement(`Recorded: ${recorded}`, 'summary-property'));
    summary.appendChild(createSummaryElement(`Role: ${entityRole}`, 'summary-property'));
    summary.appendChild(createSummaryElement(`Agent Reference: ${agentReference}`, 'summary-property'));
    summary.appendChild(createSummaryElement(`Entity Reference: ${entityReference}`, 'summary-property'));
    summary.appendChild(createSummaryElement(`Target References: ${targetReferences.join(', ')}`, 'summary-property'));

    return summary;
}


function initializeAccordion() {
    window.addEventListener('DOMContentLoaded', () => {
        fetch('/get-fhir-data')
            .then(response => response.json())
            .then(data => {
                const container = document.getElementById('accordion-container');
                // Custom order for resource groups
                const order = ['MedicationRequests', 'MedicationDispenses', 'Medications', 'Provenances'];

                // Sort keys based on the predefined order
                const sortedKeys = Object.keys(data).sort((a, b) => {
                    let indexA = order.indexOf(a);
                    let indexB = order.indexOf(b);
                    indexA = indexA === -1 ? Infinity : indexA;
                    indexB = indexB === -1 ? Infinity : indexB;
                    return indexA - indexB;
                });

                sortedKeys.forEach(key => {
                    const accordion = createAccordionItem(key, data[key], container);
                    const panel = createPanel(container);

                    data[key].forEach(item => {
                        if (item.length > 0) {
                            console.log(item[0])
                            const resourceData = item[0];
                            const summary = createSummaryForResource(key, resourceData);
                            panel.appendChild(summary);

                            summary.addEventListener('click', () => {
                                const codeElement = document.getElementById('json-code');
                                codeElement.textContent = JSON.stringify(resourceData, null, 2);
                                codeElement.removeAttribute('data-highlighted');
                                hljs.highlightElement(codeElement);
                            });
                        }
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
