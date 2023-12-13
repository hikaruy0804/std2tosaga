from flask import Flask, render_template, request, redirect, url_for, request
from std2saga import Std2saga
# from light_std2saga import Std2saga
from add_darkrai import Darkrai
import requests

app = Flask(__name__)
saga = Std2saga()
darkrai = Darkrai()

@app.route("/")
def index():
    return render_template("index.html", messages=[])

#APIを仕様ない場合
@app.route("/sagaben", methods=["POST"])
def trans_sagaben():
    user_message = request.form["message"]
    # Chatbotの処理（ここでは簡単に'test'を返す）
    response = saga.sagaben(str(user_message))
    return render_template("index.html", messages=
                           [{"sender": "user", "text": user_message}, 
                            {"sender": "bot", "text": response}]
                           )

# APIによる返答
# @app.route("/sagaben", methods=["POST"])
# def trans_sagaben():
#     user_message = request.form["message"]
#     try:
#         response = requests.post("http://localhost:8000/sagaben", #グローバルIPとポート番号を修正
#                                  json={"message": user_message})
#         response.raise_for_status()
#     except requests.exceptions.RequestException as err:
#         print(f"An error occurred: {err}")
#         return render_template("index.html", messages=[{"sender": "bot", "text": "An error occurred while processing your request. Please try again later."}])
#     else:
#         return render_template("index.html", messages=response.json()["messages"])

#/sagabenにGETしたときのリダイレクト
@app.route('/sagaben', methods=['GET'])
def redirect_to_root():
    return redirect(url_for('root'))

#T5の説明ページ
@app.route("/t5explain")
def index_t5explain():
    return render_template("index-t5explain.html")

########Darkraiのページ###########
@app.route("/darkrai")
def index_darkrai():
    return render_template("darkrai_index.html")

@app.route("/darkrai", methods=["POST"])
def darkrai_response():
    user_message = request.form["message"]
    try:
        # 外部APIへのリクエスト
        response = requests.post("https://c4ruf681jg.execute-api.ap-northeast-1.amazonaws.com/default/darkrai", json={"message": user_message})
        response.raise_for_status()
        
        # APIからのレスポンスデータを取得
        darkrai_response_data = response.json()
        if "messages" in darkrai_response_data:
            messages = darkrai_response_data["messages"]
        else:
            messages = [{"sender": "bot-darkrai", "text": "The response from the API did not contain expected data."}]
    except requests.exceptions.RequestException as err:
        # エラーが発生した場合の処理
        print(f"An error occurred: {err}")
        messages = [{"sender": "bot-darkrai", "text": "An error occurred while processing your request. Please try again later."}]
    
    return render_template("darkrai_index.html", messages_darkrai=messages)

# #APIを仕様ない場合
# @app.route("/darkrai", methods=["POST"])
# def darkrai_response():
#     darkrai_message = request.form["message"]
#     # Chatbotの処理
#     darkrai_message = darkrai.darkrai_sentence(str(darkrai_message))
#     return render_template("darkrai_index.html", messages_darkrai=
#                            [{"sender": "bot-darkrai", "text": darkrai_message}]
#                            )

#/darkraiにGETしたときのリダイレクト
@app.route('/darkrai', methods=['GET'])
def redirect_to_root_darkrai():
    return redirect(url_for('root'))

########Darkraiのページ###########


#リダイレクト先の設定
@app.route('/')
def root():
    return render_template("index.html", messages=[])

if __name__ == "__main__":
    app.run(debug=True)
