from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def main_page():
    return render_template("main.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')