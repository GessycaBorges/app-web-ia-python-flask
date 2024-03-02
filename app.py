from flask import Flask, redirect, url_for, request, render_template, session
import requests, os, uuid, json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():
    # Lê o texto que o usuário inseriu e o idioma selecionado no formulário
    original_text = request.form['text']
    target_language = request.form['language']

    # Lê as variáveis de ambiente
    key = os.environ['KEY']
    endpoint = os.environ['ENDPOINT']
    location = os.environ['LOCATION']

    #Cria o caminho necessário para chamar o serviço de Tradução, que inclui o idioma de destino
    path = '/translate?api-version=3.0'
    
    # Adiciona o parâmetro do idioma de destino
    target_language_parameter = '&to=' + target_language
    # Cria a URL completa
    constructed_url = endpoint + path + target_language_parameter

    # Cria as informações de cabeçalho, que incluem a chave para o serviço de Tradução, o local do serviço e uma ID arbitrária para a tradução
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # Cria o corpo da solicitação, que inclui o texto que queremos traduzir
    body = [{ 'text': original_text }]

    # Chama post em requests para chamar o serviço de Tradução
    translator_request = requests.post(constructed_url, headers=headers, json=body)
    # Recupera a resposta JSON do servidor, que inclui o texto traduzido
    translator_response = translator_request.json()
    # Recupera o texto traduzido
    translated_text = translator_response[0]['translations'][0]['text']

    # Chama render_template para exibir a página de resposta
    return render_template(
        'results.html',
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language
    )