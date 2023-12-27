from fhir.resources.coding import Coding


class CodingObject:
    def __init__(self, code: str, display: str, system: str):
        self.code = code
        self.display = display
        self.system = system

    def to_coding(self) -> Coding:
        return Coding(
            system=self.system,
            code=self.code,
            display=self.display,
        )