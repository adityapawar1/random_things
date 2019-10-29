from flask import Flask

app = Flask(__name__)
@app.route('/')



def main():
    file = open('power.txt', 'r')
    for line in file:
        if len(line) > 2:
            return line

app.run(debug=True, port=80, host='0.0.0.0')