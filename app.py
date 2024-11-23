from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Mengatur API Key OpenAI (menggunakan kunci dari environment variable)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Mendapatkan data dari permintaan
        req = request.get_json(silent=True, force=True)
        if req is None or 'queryResult' not in req:
            return jsonify({"fulfillmentText": "Maaf, saya tidak dapat memproses permintaan Anda. Silakan coba lagi."})
        
        query_result = req.get("queryResult")
        user_query = query_result.get("queryText")

        if not user_query:
            return jsonify({"fulfillmentText": "Maaf, saya tidak dapat memahami pertanyaan Anda. Bisakah Anda menjelaskannya kembali?"})

        # Mengirim pertanyaan pengguna ke API ChatGPT
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_query,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7
        )

        # Mengambil jawaban dari API OpenAI
        if response and len(response.choices) > 0:
            answer = response.choices[0].text.strip()
        else:
            answer = "Saya tidak yakin bagaimana menjawabnya. Bisakah Anda menanyakan dengan cara yang berbeda?"

        # Mengirim jawaban kembali ke Dialogflow
        return jsonify({
            "fulfillmentText": answer
        })

    except Exception as e:
        # Jika terjadi error, log error dan kirim pesan fallback ke pengguna
        print(f"Error: {str(e)}")
        return jsonify({
            "fulfillmentText": "Terjadi kesalahan saat memproses permintaan Anda. Silakan coba lagi nanti."
        })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
