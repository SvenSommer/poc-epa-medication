const MAX_LOG_ENTRIES = 10;

let logStorage = [];

function addLogEntry(action, url, requestPayload, response) {
    const timestamp = new Date().toISOString();
    logStorage.unshift({ timestamp, action, url, requestPayload, response });

    if (logStorage.length > MAX_LOG_ENTRIES) {
        logStorage.pop();
    }

    updateLogDisplay();
}

function updateLogDisplay() {
    const logTable = $('#logTableBody');
    logTable.empty();

    logStorage.forEach((log, index) => {
        const rowHtml = createLogTableRow(log, index);
        logTable.append(rowHtml);

        // Attach event listener to the button
        $(`#accordionButton${index}`).click(() => toggleAccordion(index));
    });
}

function createLogTableRow(log, index) {
    const isSuccess = log.response.status_code === 200;
    const rowClass = isSuccess ? 'success-row' : (log.response.status_code && log.response.status_code !== 200) ? 'error-row' : '';

    const payloadAccordionHtml = createPayloadAccordionHtml(log.requestPayload, index);

    return `
        <tr class="${rowClass}">
            <td>${log.timestamp}</td>
            <td>${log.action}</td>
            <td>${log.url}</td>
            <td>${payloadAccordionHtml}</td>
            <td>${log.response.message}</td>
            <td>${log.response.status_code}</td>
        </tr>`;
}

function createPayloadAccordionHtml(requestPayload, index) {
    return `
        <button class="btn-link collapsed" id="accordionButton${index}">Show Payload</button>
        <div class="accordion-content" id="accordionPayload${index}" style="display: none;">
            <pre>${JSON.stringify(requestPayload, null, 2)}</pre>
        </div>`;
}

function toggleAccordion(index) {
    const accordionContent = $(`#accordionPayload${index}`);
    accordionContent.toggle();
}

export { addLogEntry, updateLogDisplay };
