#!/bin/bash

# Umgebungsvariablen für PostgreSQL
DB_NAME=${DB_NAME:-fhir_resources}
DB_USER=${DB_USER:-medication_service}

# Starten des PostgreSQL-Servers
su - postgres -c "postgres -D /var/lib/postgresql/data > /var/lib/postgresql/log/logfile 2>&1 &"

# Warten, bis PostgreSQL vollständig gestartet ist
echo "Warten auf PostgreSQL..."
while ! pg_isready -q -d $DB_NAME -U $DB_USER; do
  sleep 1
done
echo "PostgreSQL gestartet."

# Starten des Medication Services
# python3 /workspaces/poc-epa-medication/epa_aktenkonto/medication_service/app.py
python3 /workspaces/poc-epa-medication/epa/medication/app.py
