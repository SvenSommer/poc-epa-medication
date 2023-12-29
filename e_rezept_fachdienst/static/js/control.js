import { addPrescriptionItem } from "./prescriptionManager.js";

// Function to show banner
function showBanner(message, type) {
    let banner = `<div class="alert ${type === 'success' ? 'alert-success' : 'alert-danger'}">${message}</div>`;
    $('#banner').html(banner);
    setTimeout(() => $('#banner').html(''), 7000); // Banner will disappear after 3 seconds
}
let logStorage = [];
function addLogEntry(action, url, requestPayload, response) {
    const timestamp = new Date().toISOString();

    logStorage.unshift({ timestamp, action, url, requestPayload, response });

    if (logStorage.length > 10) {
        logStorage.pop();
    }
    updateLogDisplay();
}

function updateLogDisplay() {
    let logTable = $('#logTableBody');
    logTable.html('');

    logStorage.forEach(log => {
        // Determine if the request was successful (status code 200)
        let isSuccess = log.response.status_code === 200;

        let rowClass = '';
        if (isSuccess) {
            rowClass = ' class="success-row"';
        } else if (log.response.status_code && log.response.status_code !== 200) {
            rowClass = ' class="error-row"';
        }

        let row = `<tr${rowClass}>
            <td>${log.timestamp}</td>
            <td>${log.action}</td>
            <td>${log.url}</td>
            <td>${JSON.stringify(log.requestPayload, null, 2)}</td>
            <td>${log.response.message}</td>
            <td>${log.response.status_code}</td>
        </tr>`;
        logTable.append(row);
    });
}

document.getElementById('addPrescription').addEventListener('click', addPrescriptionItem);

// Global counter to uniquely identify each accordion item

addPrescriptionItem();

function collectRequestData() {
    var prescriptions = [];
    console.log("Collecting prescription data...");
    document.querySelectorAll('.card').forEach(item => {
        console.log("Processing an item:", item);
        var id = item.querySelector('.card-header button').getAttribute('data-target').replace('#collapse', '').replace('collapse', '');
        console.log("ID:", id);
        var rxPrescriptionProcessIdentifier = document.getElementById('rxPrescriptionProcessIdentifier' + id).value.trim();
        var patientReference = document.getElementById('patientReference' + id).value.trim();
        var authoredOn = document.getElementById('authoredOn' + id).value.trim();
        var dosageInstructionText = document.getElementById('dosageInstructionText' + id).value.trim();
        var substitutionAllowed = document.getElementById('substitutionAllowed' + id).checked;

        var medicationCode =  "123" // field is set later
        var medicationDisplay = document.getElementById('medicationDisplay' + id).value.trim();
        var medicationSystem = document.getElementById('medicationSystem' + id).value.trim();

        var formCode = document.getElementById('formCode' + id).value.trim();
        var formDisplay = document.getElementById('formDisplay' + id).value.trim();
        var formSystem = document.getElementById('formSystem' + id).value.trim();

        var prescriptionData = {
            rxPrescriptionProcessIdentifier: rxPrescriptionProcessIdentifier,
            medication_request_info: {
                medication_reference: "123", // You may need to update this field
                rxPrescriptionProcessIdentifier: rxPrescriptionProcessIdentifier,
                patient_reference: patientReference,
                authoredOn: authoredOn,
                dosage_instruction_text: dosageInstructionText,
                substitution_allowed: substitutionAllowed
            },
            medication_info: {
                rxPrescriptionProcessIdentifier: rxPrescriptionProcessIdentifier,
                medication_coding: {
                    code: medicationCode,
                    display: medicationDisplay,
                    system: medicationSystem
                },
                form_coding: {
                    code: formCode,
                    display: formDisplay,
                    system: formSystem
                }
            },
        };
        prescriptions.push(prescriptionData);
    });
    console.log(prescriptions);
    return prescriptions;
}



function makeRequest(url, action) {
    let requestData = collectRequestData();

    if (requestData.some(med => !med.rxPrescriptionProcessIdentifier)) {
        showBanner('Error: Invalid identifier', 'error');
        return;
    }

    let requestPayload = { prescriptions: requestData };

    $.ajax({
        url: url,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(requestPayload),
        success: function (response, textStatus, xhr) {
            addLogEntry(action, url, requestPayload, response); // Log the request and response

            if (response.status_code === 200) {
                let message = response.message || action + ' successful';
                showBanner('Success: ' + message, 'success');
            } else {
                let errorMessage = response.message || 'Error: ' + xhr.status;
                showBanner("Error: '" + errorMessage + "', Status code: " + response.status_code, 'error');
            }
        },
        error: function (xhr) {
            let errorMessage = 'An unknown error occurred';
            if (xhr && xhr.responseJSON && xhr.responseJSON.error) {
                errorMessage = xhr.responseJSON.error;
            } else if (xhr && xhr.status) {
                errorMessage = 'Error: ' + xhr.status;
            }
            addLogEntry(action, url, requestPayload, { error: errorMessage }); // Log the error
            showBanner('Error: ' + errorMessage, 'error');
        }
    });
}



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
