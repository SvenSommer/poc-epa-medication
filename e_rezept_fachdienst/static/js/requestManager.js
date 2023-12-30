import { showBanner } from "./bannerManager.js";
import { addLogEntry } from "./logManager.js";


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

function collectRequestData() {
    // Helper function to trim and get value from an element
    const getValue = (id) => document.getElementById(id).value.trim();

    const splitGivenNames = (givenNamesString) => {
        return givenNamesString.split(',').map(name => name.trim());
    };

    // Collecting organization data
    const organizationInfo = {
        org_id: "456", // Hardcoded for now, replace with dynamic value if needed
        telematik_id: getValue('orgTelematikId1'),
        org_type_code: getValue('orgTypeCode1'),
        org_type_display: getValue('orgTypeDisplay1'),
        name: getValue('orgName1'),
        alias: getValue('orgAlias1'),
        contact_name: getValue('contactName1'),
        phone: getValue('phone1')
    };

    const practitionerInfo = {
        id_value: "789", // Hardcoded for now, replace with dynamic value if needed
        telematik_id: getValue('practTelematikId1'),
        anr: getValue('practAnr1'), 
        name_text:getValue('practNameText1'),
        family: getValue('practFamily1'), 
        given: splitGivenNames(getValue('practGiven1')),  
        prefix: getValue('practPrefix1'),
        qualifications: [
            {"system": "https://gematik.de/fhir/directory/CodeSystem/PractitionerProfessionOID", "code": "1.2.276.0.76.4.31"},
            {"system": "urn:oid:1.2.276.0.76.5.514", "code": "010", "display": "FA Allgemeinmedizin"},
            {"system": "urn:oid:1.2.276.0.76.5.514", "code": "523", "display": "FA Innere Medizin und (SP) Gastroenterologie"}
        ]
    };

        var prescriptions = Array.from(document.querySelectorAll('.prescription-card')).map(item => {
        var id = item.querySelector('.prescription-card button').getAttribute('data-target').replace(/#collapse|collapse/g, '');

        return {
            rxPrescriptionProcessIdentifier: getValue('rxPrescriptionProcessIdentifier' + id),
            medication_request_info: {
                medication_reference: "123", // Placeholder value
                rxPrescriptionProcessIdentifier: getValue('rxPrescriptionProcessIdentifier' + id),
                patient_reference: getValue('patientReference' + id),
                authoredOn: getValue('authoredOn' + id),
                dosage_instruction_text: getValue('dosageInstructionText' + id),
                substitution_allowed: document.getElementById('substitutionAllowed' + id).checked
            },
            medication_info: {
                rxPrescriptionProcessIdentifier: getValue('rxPrescriptionProcessIdentifier' + id),
                medication_coding: {
                    code: "123", // Placeholder value
                    display: getValue('medicationDisplay' + id),
                    system: getValue('medicationSystem' + id)
                },
                form_coding: {
                    code: getValue('formCode' + id),
                    display: getValue('formDisplay' + id),
                    system: getValue('formSystem' + id)
                }
            },
            organization_info: organizationInfo,
            practitioner_info: practitionerInfo
        };
    });

    console.log(prescriptions);
    return prescriptions;
}

export { makeRequest, collectRequestData }

