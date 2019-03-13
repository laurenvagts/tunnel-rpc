from __future__ import print_function
import sys
from flask import Flask, request, Response
from jsonrpcserver import dispatch


def create_app():
    app = Flask(__name__)

    @app.route("/", methods=["POST"])
    def index():
        req = request.get_data().decode()
        response = dispatch(req, debug=True)
        print(req, response, file=sys.stderr)
        return Response(str(response), response.http_status, mimetype="application/json")

    return app
