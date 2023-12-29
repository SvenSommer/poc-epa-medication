
function addPrescriptionItem() {
    const accordion = document.getElementById('prescriptionAccordion');
    const newItem = createAccordionItem({ id: ++prescriptionCounter });
    accordion.appendChild(newItem);
}
const DateTimeUtils = {
    getCurrentDateTimeFormatted() {
        const now = new Date();
        return now.toISOString().slice(0, 19).replace('T', ' ');
    },
    getCurrentDateFormatted() {
        const now = new Date();
        return now.toISOString().slice(0, 10).replace(/-/g, '');
    }
};

const IdentifierUtils = {
    generateBaseIdentifier() {
        const prefix = "160.";
        const segments = new Array(4).fill(null).map(() => Math.floor(Math.random() * 900 + 100));
        return prefix + segments.join('.') + '_';
    },
    generatePrescriptionIdentifier() {
        return this.generateBaseIdentifier() + DateTimeUtils.getCurrentDateFormatted();
    }
};
let prescriptionCounter = 0;
function createAccordionItem(data = {}) {
    const prescriptionIdentifier = IdentifierUtils.generatePrescriptionIdentifier();
    const currentDateTime = DateTimeUtils.getCurrentDateTimeFormatted();

    const item = document.createElement('div');
    item.className = 'card';
    item.innerHTML = `
        <!-- Accordion Header -->
        <div class="card-header" role="tab" id="heading${data.id}">
            <h5 class="mb-0">
                <button class="btn btn-link collapsed" data-toggle="collapse" data-target="#collapse${data.id}" aria-expanded="false" aria-controls="collapse${data.id}">
                    <span id="summaryText${data.id}">Prescription ${data.id || 'New'}</span> <!-- Summary text placeholder -->
                </button>
                <button class="btn btn-danger remove-button" id="removeButton${data.id}">
                    <i class="fas fa-trash"></i>
                </button>
            </h5>
        </div>

        <!-- Accordion Body -->
        <div id="collapse${data.id}" class="collapse" role="tabpanel" aria-labelledby="heading${data.id}" data-parent="#prescriptionAccordion">
            <div class="card-body">
                <!-- Prescription Details Section -->
                <h5>
                    <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#prescriptionDetails${data.id}" aria-expanded="false" aria-controls="prescriptionDetails${data.id}">
                        Prescription Details
                    </button>
                </h5>
                <div id="prescriptionDetails${data.id}" class="collapse" aria-labelledby="heading${data.id}">
                    <div class="row">
                        <div class="col-md-6">
                            <label for="rxPrescriptionProcessIdentifier${data.id}" class="form-label">Rx Prescription Process Identifier</label>
                            <input type="text" class="form-control" id="rxPrescriptionProcessIdentifier${data.id}" value="${prescriptionIdentifier}">
                        </div>
                        <div class="col-md-6">
                            <label for="patientReference${data.id}" class="form-label">Patient Reference</label>
                            <input type="text" class="form-control" id="patientReference${data.id}" value="789">
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-4">
                            <label for="authoredOn${data.id}" class="form-label">Authored On</label>
                            <input type="text" class="form-control" id="authoredOn${data.id}" value="${currentDateTime}">
                        </div>
                        <div class="col-md-4">
                            <label for="dosageInstructionText${data.id}" class="form-label">Dosage Instruction Text</label>
                            <input type="text" class="form-control" id="dosageInstructionText${data.id}" value="1-0-1">
                        </div>
                        <div class="col-md-4 form-check">
                            <input type="checkbox" class="form-check-input" id="substitutionAllowed${data.id}" checked>
                            <label class="form-check-label" for="substitutionAllowed${data.id}">Substitution Allowed</label>
                        </div>
                    </div>
                </div>

                <!-- Medication Coding Section -->
                <h5>
                    <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#medicationCoding${data.id}" aria-expanded="true" aria-controls="medicationCoding${data.id}">
                        Medication Coding
                    </button>
                </h5>
                <div id="medicationCoding${data.id}" class="collapse" aria-labelledby="heading${data.id}">
                
                    <div class="row">
                        <div class="col-md-4">
                            <label for="medicationCode${data.id}" class="form-label">Code</label>
                            <input type="text" class="form-control" id="medicationCode${data.id}" value="08671219">
                        </div>
                        <div class="col-md-4">
                            <label for="medicationDisplay${data.id}" class="form-label">Display</label>
                            <input type="text" class="form-control" id="medicationDisplay${data.id}" value="Aciclovir 800 - 1 A Pharma® 35 Tbl. N1">
                        </div>
                        <div class="col-md-4">
                            <label for="medicationSystem${data.id}" class="form-label">System</label>
                            <input type="text" class="form-control" id="medicationSystem${data.id}" value="http://fhir.de/CodeSystem/ifa/pzn">
                        </div>
                    </div> 
                </div>
                <h5>
                    <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#formCoding${data.id}" aria-expanded="true" aria-controls="formCoding${data.id}">
                        Form Coding
                    </button>
                </h5>
                <div id="formCoding${data.id}" class="collapse" aria-labelledby="heading${data.id}">
                    <div class="row">
                        <div class="col-md-4">
                            <label for="formCode${data.id}" class="form-label">Code</label>
                            <input type="text" class="form-control" id="formCode${data.id}" value="TAB">
                        </div>
                        <div class="col-md-4">
                            <label for="formDisplay${data.id}" class="form-label">Display</label>
                            <input type="text" class="form-control" id="formDisplay${data.id}" value="Tablette">
                        </div>
                        <div class="col-md-4">
                            <label for="formSystem${data.id}" class="form-label">System</label>
                            <input type="text" class="form-control" id="formSystem${data.id}" value="https://fhir.kbv.de/CodeSystem/KBV_CS_SFHIR_KBV_DARREICHUNGSFORM">
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    attachEventListenersToAccordionItem(item, data.id);
    const accordion = document.getElementById('prescriptionAccordion');
    accordion.appendChild(item);
    updatePrescriptionSummary(data.id);
    return item;
}

function attachEventListenersToAccordionItem(item, id) {
    const removeButton = item.querySelector(`#removeButton${id}`);
    removeButton?.addEventListener('click', () => item.remove());

    const collapseElement = item.querySelector(`#collapse${id}`);
    collapseElement?.addEventListener('hidden.bs.collapse', () => updatePrescriptionSummary(id));
}

function updatePrescriptionSummary(id) {
    var rxIdentifier = document.getElementById('rxPrescriptionProcessIdentifier' + id).value;
    var medicationCode = document.getElementById('medicationCode' + id).value;
    var medicationDisplay = document.getElementById('medicationDisplay' + id).value;
    var formDisplay = document.getElementById('formDisplay' + id).value;
    var dosageText = document.getElementById('dosageInstructionText' + id).value;

    var summaryText = `
        ${rxIdentifier}, 
        ${medicationDisplay} (${medicationCode}), ${formDisplay}, 
        ${dosageText}
    `;

    document.getElementById(`summaryText${id}`).innerHTML = summaryText;
}


export { addPrescriptionItem };