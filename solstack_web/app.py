
from flask import Flask, request, redirect, url_for, render_template

import ansible_runner

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def main_page():
    return render_template("main.html")

@app.route('/sc', methods=["GET", "POST"])
def sc_page():
    return render_template("sc.html")

@app.route('/test')
def test1():
    r = ansible_runner.run(private_data_dir='.', playbook='test.yml')
    # r = ansible_runner.run(private_data_dir='/tmp/demo', host_pattern='localhost', module='shell', module_args='whoami')
    print("{}: {}".format(r.status, r.rc))
    # successful: 0
    for each_host_event in r.events:
        print(each_host_event['event'])
    print("Final status:")
    print(r.stats)
    return "check logs"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')