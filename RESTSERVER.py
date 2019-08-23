from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from song_lyric_analysis import LyricGenerator_modeller


app = Flask(__name__)
CORS(app)


@app.route('/modeller_init', methods=['GET'])
def init_model():

    global model
    model = LyricGenerator_modeller()
    response = {
            'success': True
        }
    return jsonify(response) , 201


@app.route('/modeller_genres', methods=['GET'])
def get_genres():
    genres = model.get_genres()
    if len(genres) > 0:
        response = {
           'genres' : model.get_genres()
        }
        return jsonify(response) , 200
    else:
        response = {
            'message': 'No genres available'
        }
        return jsonify(response) , 500

@app.route('/modeller_build', methods=['POST'])
def build_model():
    values = request.get_json()
    print(values['genre'])
    model.init_model(values['genre'])
    response = {
            'success': True
        }
    return jsonify(response) , 201

@app.route('/modeller_suggestion', methods=['POST'])
def suggestion():
    values = request.get_json()
    print(values['wordlist'])
    response = {
            'suggestions' : model.suggest_next(values['wordlist'])
            }
    print(response)
    return jsonify(response) , 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
