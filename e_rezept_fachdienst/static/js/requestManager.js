import { showBanner } from "./bannerManager.js";
import { addLogEntry } from "./logManager.js";


function makeRequest(url, action, requestPayload) {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: url,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(requestPayload),
            success: function (response, textStatus, xhr) {
                addLogEntry(action, url, response.fhir_request_payload, response); 

                if (response.status_code === 200) {
                    let message = response.message || action + ' successful';
                    showBanner('Success: ' + message, 'success');
                    resolve(response);
                } else {
                    let errorMessage = response.message || 'Error: ' + xhr.status;
                    showBanner("Error: '" + errorMessage + "', Status code: " + response.status_code, 'error');
                    reject(new Error(errorMessage));
                }
            },
            error: function (xhr) {
                let errorMessage = 'An unknown error occurred';
                if (xhr && xhr.responseJSON && xhr.responseJSON.error) {
                    errorMessage = xhr.responseJSON.error;
                } else if (xhr && xhr.status) {
                    errorMessage = 'Error: ' + xhr.status;
                }
                addLogEntry(action, url, requestPayload, { error: errorMessage }); 
                showBanner('Error: ' + errorMessage, 'error');
                reject(new Error(errorMessage));
            }
        });
    });
}

function getValue(id, logError = false) {
    const element = document.getElementById(id);
    if (!element) {
        const message = `Element with ID '${id}' not found.`;
        logError ? console.error(message) : console.warn(message);
        return '';
    }

    const value = element.value.trim();
    if (value === '') {
        const message = `Value for element with ID '${id}' is empty.`;
        logError ? console.error(message) : console.warn(message);
    }

    return value;
}


function collectDispensationRequestData() {
    const farmacyOrgInfo = {
        org_id: "456", // Hardcoded for now, replace with dynamic value if needed
        telematik_id: getValue('farmacyOrgTelematikId1'),
        org_type_code: getValue('farmacyOrgTypeCode1'),
        org_type_display: getValue('farmacyOrgTypeDisplay1'),
        name: getValue('farmacyOrgName1'),
        alias: getValue('farmacyOrgAlias1'),
        contact_name: getValue('farmacyOrgContactName1'),
        phone: getValue('farmacyOrgPhone1')
    };
    var dispensations = Array.from(document.querySelectorAll('.dispensation-card')).map(item => {
        var id = item.querySelector('.dispensation-card button').getAttribute('data-target').replace(/#dispensationcollapse|dispensationcollapse/g, '');

        return {
            rxPrescriptionProcessIdentifier: getValue('dispensationRxPrescriptionProcessIdentifier' + id),
            medication_dispense_info: {
                rxPrescriptionProcessIdentifier: getValue('dispensationRxPrescriptionProcessIdentifier' + id),
                medication_reference: "123",
                patient_identifier: getValue('dispensationPatientReference' + id),
                performer_organization_reference: farmacyOrgInfo.org_id,
                authorizing_prescription_reference: getValue('dispensationAuthorizing_prescription_reference' + id),
                when_handed_over: getValue('dispensationWhen_handed_over' + id),
                dosage_instruction_text: getValue('dispensationDosageInstructionText' + id),
                substitution_allowed: document.getElementById('dispensationSubstitutionAllowed' + id).checked
            },
            medication_info: {
                rxPrescriptionProcessIdentifier: getValue('dispensationRxPrescriptionProcessIdentifier' + id),
                medication_coding: {
                    code: getValue('dispensationMedicationCode' + id),
                    display: getValue('dispensationMedicationDisplay' + id),
                    system: getValue('dispensationMedicationSystem' + id)
                },
                form_coding: {
                    code: getValue('dispensationFormCode' + id),
                    display: getValue('dispensationFormDisplay' + id),
                    system: getValue('dispensationFormSystem' + id)
                }
            },
            organization_info: farmacyOrgInfo
        };
    });

    return dispensations;
}
function collectPrescriptionRequestData() {
    const splitGivenNames = (givenNamesString) => {
        return givenNamesString.split(',').map(name => name.trim());
    };

    const doctorOrgInfo = {
        org_id: "456", // Hardcoded for now, replace with dynamic value if needed
        telematik_id: getValue('doctorOrgTelematikId1'),
        org_type_code: getValue('doctorOrgTypeCode1'),
        org_type_display: getValue('doctorOrgTypeDisplay1'),
        name: getValue('doctorOrgName1'),
        alias: getValue('doctorOrgAlias1'),
        contact_name: getValue('doctorOrgContactName1'),
        phone: getValue('doctorOrgPhone1')
    };

    const practitionerInfo = {
        id_value: "789", // Hardcoded for now, replace with dynamic value if needed
        telematik_id: getValue('practTelematikId1'),
        anr: getValue('practAnr1'),
        name_text: getValue('practNameText1'),
        family: getValue('practFamily1'),
        given: splitGivenNames(getValue('practGiven1')),
        prefix: getValue('practPrefix1'),
        qualifications: [
            { "system": "https://gematik.de/fhir/directory/CodeSystem/PractitionerProfessionOID", "code": "1.2.276.0.76.4.31" },
            { "system": "urn:oid:1.2.276.0.76.5.514", "code": "010", "display": "FA Allgemeinmedizin" },
            { "system": "urn:oid:1.2.276.0.76.5.514", "code": "523", "display": "FA Innere Medizin und (SP) Gastroenterologie" }
        ]
    };

    var prescriptions = Array.from(document.querySelectorAll('.prescription-card')).map(item => {
        var id = item.querySelector('.prescription-card button').getAttribute('data-target').replace(/#prescriptioncollapse|prescriptioncollapse/g, '');
        let prescription = {
            rxPrescriptionProcessIdentifier: getValue('prescriptionRxPrescriptionProcessIdentifier' + id),
            medication_request_info: {
                medication_reference: "123", // Placeholder value
                rxPrescriptionProcessIdentifier: getValue('prescriptionRxPrescriptionProcessIdentifier' + id),
                patient_reference: getValue('prescriptionPatientReference' + id),
                authoredOn: getValue('prescriptionAuthoredOn' + id),
                dosage_instruction_text: getValue('prescriptionDosageInstructionText' + id),
                substitution_allowed: document.getElementById('prescriptionSubstitutionAllowed' + id).checked
            },
            medication_info: {
                rxPrescriptionProcessIdentifier: getValue('prescriptionRxPrescriptionProcessIdentifier' + id),
                medication_coding: {
                    code: getValue('prescriptionMedicationCode' + id),
                    display: getValue('prescriptionMedicationDisplay' + id),
                    system: getValue('prescriptionMedicationSystem' + id)
                },
                form_coding: {
                    code: getValue('prescriptionFormCode' + id),
                    display: getValue('prescriptionFormDisplay' + id),
                    system: getValue('prescriptionFormSystem' + id)
                }
            },
            organization_info: doctorOrgInfo,
            practitioner_info: practitionerInfo
        };
        return prescription;
    });
    return prescriptions;
}

export { makeRequest, collectPrescriptionRequestData, collectDispensationRequestData }

