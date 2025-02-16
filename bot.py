import requests
from flask import Flask, request

app = Flask(__name__)

# Configurações do WhatsApp Cloud API
token = "SEU_TOKEN_DO_FACEBOOK"
phone_number_id = "SEU_PHONE_NUMBER_ID"
verify_token = "SEU_TOKEN_DE_VERIFICACAO"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        # Verificação do webhook
        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if mode == "subscribe" and token == verify_token:
            return challenge, 200
        else:
            return "Erro de verificação", 403

    elif request.method == "POST":
        data = request.json
        if "entry" in data:
            for entry in data["entry"]:
                for change in entry.get("changes", []):
                    if "value" in change and "messages" in change["value"]:
                        for message in change["value"]["messages"]:
                            phone_number = message["from"]
                            text = message["text"]["body"].lower()
                            resposta = processar_mensagem(text)
                            enviar_mensagem(phone_number, resposta)
        return "OK", 200

# Função para processar mensagens
def processar_mensagem(text):
    if "oi" in text or "olá" in text:
        return "Olá! Como posso ajudar?"
    elif "preço" in text:
        return "Nosso serviço de bots tem preços acessíveis! Entre em contato para mais detalhes."
    else:
        return "Desculpe, não entendi. Poderia reformular a pergunta?"

# Função para enviar mensagem
def enviar_mensagem(phone, message):
    url = f"https://graph.facebook.com/v17.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": phone,
        "text": {"body": message}
    }
    requests.post(url, headers=headers, json=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
