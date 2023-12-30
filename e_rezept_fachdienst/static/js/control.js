import {addReceiptItem, getPrescriptionDefaultData,  getDispenseDefaultData, updateSentPrescriptionsUI } from "./receiptManager.js";
import { addOrganisation, getDefaultDoctorOrganisationData,getDefaultFarmacyOrganisationData  } from "./organisationManager.js";
import { addPractitioner } from "./practitionerManager.js";
import { makeRequest, collectPrescriptionRequestData, collectDispensationRequestData } from "./requestManager.js";

document.getElementById('addPrescription').addEventListener('click', function() {
    addReceiptItem('prescriptionAccordion', getPrescriptionDefaultData());
});

document.getElementById('addDispensation').addEventListener('click', function() {
    addReceiptItem('dispensationAccordion', getDispenseDefaultData());
});


addReceiptItem('prescriptionAccordion',getPrescriptionDefaultData());
addReceiptItem('dispensationAccordion', getDispenseDefaultData());

addOrganisation(getDefaultDoctorOrganisationData());
addOrganisation(getDefaultFarmacyOrganisationData());
addPractitioner();

// Send prescription button click event
let successfulPrescriptions = [];

$('#sendPrescription').click(function () {
    let requestData = collectPrescriptionRequestData();
    let requestPayload = { prescriptions: requestData };
    console.log("requestPayload:", requestPayload);
    makeRequest('/send_prescription', 'Prescription sent', requestPayload)
    .then(response => {
        requestData.forEach(prescription => {
            successfulPrescriptions.push(prescription.rxPrescriptionProcessIdentifier);
        });

        console.log("Saved rxPrescriptionProcessIdentifiers:", successfulPrescriptions);
        updateSentPrescriptionsUI(successfulPrescriptions); // Update the UI with the sent prescriptions
    })
    .catch(error => {
        console.error("Error sending prescription:", error);
    });
});


// Cancel prescription button click event
$('#cancelPrescription').click(function () {
    makeRequest('/cancel_prescription', 'Prescription cancelled');
});

// Send dispensation button click event
$('#sendDispensation').click(function () {
    let requestData = collectDispensationRequestData();
    let requestPayload = { dispensations: requestData };
    console.log("requestPayload:", requestPayload);
    makeRequest('/send_dispensation', 'Dispensation sent', requestPayload).then(response => {
        console.log("Dispensed rxPrescriptionProcessIdentifiers:", successfulPrescriptions);
    })
});

// Cancel dispensation button click event
$('#cancelDispensation').click(function () {
    makeRequest('/cancel_dispensation', 'Dispensation cancelled');
});
