
from flask import Flask, request, redirect, url_for, render_template, Response

import ansible_runner

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def main_page():
    if request.method == "POST":
        prov_type = request.form["prov_type"]
        return redirect(f"/{prov_type}")
    else:
        return render_template("main.html")

@app.route('/sc', methods=["GET", "POST"])
def sc_page():
    if request.method == "POST":
        sctoken = request.form["sctoken"]
        sc_create(sctoken)
        return "Done"
    else:
        return render_template("sc.html")

@app.route('/gc', methods=["GET", "POST"])
def gc_page():
# TODO: need to async operations - https://stackoverflow.com/questions/31866796/making-an-asynchronous-task-in-flask/55440793     
    if request.method == "POST":
        action = request.form["action"]
        print(request.form["action"])
        print("action: " + action)
        adminpw = request.form["adminpw"]
        clustername = request.form["clustername"]
        if action == "create-deploy":
            gc_auth()
            gc_cluster_create(clustername)
            gc_ha_deploy(adminpw)
        elif action == "undeploy-destroy":
            gc_ha_undeploy(adminpw)
            gc_cluster_destroy(clustername)
        return "Done" 

    else:
        return render_template("gc.html")

def sc_create(token):
    r = ansible_runner.run(
        private_data_dir='.',
        playbook='ansible-solace/working-with-solace-cloud/playbook.sc-create.yml', 
        extravars={
            'WORKING_DIR': '.',
            'SOLACE_CLOUD_API_TOKEN': token
            }
    )
    print("{}: {}".format(r.status, r.rc))
    # successful: 0
    for each_host_event in r.events:
        print(each_host_event['event'])
    print("Final status:")
    print(r.stats)

def gc_auth():
    #We keep the default for now  - intentionally hard-coded to hint for future dev.
    r = ansible_runner.run(
        private_data_dir='/app-pb/',
        playbook='/app-pb/auth.gcp.gcloud.yml', 
        extravars={
            }
    )
    print("{}: {}".format(r.status, r.rc))
    # successful: 0
    for each_host_event in r.events:
        print(each_host_event['event'])
    print("Final status:")
    print(r.stats)

def gc_cluster_destroy(clustername):
    #We keep the default for now  - intentionally hard-coded to hint for future dev.
    r = ansible_runner.run(
        private_data_dir='/app-pb/',
        playbook='/app-pb/destroy.gcp.cluster.yml', 
        extravars={
            'gcp_cluster_name': 'ansible-gcp-appmo-ambush'
            }
    )
    print("{}: {}".format(r.status, r.rc))
    # successful: 0
    for each_host_event in r.events:
        print(each_host_event['event'])
    print("Final status:")
    print(r.stats)


def gc_cluster_create(clustername):
    #We keep the default for now  - intentionally hard-coded to hint for future dev.
    r = ansible_runner.run(
        private_data_dir='/app-pb/',
        playbook='/app-pb/create.gcp.cluster.yml', 
        extravars={
            'gcp_cluster_name': 'ansible-gcp-appmo-ambush'
            }
    )
    print("{}: {}".format(r.status, r.rc))
    # successful: 0
    for each_host_event in r.events:
        print(each_host_event['event'])
    print("Final status:")
    print(r.stats)

def gc_ha_deploy(adminpw):
    #We keep the default for now  - intentionally hard-coded to hint for future dev.
    r = ansible_runner.run(
        private_data_dir='/app-pb/',
        playbook='/app-pb/deploy.solace.ha.yml', 
        extravars={
            'pubsub_admin_pw': 'admin',
            }
    )
    print("{}: {}".format(r.status, r.rc))
    # successful: 0
    for each_host_event in r.events:
        print(each_host_event['event'])
    print("Final status:")
    print(r.stats)

def gc_ha_undeploy(adminpw):
    #We keep the default for now  - intentionally hard-coded to hint for future dev.
    r = ansible_runner.run(
        private_data_dir='/app-pb/',
        playbook='/app-pb/undeploy.solace.ha.yml', 
        extravars={
            'pubsub_admin_pw': 'admin',
            }
    )
    print("{}: {}".format(r.status, r.rc))
    # successful: 0
    for each_host_event in r.events:
        print(each_host_event['event'])
    print("Final status:")
    print(r.stats)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
