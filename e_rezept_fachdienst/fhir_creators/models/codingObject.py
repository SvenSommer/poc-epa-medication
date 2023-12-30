from fhir.resources.coding import Coding
from fhir.resources.codeableconcept import CodeableConcept

class CodingObject:
    def __init__(self, code: str, display: str, system: str):
        self.code = code
        self.display = display
        self.system = system


    def create_codeable_concept_from_dict(coding_dict: dict) -> CodeableConcept:
        coding_obj = CodingObject.from_dict(coding_dict)
        return CodeableConcept(coding=[coding_obj.to_coding()])


    def to_coding(self) -> Coding:
        return Coding(
            system=self.system,
            code=self.code,
            display=self.display
        )

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            code=data['code'],
            display=data['display'],
            system=data['system']
        )
