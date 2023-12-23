import json
import logging
from controller.fhir.epaFhirRessource import ePAFHIRRessource
from fhir.resources.provenance import Provenance
from fhir.resources.reference import Reference
from fhir.resources.fhirtypes import DateTime
from datetime import datetime

class ProvenanceController(ePAFHIRRessource):
    def __init__(self, db_reader, db_writer):
        self.db_reader = db_reader
        self.db_writer = db_writer

    @staticmethod
    def build_provenance(target_references: list, recorded_datetime: str, agent_reference: list, entity_reference: list) -> Provenance:
        provenance = Provenance(
            target=[Reference(reference=tr) for tr in target_references],
            recorded=DateTime.validate(recorded_datetime),
            agent=[{"who": Reference(reference=ar["who"]["reference"])} for ar in agent_reference],
            entity=[{"role": "derivation", "what": Reference(reference=er["what"]["reference"])} for er in entity_reference]
        )
        
        return provenance

    def create(self, existing_identifier, new_identifier):
        provenance_data = self.build_provenance(
            target_references=["urn:uuid:" + str(existing_identifier)],
            recorded_datetime=datetime.now().isoformat(),
            agent_reference=[{"who": {"reference": "System/MedicationService"}}],
            entity_reference=[{"what": {"reference": "urn:uuid:" + str(new_identifier)}}]
        )
        
        return {"Provenance": json.loads(provenance_data.json())}