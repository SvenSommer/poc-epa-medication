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

function addPrescriptionItem() {
    const accordion = document.getElementById('prescriptionAccordion');
    const newItem = createAccordionItem(/* pass default values or empty strings */);
    accordion.appendChild(newItem);
}

function createAccordionItem(data = {}) {
    const item = document.createElement('div');
    item.className = 'accordion-item';
    item.innerHTML = `
        <div class="accordion-header">
            <button class="accordion-button collapsed" data-bs-toggle="collapse" data-bs-target="#collapse${data.id}">
                ${data.summary || 'New Prescription'}
            </button>
            <button class="btn btn-danger remove-button">
                <i class="fas fa-minus"></i>
            </button>
        </div>
        <div id="collapse${data.id}" class="accordion-collapse collapse">
            <div class="accordion-body">
                <!-- Form elements to edit prescription details -->
            </div>
        </div>
    `;

    item.querySelector('.remove-button').addEventListener('click', () => item.remove());
    
    // Add event listeners or additional logic to handle prescription detail editing

    return item;
}

// Initialize with one item
addPrescriptionItem();

function collectMedicationData() {
    var medications = [];
    document.querySelectorAll('.medication-entry').forEach(entry => {
        var data = {
            rxPrescriptionProcessIdentifier: entry.children[0].value.trim(),
            medicationCode: entry.children[1].value.trim(),
            // Collect other fields as needed
        };
        medications.push(data);
    });
    return medications;
}

function makeRequest(url, action) {
    let medications = collectMedicationData();

    if (medications.some(med => !med.rxPrescriptionProcessIdentifier)) {
        showBanner('Error: Invalid identifier', 'error');
        return;
    }

    let requestPayload = { medications };

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
