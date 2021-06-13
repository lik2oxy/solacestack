# Last updated: June/2/2021 
# Author: Hayoung Yoon - hayoung.yoon@solace.com
# This is a Dockerfile to build minimal docker image to run Solace Cloud Provisioning and Configuration using Ansible
# See more details regarding
# 	Solace Ansible : https://solace.com/blog/using-ansible-automate-config-pubsub-plus/
# 
# 
# HOWTO TEST
# $ docker build --tag solaceansibletest:0.1 . 
# $ docker run -it solaceansibletest:0.1
# $ export export SOLACE_CLOUD_API_TOKEN=<Your Solace Cloud API token>
# $ root@xxyyzzaa112233:~/ansible-solace/working-with-solace-cloud# ./run.create.sh
# More than a few min to complete the command. If successful, it will display the message like below at the end.
# PLAY RECAP ******************************************************************************************************************
# localhost                  : ok=8    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

FROM python:3

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app
RUN apt-get update -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends docker sshpass vim \
    && pip install -r requirements.txt \
    && ansible-galaxy collection install solace.pubsub_plus \
    && git clone https://github.com/solace-iot-team/ansible-solace.git
COPY ./solstack_web /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]