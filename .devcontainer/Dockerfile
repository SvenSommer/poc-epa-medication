FROM mcr.microsoft.com/devcontainers/base:alpine-3.18

# Setzen der Umgebungsvariablen
ENV FIRELY_TERMINAL_VERSION=3.1.0
ENV JAVA_VALIDATOR_VERSION=6.0.11
ENV SUSHI_VERSION=3.5.0
ENV TZ=Europe/Berlin

# Installieren der notwendige Tools
# Add Microsoft's .NET SDK repository and install .NET SDK
RUN wget https://dot.net/v1/dotnet-install.sh \
    && chmod +x dotnet-install.sh \
    && ./dotnet-install.sh --channel 6.0 --install-dir /usr/share/dotnet \
    && ln -s /usr/share/dotnet/dotnet /usr/local/bin \
    && rm dotnet-install.sh

# Install ICU libraries
RUN apk add --no-cache icu-libs

# Install Node.js and npm
RUN apk add --no-cache nodejs npm

# Install Java (OpenJDK)
RUN apk add --no-cache openjdk11

# Install Firely Terminal as vscode user
# Switch to the vscode user
USER vscode

# Install Firely Terminal
RUN dotnet tool install --global Firely.Terminal --version $FIRELY_TERMINAL_VERSION

# Add .NET tools to PATH for vscode user
ENV PATH="/home/vscode/.dotnet/tools:${PATH}"

# Switch back to root user to perform remaining installations
USER root

RUN npm install -g fsh-sushi@$SUSHI_VERSION

# Installieren der zusätzliche Abhängigkeiten
RUN apk update && apk add --no-cache jq findutils curl ca-certificates

# Setup for FHIR Validator
RUN mkdir -p /home/vscode/.fhir/validators/
RUN wget -q https://github.com/hapifhir/org.hl7.fhir.core/releases/download/$JAVA_VALIDATOR_VERSION/validator_cli.jar -O /home/vscode/.fhir/validators/validator_cli.jar

# Set ownership
RUN mkdir -p /home/vscode/.fhir/packages && \
    chown -R vscode:vscode /home/vscode/.fhir/packages

RUN mkdir -p /home/vscode/.fhir/settings/
COPY codfsh-config.yaml /home/vscode/.fhir/settings/codfsh-config.yaml

# Install Python and Pip
RUN apk add --no-cache python3 py3-pip

# Install PostgreSQL
RUN apk add --no-cache postgresql

FROM mcr.microsoft.com/devcontainers/base:alpine-3.18

# Setzen der Umgebungsvariablen
ENV FIRELY_TERMINAL_VERSION=3.1.0
ENV JAVA_VALIDATOR_VERSION=6.0.11
ENV SUSHI_VERSION=3.5.0
ENV TZ=Europe/Berlin

# Installieren der notwendige Tools
# Add Microsoft's .NET SDK repository and install .NET SDK
RUN wget https://dot.net/v1/dotnet-install.sh \
    && chmod +x dotnet-install.sh \
    && ./dotnet-install.sh --channel 6.0 --install-dir /usr/share/dotnet \
    && ln -s /usr/share/dotnet/dotnet /usr/local/bin \
    && rm dotnet-install.sh

# Install ICU libraries
RUN apk add --no-cache icu-libs

# Install Node.js and npm
RUN apk add --no-cache nodejs npm

# Install Java (OpenJDK)
RUN apk add --no-cache openjdk11

# Install Firely Terminal as vscode user
# Switch to the vscode user
USER vscode

# Install Firely Terminal
RUN dotnet tool install --global Firely.Terminal --version $FIRELY_TERMINAL_VERSION

# Add .NET tools to PATH for vscode user
ENV PATH="/home/vscode/.dotnet/tools:${PATH}"

# Switch back to root user to perform remaining installations
USER root

RUN npm install -g fsh-sushi@$SUSHI_VERSION

# Installieren der zusätzliche Abhängigkeiten
RUN apk update && apk add --no-cache jq findutils curl ca-certificates

# Setup for FHIR Validator
RUN mkdir -p /home/vscode/.fhir/validators/
RUN wget -q https://github.com/hapifhir/org.hl7.fhir.core/releases/download/$JAVA_VALIDATOR_VERSION/validator_cli.jar -O /home/vscode/.fhir/validators/validator_cli.jar

# Set ownership
RUN mkdir -p /home/vscode/.fhir/packages && \
    chown -R vscode:vscode /home/vscode/.fhir/packages

RUN mkdir -p /home/vscode/.fhir/settings/
COPY codfsh-config.yaml /home/vscode/.fhir/settings/codfsh-config.yaml

# Kopieren des Startskripts
COPY start.sh /workspaces/poc-epa-medication/start.sh
# Ausführbar machen des Startskripts
RUN chmod +x /workspaces/poc-epa-medication/start.sh

# Install Python and Pip
RUN apk add --no-cache python3 py3-pip

# Install PostgreSQL
RUN apk add --no-cache postgresql

# Install Flask and other Python dependencies
COPY requirements.txt /workspace/
RUN pip3 install -r /workspace/requirements.txt

# Initialisieren der PostgreSQL-Datenbank
RUN mkdir /run/postgresql /var/lib/postgresql/data /var/lib/postgresql/log \
    && chown -R postgres:postgres /run/postgresql /var/lib/postgresql/data /var/lib/postgresql/log \
    && su - postgres -c "initdb /var/lib/postgresql/data"

# PostgreSQL Konfigurationsbefehle
# Umgebungsvariablen für die PostgreSQL-Datenbankkonfiguration
ENV DB_NAME=fhir_resources
ENV DB_USER=medication_service
ENV DB_PASSWORD=secret_password

# Switch to the postgres user to perform database operations
USER postgres

# Create a database, a user, grant privileges, and make necessary configurations
RUN pg_ctl start -D /var/lib/postgresql/data -l /var/lib/postgresql/log/logfile \
    && psql -c "CREATE DATABASE $DB_NAME;" \
    && psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" \
    && psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;" \
    && psql -c "ALTER USER $DB_USER WITH SUPERUSER;" \
    && pg_ctl stop -D /var/lib/postgresql/data

# Switch back to the root user (optional, depending on further needs)
USER root


# Expose PostgreSQL port
EXPOSE 5432

# Expose the port Flask is running on
EXPOSE 5000

# Setzen des Arbeitsverzeichnis
WORKDIR /workspace

ENV PYTHONPATH /workspace
ENV FHIR_OPERATION_URL http://127.0.0.1:5000

# Kopieren des gesamten Projekts
COPY . /workspace

# Startbefehl
CMD [ "/bin/bash" ]
