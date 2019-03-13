import sys
from flask import Flask, request, Response
from jsonrpcserver import dispatch


def create_app():
    """Create Flask endpoint

    Accepts and executes command requests from JSON data.

    :return:
        (application/json) Application for execution.
    """
    app = Flask(__name__)

    @app.route("/", methods=["POST"])
    def index():
        req = request.get_data().decode()
        response = dispatch(req, debug=True)
        print(req, response, file=sys.stderr)
        return Response(str(response), response.http_status, mimetype="application/json")

    return app
