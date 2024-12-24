from flask import Flask, render_template, request, jsonify
import requests

RASA_API_URL = 'http://localhost:5005/webhooks/rest/webhook'  # Corrected URL

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    # Retrieve user message from the request
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'response': "No message provided."}), 400

    print("User Message:", user_message)

    try:
        # Send user message to Rasa and get bot's response
        rasa_response = requests.post(RASA_API_URL, json={'message': user_message})

        if rasa_response.status_code == 200:
            rasa_response_json = rasa_response.json()
            print("Rasa Response:", rasa_response_json)

            # Extract bot's response
            bot_response = rasa_response_json[0]['text'] if rasa_response_json else "Sorry, I didn't understand that."
        else:
            bot_response = "Sorry, I couldn't connect to the Rasa server."
    except requests.exceptions.RequestException as e:
        print("Error connecting to Rasa:", e)
        bot_response = "Error connecting to the bot server. Please try again later."

    # Return the bot's response as JSON
    return jsonify({'response': bot_response})


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, port=3000)
