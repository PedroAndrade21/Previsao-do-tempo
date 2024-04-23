from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def obter_previsao_tempo(cidade):

    api_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': cidade,
        'appid': '69a9f96a8054d905a068f50f964409cb',  
    }

    resposta = requests.get(api_url, params=params)
    dados = resposta.json()

    return dados

@app.route('/', methods=['GET', 'POST'])
def previsao_tempo():
    cidade = None
    previsao = None

    if request.method == 'POST':
        cidade = request.form['cidade']
        dados_tempo = obter_previsao_tempo(cidade)

        if dados_tempo['cod'] == 404:
            previsao = None
        else:
            previsao = {
                'cidade': cidade,
                'descricao': dados_tempo['weather'][0]['description'],
                'temperatura': round(dados_tempo['main']['temp'] - 273.15, 2),  # Converter de Kelvin para Celsius
                'umidade': dados_tempo['main']['humidity'],
            }

    return render_template('index.html', cidade=cidade, previsao=previsao)

if __name__ == '__main__':
    app.run(debug=True)
