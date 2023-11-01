from flask import Flask, jsonify
import requests

app = Flask(__name__)


@app.route('/news')
def buscar_noticias():
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        'apiKey': 'e93e151696c347639a910ceae2b9e8a7',
        'country': 'BR',
    }

    response = requests.get(url, params=params)
    noticias = response.json()
    return jsonify(noticias)


'''
    if response.status.code == 'ok':
        noticias = response.json()
        return jsonify(noticias)
    else:
        return jsonify({'erro': 'Não foi possível buscar as notícias'})
'''


if __name__ == '__main__':
    app.run(debug=True)
