# chat bot (python)

## Usage

### ターミナルで動くチャットボット
```python
cd terminal-app/
python3 app.py
```

### slackと連携するチャットボット
```python
pip3 -r requirements.txt
python3 app.py
```

#### localhostでslackとの連携を試すのに便利なやつ
```zsh
brew install ngrok
ngrok http 5002 # localhost:5002を外部公開できる
```

#### slack appの設定
- https://api.slack.com/app
- Event Subscription - Request URL にリクエストしたいURLを入力
- app.pyのTOKENをOAuth & Permissions - OAuth Tokens for Your Workspace - Bot User OAuth Token の値に書き換える

##### 権限設定

###### OAuth & Permissions
- channels:history
  - ログ取得権限
- chat:write
  - 書き込み権限
- groups:hitory
  - プライベートチャンネル（DM）ログ取得権限
- users:read
  - ユーザ情報取得権限

###### Event Subsccription
- message.channels
  - チャンネル内に投稿がされたときにEventが送信される
- message.groups
  - プライベートチャンネル（DM）内に投稿がされた時にEventが送信される
