const createSummaryElement = (text, className) => {
    const element = document.createElement('div');
    element.classList.add(className);
    element.textContent = text;
    return element;
};
window.addEventListener('DOMContentLoaded', () => {
    fetch('/get-fhir-data')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('accordion-container');

            Object.keys(data).forEach(key => {
                const accordion = document.createElement('button');
                accordion.className = 'accordion';
                accordion.textContent = `${key} (${data[key].length} Elemente)`;
                container.appendChild(accordion);

                const panel = document.createElement('div');
                panel.className = 'panel';
                container.appendChild(panel);

                data[key].forEach(item => {
                    const resourceData = item[0];
                    let summary;

                    if (key === 'MedicationDispenses') {
                        const rxIdentifier = resourceData.extension.find(ext => ext.url.includes('rx-prescription-process-identifier-extension'))?.valueIdentifier?.value;
                        const whenHandedOver = resourceData.whenHandedOver;
                        const status = resourceData.status;
                        const wasSubstituted = resourceData.substitution?.wasSubstituted;

                        summary = document.createElement('div');
                        summary.appendChild(createSummaryElement(`Rx Identifier: ${rxIdentifier}`, 'summary-property'));
                        summary.appendChild(createSummaryElement(`Handed Over: ${whenHandedOver}`, 'summary-property'));
                        summary.appendChild(createSummaryElement(`Status: ${status}`, 'summary-property'));
                        summary.appendChild(createSummaryElement(`Substituted: ${wasSubstituted}`, 'summary-property'));

                    } else if (key === 'MedicationRequests') {
                        const rxIdentifier = resourceData.identifier.find(ident => ident.system.includes('rx-prescription-process-identifier'))?.value;
                        const authoredOn = resourceData.authoredOn;
                        const status = resourceData.status;
                        const substitutionAllowed = resourceData.substitution?.allowedBoolean;

                        summary = document.createElement('div');
                        summary.appendChild(createSummaryElement(`Rx Identifier: ${rxIdentifier}`, 'summary-property'));
                        summary.appendChild(createSummaryElement(`Authored On: ${authoredOn}`, 'summary-property'));
                        summary.appendChild(createSummaryElement(`Status: ${status}`, 'summary-property'));
                        summary.appendChild(createSummaryElement(`Substitution Allowed: ${substitutionAllowed}`, 'summary-property'));

                    } else if (key === 'Medications') {
                        const code = resourceData.code?.coding?.[0]?.code;
                        const display = resourceData.code?.coding?.[0]?.display;

                        summary = document.createElement('div');
                        summary.appendChild(createSummaryElement(`Code: ${code}`, 'summary-property'));
                        summary.appendChild(createSummaryElement(`Display: ${display}`, 'summary-property'));

                    } else if (key === 'Organisations') {
                        const name = resourceData.name;

                        summary = document.createElement('div');
                        summary.appendChild(createSummaryElement(`Name: ${name}`, 'summary-property'));

                    } else if (key === 'Practitioners') {
                        const name = resourceData.name?.[0]?.text;

                        summary = document.createElement('div');
                        summary.appendChild(createSummaryElement(`Name: ${name}`, 'summary-property'));

                    } else {
                        summary = document.createElement('pre');
                        summary.textContent = JSON.stringify(resourceData, null, 2);
                    }
                    summary.className = 'summary-div';

                    panel.appendChild(summary);

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
};
