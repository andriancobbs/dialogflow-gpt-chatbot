# app.py
from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Setup API Key OpenAI (gunakan kunci dari environment variable)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    query_result = req.get("queryResult")
    
    user_query = query_result.get("queryText")

    # Kirim pertanyaan pengguna ke ChatGPT API
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=user_query,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7
    )

    # Ambil jawaban dari OpenAI API
    answer = response.choices[0].text.strip()

    # Kirim jawaban kembali ke Dialogflow
    return jsonify({
        "fulfillmentText": answer
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
