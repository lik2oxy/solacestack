
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
        if isValidGcOperationArgs(request.form)==False:
            return "invalid parameters"

        action = request.form["action"]
        print("action: " + action)

        gc_auth()
        res="Done"
        if action == "create-deploy":
            gc_cluster_create(request.form)
            res=gc_ha_deploy(request.form)
        elif action == "undeploy-destroy":
            gc_ha_undeploy(request.form)
            gc_cluster_destroy(request.form)
        return res 

    else:
        return render_template("gc.html")

def sc_create(token):
    run_playbook('.', 'ansible-solace/working-with-solace-cloud/playbook.sc-create.yml', {
            'WORKING_DIR': '.',
            'SOLACE_CLOUD_API_TOKEN': token
            })
def gc_auth():
    run_playbook('/app-pb/', '/app-pb/auth.gcp.gcloud.yml', {})

def gc_cluster_destroy(reqForms):
    run_playbook('/app-pb/', '/app-pb/destroy.gcp.cluster.yml', toArray(reqForms))

def gc_cluster_create(reqForms):
    run_playbook('/app-pb/', '/app-pb/create.gcp.cluster.yml', toArray(reqForms))

def gc_ha_deploy(reqForms):
    hostAndPlaybackEvent=run_playbook('/app-pb/', '/app-pb/deploy.solace.ha.yml', toArray(reqForms))
    # TODO: We should manipulate the output of the command below
    # kubectl describe service solaceha-pubsubplus-ha -n ansible-test-namespace
    lb_ingress_ip="undefined"
    address="http://"+lb_ingress_ip+":8080"
    
    for ev in hostAndPlaybackEvent.events:
        if 'event_data' in ev and 'task' in ev['event_data'] and ev['event_data']['task']=="Show IP of the svc":
            res=ev['event_data']['res']
            if 'stdout' in res:
                address=res['stdout'].replace("\n","<br>")
    return address

def gc_ha_undeploy(reqForms):
    run_playbook('/app-pb/', '/app-pb/undeploy.solace.ha.yml', toArray(reqForms))

def run_playbook(priv_data_dir, playbook_path, args):
    print("debug-pvd "+ priv_data_dir)
    print("debug-pbp "+ playbook_path)
    print("debug-arg")
    print(args)
    r = ansible_runner.run(
        private_data_dir=priv_data_dir,
        playbook=playbook_path,
        extravars=args
    )
    print("{}: {}".format(r.status, r.rc))
    # successful: 0
    for each_host_event in r.events:
        print("ev:" + each_host_event['event'])
    print("Final status:")
    print(r.stats)
    return r

def isValidGcOperationArgs(formDict):
    print("isValidGcOperationArgs: " + formDict["action"])
    action = formDict["action"]
    if formDict["clustername"] == "":
        return False
    if formDict["deploymentname"] == "":
        return False
    if action == "create-deploy" and formDict["adminpw"]=="":
        return False

    return True

def toArray(formDict):
    extravars={
            'gcp_cluster_name':  formDict["clustername"],
            'gcp_cluster_location':  formDict["clusterlocation"],
            'pubsub_admin_pw':  formDict["adminpw"],
            'pubsub_name': formDict["deploymentname"]
            }
    return extravars

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
