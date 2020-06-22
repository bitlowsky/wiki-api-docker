from flask import Flask, jsonify, request
from wiki import get_wiki_summary_with_db_check

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def root():
    response = {}
    query = request.args.get("query", None)

    if query:
        response['query'] = query
        response["summary"] = get_wiki_summary_with_db_check(query)
        response["status"] = 200 if len(response["summary"]) else 404

    else:
        response['query'] = ''
        response["summary"] = ''
        response["status"] = 400
        response["message"] = {
            'description': "You must specify a query parameter.",
            'example': "/?query=кошка"
        }

    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
