import requests
from flask import Flask, request, Response


TOKEN = "xoxb-2668681787747-2681295403073-irXv0keZLSaSIMurDGvDLpdJ"  # 作成したSlackAppのBotUserOAuthToken
CHANNEL_ID = "D02K80D6L4X"  # 投稿するチャンネルのID

# Flaskサーバの起動の準備
app = Flask(__name__)

def post_message(text):
    api_url = "https://slack.com/api/chat.postMessage"  # SlackAppが投稿に使用するSlackAPIのURL
    # SlackAPIに送信するデータのヘッダー
    headers = {
        "Authorization": "Bearer {}".format(TOKEN),
        "Content-type": "application/x-www-form-urlencoded"
    }
    # SlackAPIに送信するデータの本体
    payload = {
        "channel": CHANNEL_ID,
        "text": text
    }
    res = requests.post(api_url, headers=headers, params=payload)  # SlackAPIにデータを送信
    res = res.json()  # SlackAPIからの応答をJSON形式に変換
    return

# SlackAppからのEventを受信する関数
@app.route("/run", methods=["POST"])
def slack_chatbot():
    payload = request.json  # 受信したデータをJSON形式に変換

    # SlackのEventSubscriptionの設定時の応答を返す
    if "challenge" in payload:  # SlackのEventSubscriptionの設定時に受信するデータには"challenge"パラメータがある
        print("received 'challenge' parameter")  # パラメータを受信したことの確認
        token = str(payload["challenge"])  # "challenge"パラメータを文字列型に変換
        return Response(token, mimetype="text/plane")  # "challenge"パラメータを返信
    
    # SlackのEventSubscriptionが実行された時に実行
    if "event" in payload:  # SlackのEventSubscriptionが実行された時に受信するデータには"event"がある
        event = payload["event"]  # "event"データを変数に格納
        # pprint(event)  # "event"データの確認
        if "blocks" in event:  # ユーザの投稿には"blocks"がある
            if "text" in event:  # "text"があるか確認
                print("received user's post")  # ユーザの投稿を受信したことの確認
                input_text = event["text"]  # 投稿されたテキストを変数に格納
                post_message(input_text)  # main関数(上のセルにあるメインの処理をする関数)の呼び出し
    return Response("nothing", mimetype="text/plane")  # 返信

# Flaskサーバの起動
if __name__ == '__main__':
    app.run()