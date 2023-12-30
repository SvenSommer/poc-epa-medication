import { addPrescriptionItem } from "./prescriptionManager.js";
import { addOrganisation } from "./organisationManager.js";
import { addPractitioner } from "./practitionerManager.js";
import { makeRequest } from "./requestManager.js";

document.getElementById('addPrescription').addEventListener('click', addPrescriptionItem);

// Global counter to uniquely identify each accordion item

addPrescriptionItem();
addOrganisation();
addPractitioner();

// Send prescription button click event
$('#sendPrescription').click(function () {
    makeRequest('/send_prescription', 'Prescription sent');
});

// Cancel prescription button click event
$('#cancelPrescription').click(function () {
    makeRequest('/cancel_prescription', 'Prescription cancelled');
});

// Send dispensation button click event
$('#sendDispensation').click(function () {
    makeRequest('/send_dispensation', 'Dispensation sent');
});

// Cancel dispensation button click event
$('#cancelDispensation').click(function () {
    makeRequest('/cancel_dispensation', 'Dispensation cancelled');
});
