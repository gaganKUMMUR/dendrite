from ariadne import graphql_sync
from ariadne.explorer import ExplorerGraphiQL
from flask import request, jsonify
from core import app
from schema import schema

explorer_html = ExplorerGraphiQL().html(None)

@app.route("/", methods=["GET"])
def graphql_playground():
    return explorer_html, 200


@app.route("/", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema=schema, data=data, context_value=request, debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code


if __name__ == "__main__":
    app.run(debug=True,port=8000)
