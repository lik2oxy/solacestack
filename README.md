# solacestack
Tools to setup Solace demo environment

# Quick Start
## Clone
<pre><code>
git clone https://github.com/lik2oxy/solacestack.git 
</code></pre>

## Build 
<pre><code>
docker build --tag solaceansibletest:0.4 .
</code></pre>

## Run
<pre><code>
docker run -v URI_MY_PROJ_SERVICE_ACCOUNT_JSON:/app-pb/res/my-project-serviceaccount.json -p 5000:5000 -it solaceansibletest:0.4
</code></pre>

URI_MY_PROJ_SERVICE_ACCOUNT_JSON is the absolute path of the google cloud service account credential in json format (ex: /home/hyoon/.mycredential/my-project-serviceaccount.json). Note that IAM user should have 1) "Kubernetes Engune Admin" and 2) "Service Account User" permissions. 

## Note
You might need to modify pb/vars/gcp_k8s_pubsub.vars.yml per your Google Cloud Project configuration.
