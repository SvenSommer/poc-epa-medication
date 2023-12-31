import {addReceiptItem } from "./receiptManager.js";
import { getPrescriptionDefaultData, getDispenseDefaultData, gatherSentPrescriptionFromInputFields,  gatherDispensationFromPrescriptionInputFields, gatherDispensationFromDispensationInputFields } from "./receiptDataManager.js";
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


addOrganisation(getDefaultDoctorOrganisationData());
addOrganisation(getDefaultFarmacyOrganisationData());
addPractitioner();

$('#sendPrescription').click(function () {
    let requestData = collectPrescriptionRequestData();
    let requestPayload = { prescriptions: requestData };

    makeRequest('/send_prescription', 'Prescription sent', requestPayload)
    .then(response => {

        let dispensations = gatherDispensationFromPrescriptionInputFields();
        for (const dispensation of dispensations) {
            addReceiptItem('dispensationAccordion', dispensation);
        }
        let prescriptions = gatherSentPrescriptionFromInputFields()
        for (const prescription of prescriptions) {
            addReceiptItem('sentPrescriptionAccordion', prescription);
        }
        console.log("Prescriptions sent:", prescriptions);
    })
    .catch(error => {
        console.error("Error sending prescription:", error);
    });
});



$('#cancelPrescription').click(function () {
    const checkedCheckboxes = document.querySelectorAll('.checkbox-button:checked[data-purpose="sentPrescription"]');
    const selectedIds = Array.from(checkedCheckboxes).map(checkbox => {
        return { 'rxPrescriptionProcessIdentifier': checkbox.getAttribute('data-rxPrescriptionProcessIdentifier') };
    });
    let requestPayload = { prescriptionIdentifiers: selectedIds };
    makeRequest('/cancel_prescription', 'Prescription cancelled', requestPayload);
});


// Send dispensation button click event
$('#sendDispensation').click(function () {
    let requestData = collectDispensationRequestData();
    let requestPayload = { dispensations: requestData };
    console.log("requestPayload:", requestPayload);
    makeRequest('/send_dispensation', 'Dispensation sent', requestPayload).then(response => {
        let dispensations = gatherDispensationFromDispensationInputFields();
        for (const dispensation of dispensations) {
            addReceiptItem('sentDispensationAccordion', dispensation);
        }
    })
});

// Cancel dispensation button click event
$('#cancelDispensation').click(function () {
    const checkedCheckboxes = document.querySelectorAll('.checkbox-button:checked[data-purpose="sentDispensation"]');
    const selectedIds = Array.from(checkedCheckboxes).map(checkbox => {
        // Modify this line according to the data format expected by /cancel_dispensation
        return { 'rxPrescriptionProcessIdentifier': checkbox.getAttribute('data-rxPrescriptionProcessIdentifier') };
    });
    let requestPayload = { dispensationIdentifiers: selectedIds };
    makeRequest('/cancel_dispensation', 'Dispensation cancelled', requestPayload);
});

