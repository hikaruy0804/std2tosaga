from flask import Flask, render_template, request, redirect, url_for, request
import requests
# from std2saga import Std2saga
# from light_std2saga import Std2saga

app = Flask(__name__)
# saga = Std2saga()

@app.route("/")
def index():
    return render_template("index.html", messages=[])

#APIを仕様ない場合
# @app.route("/sagaben", methods=["POST"])
# def chatbot():
#     user_message = request.form["message"]
#     # Chatbotの処理（ここでは簡単に'test'を返す）
#     response = saga.sagaben(str(user_message))
#     return render_template("index.html", messages=
#                            [{"sender": "user", "text": user_message}, 
#                             {"sender": "bot", "text": response}]
#                            )

#APIによる返答
@app.route("/sagaben", methods=["POST"])
def trans_sagaben():
    user_message = request.form["message"]
    try:
        response = requests.post("http://localhost:8000/sagaben", #グローバルIPとポート番号を修正
                                 json={"message": user_message})
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print(f"An error occurred: {err}")
        return render_template("index.html", messages=[{"sender": "bot", "text": "An error occurred while processing your request. Please try again later."}])
    else:
        return render_template("index.html", messages=response.json()["messages"])

#T5の説明ページ
@app.route("/t5explain")
def index_t5explain():
    return render_template("index-t5explain.html")

#/sagabenにGETしたときのリダイレクト
@app.route('/sagaben', methods=['GET'])
def redirect_to_root():
    return redirect(url_for('root'))

#リダイレクト先の設定
@app.route('/')
def root():
    return render_template("index.html", messages=[])

if __name__ == "__main__":
    app.run(debug=True)
