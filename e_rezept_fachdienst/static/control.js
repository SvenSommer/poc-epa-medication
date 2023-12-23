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
    
    if (logStorage.length > 5) {
        logStorage.pop();
    }
    updateLogDisplay();
}

function updateLogDisplay() {
    let logTable = $('#logTableBody');
    logTable.html('');

    logStorage.forEach(log => {
        // Check if the status code is not 200
        let isError = log.response.status_code && log.response.status_code !== 200;

        let row = `<tr${isError ? ' class="error-row"' : ''}>
            <td>${log.timestamp}</td>
            <td>${log.action}</td>
            <td>${log.url}</td>
            <td>${log.requestPayload.rxPrescriptionProcessIdentifier}</td>
            <td>${log.response.message}</td>
            <td>${log.response.status_code}</td>
        </tr>`;
        logTable.append(row);
    });
}

function makeRequest(url, action) {
    let rxPrescriptionProcessIdentifier = $('#rxPrescriptionProcessIdentifier').val().trim();

    if (!rxPrescriptionProcessIdentifier) {
        showBanner('Error: Invalid identifier', 'error');
        return;
    }

    let requestPayload = { rxPrescriptionProcessIdentifier };

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
