import { addReceiptItem } from "./receiptManager.js";
import { getPrescriptionDefaultData, getDispenseDefaultData, gatherSentPrescriptionFromInputFields, gatherDispensationFromPrescriptionInputFields, gatherDispensationFromDispensationInputFields } from "./receiptDataManager.js";

import { addOrganisation, getDefaultDoctorOrganisationData, getDefaultFarmacyOrganisationData } from "./organisationManager.js";

import { addPractitioner } from "./practitionerManager.js";
import { makeRequest, collectPrescriptionRequestData, collectDispensationRequestData } from "./requestManager.js";

function setupEventListeners() {
    document.getElementById('addPrescription').addEventListener('click', () => {
        addReceiptItem('prescriptionAccordion', getPrescriptionDefaultData());
    });

    document.getElementById('addDispensation').addEventListener('click', () => {
        addReceiptItem('dispensationAccordion', getDispenseDefaultData());
    });

    $('#sendPrescription').click(sendPrescription);
    $('#cancelPrescription').click(cancelPrescription);
    $('#sendDispensation').click(sendDispensation);
    $('#cancelDispensation').click(cancelDispensation);
}

function sendPrescription() {
    const requestData = collectPrescriptionRequestData();
    const requestPayload = { prescriptions: requestData };

    makeRequest('/send_prescription', 'Prescription sent', requestPayload)
        .then(response => handlePrescriptionResponse())
        .catch(error => console.error("Error sending prescription:", error));
}

function handlePrescriptionResponse() {
    processDispensations(gatherDispensationFromPrescriptionInputFields(), 'dispensationAccordion');
    processPrescriptions(gatherSentPrescriptionFromInputFields(), 'sentPrescriptionAccordion');
}

function cancelPrescription() {
    const selectedIds = getSelectedItems('.checkbox-button:checked[data-purpose="sentPrescription"]', 'data-rxPrescriptionProcessIdentifier');
    makeRequest('/cancel_prescription', 'Prescription cancelled', { prescriptionIdentifiers: selectedIds });
}

function sendDispensation() {
    const requestData = collectDispensationRequestData();
    makeRequest('/send_dispensation', 'Dispensation sent', { dispensations: requestData })
        .then(response => processDispensations(gatherDispensationFromDispensationInputFields(), 'sentDispensationAccordion'));
}

function cancelDispensation() {
    const selectedIds = getSelectedItems('.checkbox-button:checked[data-purpose="sentDispensation"]', 'data-rxPrescriptionProcessIdentifier');
    makeRequest('/cancel_dispensation', 'Dispensation cancelled', { dispensationIdentifiers: selectedIds });
}

function processDispensations(dispensations, accordionId) {
    dispensations.forEach(dispensation => addReceiptItem(accordionId, dispensation));
}

function processPrescriptions(prescriptions, accordionId) {
    prescriptions.forEach(prescription => addReceiptItem(accordionId, prescription));
}

function getSelectedItems(selector, dataAttribute) {
    return Array.from(document.querySelectorAll(selector)).map(checkbox => ({
        rxPrescriptionProcessIdentifier: checkbox.getAttribute(dataAttribute)
    }));
}

addReceiptItem('prescriptionAccordion', getPrescriptionDefaultData());
addOrganisation(getDefaultDoctorOrganisationData());
addOrganisation(getDefaultFarmacyOrganisationData());
addPractitioner();
setupEventListeners();
