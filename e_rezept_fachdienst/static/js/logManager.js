

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

    logStorage.forEach((log, index) => {
        let isSuccess = log.response.status_code === 200;
        let rowClass = isSuccess ? ' class="success-row"' : (log.response.status_code && log.response.status_code !== 200) ? ' class="error-row"' : '';

        let payloadAccordion = `
            <button class="btn-link collapsed" id="accordionButton${index}">Show Payload</button>
            <div class="accordion-content" id="accordionPayload${index}" style="display: none;">
                <pre>${JSON.stringify(log.requestPayload, null, 2)}</pre>
            </div>
        `;

        let row = `<tr${rowClass}>
            <td>${log.timestamp}</td>
            <td>${log.action}</td>
            <td>${log.url}</td>
            <td>${payloadAccordion}</td>
            <td>${log.response.message}</td>
            <td>${log.response.status_code}</td>
        </tr>`;

        logTable.append(row);

        // Attach event listener to the button
        $(`#accordionButton${index}`).on('click', function() {
            toggleAccordion(index);
        });
    });
}

function toggleAccordion(index) {
    let accordionContent = document.getElementById(`accordionPayload${index}`);
    accordionContent.style.display = accordionContent.style.display === "none" ? "block" : "none";
}






export { addLogEntry, updateLogDisplay }