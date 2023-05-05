from flask import Flask, render_template, request
from std2saga import Std2saga

app = Flask(__name__)
saga = Std2saga()

@app.route("/")
def index():
    return render_template("index.html", messages=[])

@app.route("/chatbot", methods=["POST"])
def chatbot():
    user_message = request.form["message"]
    # Chatbotの処理（ここでは簡単に'test'を返す）
    response = saga.sagaben(str(user_message))
    return render_template("index.html", messages=
                           [{"sender": "user", "text": user_message}, 
                            {"sender": "bot", "text": response}]
                           )

if __name__ == "__main__":
    app.run(debug=True)
