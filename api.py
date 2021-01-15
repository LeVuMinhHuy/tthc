from flask import Flask, request, jsonify
from flask_cors import CORS
from message_handler import catch_intent, get_name_tthc,searchTTHC

app = Flask(__name__)
CORS(app)

def msg(code, mess=None):
    if code == 200 and mess is None:
        return jsonify({"code": 200, "value": True})
    else:
        return jsonify({"code": code, "message": mess}), code

@app.route('/api/send-message', methods=['POST'])
def send_message():
    input_data = request.json
    if "message" not in input_data.keys():
        return msg(400, "Message cannot be None")
    else:
        message = input_data["message"]

    if input_data['state'] == 'not_found':
        result = get_name_tthc(message)
        query = result[0]
        type_database = result[1]
        return jsonify(searchTTHC(type_database, query))

    intent = catch_intent(message)
    return intent

if __name__ == '__main__':
    app.run(debug=True)