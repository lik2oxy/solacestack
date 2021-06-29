
from flask import Flask, request, redirect, url_for, render_template

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')