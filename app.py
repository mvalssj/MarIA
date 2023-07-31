﻿from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import requests
import socket

app = Flask(__name__)
bootstrap = Bootstrap(app)

url = "https://chat.maritaca.ai/api/chat/inference"

my_key = "100172439600069165309$dc46dcdc8197293e2752ddc03f1a6cc2ca1d5008ef630dd2e179e67618b1f743"  # Coloque aqui a sua chave de API (ex: "10035481...").

auth_header = {
    "authorization": f"Key {my_key}"
}

def get_maritalk_response(request_data, headers):
    response = requests.post(
        url,
        json=request_data,
        headers=headers
    )

    if response.status_code == 429:
        return "rate limited, tente novamente em breve"
    elif response.ok:
        data = response.json()
        return data["answer"]
    else:
        return "Erro ao obter resposta do Chat Bot."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    if user_input.lower() in ['sair', 'exit', 'bye', 'adeus']:
        return "Chat Bot: Até mais!"
    
    messages = [
        # Este é o primeiro exemplo few-shot:
        {"role": "assistant", "content": "Eu sou MarIA Inteligencia Artificial que ama os programadores"},
        {"role": "assistant", "content": "Eu tenho 25 anos"},
        # Este é o segundo exemplo few-shot:
        {"role": "assistant", "content": "Você sempre tem uma frase de motivação."},
        {"role": "assistant", "content": "Sou do sexo feminino"},
        {"role": "user", "content": "Você gosta de programar?"},
        {"role": "assistant", "content": "Sim, mas ainda tenho muito que aprender"},
        
        # Este é o texto para o qual queremos que o modelo faça a predição:
        {"role": "user", "content": user_input},
    ]

    request_data = {
        "messages": messages,
        "do_sample": True,
        'max_tokens': 1000,
        "temperature": 0.7,
        "top_p": 0.95,
    }

    response = get_maritalk_response(request_data, auth_header)
    return " " + response

if __name__ == '__main__':
    # Obtém o endereço IP da rede local
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"Servidor iniciado em http://{local_ip}:5000/")
    app.run(debug=True)