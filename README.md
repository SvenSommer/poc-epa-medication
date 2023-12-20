# README for E-Rezept-Fachdienst and ePA MediationService Communication POC

This Proof of Concept (POC) demonstrates seamless communication between the E-Rezept-Fachdienst and the ePA MediationService, utilizing Docker and VS Code's .devcontainer feature for a streamlined setup process.

## Overview

This project involves two main components:

- Medication Service: Manages medication requests and dispensations.
- E-Rezept-Fachdienst: Handles electronic prescription operations.

The project uses Python and is designed to be run in a containerized environment for ease of setup and consistency across platforms.

## Prerequisites

- Docker
- Visual Studio Code with Remote - Containers extension

## Setup

The project is configured to be run in a containerized development environment using Docker and VS Code's Remote - Containers feature. This setup ensures that all necessary dependencies and environment settings are automatically handled.

## Starting the Services

To get the POC running, you need to start both services in separate terminals:

Medication Service:

```bash
/workspaces/poc-epa-medication/epa_aktenkonto/medication_service (main) $ python app.py
```

E-Rezept-Fachdienst:
```bash
/workspaces/poc-epa-medication/e_rezept_fachdienst (main) $ python3 app.py
```

Expected Result
Upon successful execution, the following log messages should be visible:

For E-Rezept-Fachdienst:
```bash
INFO:root:Response from /$provide-prescription: {'message': 'OperationOutcome (success)'}
INFO:root:Cancel Prescription Response: {'message': 'Prescription cancelled successfully'}
INFO:root:Response from /$provide-dispensation: {'message': 'Dispensation provided successfully'}
INFO:root:Cancel Dispensation Response: {'message': 'Dispensation cancelled successfully'}
```

For Medication Service:
```bash
INFO:root:RxPrescriptionProcessIdentifier: 160.768.272.480.500_20231220
INFO:root:MedicationRequest Status: active
INFO:werkzeug:127.0.0.1 - - [20/Dec/2023 23:22:38] "POST /$provide-prescription HTTP/1.1" 200 -
INFO:werkzeug:127.0.0.1 - - [20/Dec/2023 23:22:38] "POST /$cancel-prescription HTTP/1.1" 200 -
INFO:root:RxPrescriptionProcessIdentifier: 160.768.272.480.500_20231220
INFO:root:MedicationDispense Status: completed
INFO:werkzeug:127.0.0.1 - - [20/Dec/2023 23:22:38] "POST /$provide-dispensation HTTP/1.1" 200 -
INFO:werkzeug:127.0.0.1 - - [20/Dec/2023 23:22:38] "POST /$cancel-dispensation HTTP/1.1" 200 -
```
-
## Contributing
Contributions are welcome! Please adhere to the project's coding standards and include appropriate tests. For any contributions or queries, please contact the project maintainers.

## License
MIT License

## Contact
For any queries or contributions, please contact me via Github.