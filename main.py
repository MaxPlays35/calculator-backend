from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from models import Expression

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


@cross_origin()
@app.post("/calculate")
def calc():
    expression = Expression(request.json["expression"])
    _, error, index = expression.parse()
    if error:
        return jsonify({"answer": None, "error": error, "index": index})
    expression.translate()
    answer = expression.calculate()
    return jsonify({"answer": answer, "error": False, "index": 0})


@cross_origin()
@app.post("/solve")
def solve():
    expression = Expression(request.json["expression"])
    _, error, index = expression.parse()
    if error:
        return jsonify({"answer": None, "error": error, "index": index})
    print(expression.translate())
    a, b = request.json["start"], request.json["end"]
    root = expression.find_root(a, b)
    return jsonify({"answer": root, "error": False, "index": 0})


@cross_origin()
@app.post("/integral")
def integral():
    expression = Expression(request.json["expression"])
    _, error, index = expression.parse()
    if error:
        return jsonify({"answer": None, "error": error, "index": index})
    print(expression.translate())
    a, b = request.json["start"], request.json["end"]
    result = expression.simpson(a, b)
    return jsonify({"answer": str(result), "error": False, "index": 0})


if __name__ == "__main__":
    app.run("0.0.0.0")
