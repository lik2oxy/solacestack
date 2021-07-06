# HOWTO TEST
# $ docker build --tag solaceansibletest:0.3 .
# $ docker run -v <URI_GCP_SERVICE_ACCOUNT_CREDENTIAL>:/app-pb/res/my-project-serviceaccount.json -it solaceansibletest:0.3
#     EX: docker run -v ~/.google_gcp/serviceAccountCredential.json:/app-pb/res/my-project-serviceaccount.json -p 5000:5000 -it solaceansibletest:0.3
#

FROM python:3.7

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app
RUN apt-get update -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends docker sshpass vim tar \
    && pip install -r requirements.txt \
    && ansible-galaxy collection install solace.pubsub_plus google.cloud kubernetes.core \
    && git clone https://github.com/solace-iot-team/ansible-solace.git

RUN curl -sSL https://sdk.cloud.google.com > /tmp/gcl && bash /tmp/gcl --install-dir=/root/ --disable-prompts
ENV PATH="$PATH:/root/google-cloud-sdk/bin"
RUN export CLOUDSDK_CORE_DISABLE_PROMPTS=1
RUN gcloud components update kubectl

COPY ./solstack_web /app
COPY ./pb /app-pb
COPY ./linux-amd64/helm /usr/local/bin/helm

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
