# 1. Import Flask
from flask import Flask


# 2. Create an app
app = Flask(__name__)

@app.route("/")
def home():
    return "Hi"


@app.route("/normal")
def normal():
    return hello_dict


@app.route("/jsonified")
def jsonified():
    return jsonify(hello_dict)









if __name__ == "__main__":
    app.run(debug=True)
