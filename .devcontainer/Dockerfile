FROM mcr.microsoft.com/devcontainers/base:alpine-3.18

# Set environment variables
ENV FIRELY_TERMINAL_VERSION=3.1.0
ENV JAVA_VALIDATOR_VERSION=6.0.11
ENV SUSHI_VERSION=3.5.0
ENV TZ=Europe/Berlin

# Install necessary tools
RUN wget https://dot.net/v1/dotnet-install.sh \
    && chmod +x dotnet-install.sh \
    && ./dotnet-install.sh --channel 6.0 --install-dir /usr/share/dotnet \
    && ln -s /usr/share/dotnet/dotnet /usr/local/bin \
    && rm dotnet-install.sh \
    && apk add --no-cache icu-libs nodejs npm openjdk11 \
    && npm install -g fsh-sushi@$SUSHI_VERSION \
    && apk update && apk add --no-cache jq findutils curl ca-certificates \
    && mkdir -p /home/vscode/.fhir/validators/ \
    && wget -q https://github.com/hapifhir/org.hl7.fhir.core/releases/download/$JAVA_VALIDATOR_VERSION/validator_cli.jar -O /home/vscode/.fhir/validators/validator_cli.jar \
    && mkdir -p /home/vscode/.fhir/packages /home/vscode/.fhir/settings/ \
    && chown -R vscode:vscode /home/vscode/.fhir/packages \
    && apk add --no-cache python3 py3-pip postgresql postgresql-client

# Install Firely Terminal as vscode user
USER vscode
RUN dotnet tool install --global Firely.Terminal --version $FIRELY_TERMINAL_VERSION
ENV PATH="/home/vscode/.dotnet/tools:${PATH}"

# Copy configuration and start script
USER root
COPY codfsh-config.yaml /home/vscode/.fhir/settings/codfsh-config.yaml
COPY start.sh /workspace/poc-epa-medication/start.sh
RUN chmod +x /workspace/poc-epa-medication/start.sh

# Install Flask and other Python dependencies
COPY src/requirements.txt /workspace/src/requirements.txt
RUN pip3 install -r /workspace/src/requirements.txt

# Expose necessary ports
EXPOSE 5432 5000 5001

# Set working directory and environment variables for Flask and project
WORKDIR /workspace
ENV PYTHONPATH /workspace
ENV FHIR_OPERATION_URL http://127.0.0.1:5000

# Copy the entire project
COPY . /workspace

# Optional: Starting command
 CMD [ "/bin/bash" ]
