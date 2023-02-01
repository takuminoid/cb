# チャットボット本体
import traceback # エラーが起きた際に、そのエラー内容を表示するモジュールをインポート
import sys

class chat_bot():
    def __init__(self):
        self.state = {'state':'None', 'is_exit' : False} # 状態遷移図をstate で表現、is_exist で終了条件を判定
        self.bot_name = '(bot):'    # bot の名前
        self.menu = ['魚定食', 'カツ丼', 'カレーライス']    # 予約できるメニュー一覧

        # 状態遷移図の矢印を表すルール
        self.update_rule = {
            'None' : 'wait_input_obj'
            ,'wait_input_obj' : 'wait_input_num_reservation'
            ,'wait_input_num_reservation' : 'wait_input_time'
            ,'wait_input_time' : 'wait_input_menu'
            ,'wait_input_menu' : 'tell_reservation_info'
        }
        self.reservation = {'obj':'', 'time':'', 'num_reservation':'', 'menu':''} # 予約の情報を保存する辞書

    # 状態の更新
    def update_state(self):
        self.state['state'] = self.update_rule[self.state['state']] # self.update_rule に従いチャットボットの状態を更新

    # 対話開始のメッセージ
    def start_declare(self):
        print('--- chat bot の動作を開始します---')
        print('{}こんにちは。〇〇店の予約チャットボットです。来店予約とテイクアウトの予約を承ります。\n来店予約、テイクアウトどちらの予約を行いますか？'.format(self.bot_name))
        self.update_state()

    # お店の予約かテイクアウトかを聞く
    def ask_reason(self, user_response):
        if '来店' in user_response:
            self.reservation['obj'] = '来店予約'
        elif 'テイクアウト' in user_response:
            self.reservation['obj'] = 'テイクアウトの予約'
        else:
            print('{}申し訳ございません。来店予約、テイクアウトの予約のどちらかを、もう一度入力をお願いいたします。'.format(self.bot_name))
        
        if self.reservation['obj'] != '':
            print('{}{}ですね！\n続いて、人数は何人にしますか？\n数値のみでお答えください。'.format(
                self.bot_name, self.reservation['obj']
            ))
            self.update_state()

    # 予約人数の確認
    def ask_num_people(self, user_response):
        try:
            num_reservation = int(user_response)
            self.reservation['num_reservation'] = num_reservation
            print('{}{}名で予約を進めていきますね！\n続いて、来店時間は何時にしますか？\n17〜24の数字でお答えください。'.format(
                self.bot_name, self.reservation['num_reservation']
            ))
            self.update_state()
        except:
            print('{}数値のみ入力してください'.format(self.bot_name))   

    # 予約時間の確認
    def ask_time(self, user_response):
        try:
            num_time = int(user_response)
            if 17 <= num_time <= 24:                          
                self.reservation['time'] = num_time
                print('{}{}時に来店で予約を進めていきますね！\n続いて、メニューはどうしますか？\n{}の中からご選択ください。'.format(
                    self.bot_name, self.reservation['time'], self.menu
                ))
                self.update_state()
            else:
                print('17〜24の数字でお答えください。')
        except:
            print('{}数値のみ入力してください'.format(self.bot_name))  

    # 予約メニューの確認
    def ask_menu(self, user_response):
        for cand_menu in self.menu:            
            if cand_menu in user_response:
                if self.reservation['menu'] == '':
                    self.reservation['menu'] += cand_menu
                else:
                    self.reservation['menu'] += ', ' + cand_menu            

        if self.reservation['menu'] == '':
            print('{}申し訳ございません。メニューが見つかりませんでした。もう一度入力をお願いいたします。\nメニュー：{}'.format(
                self.bot_name, self.menu
            ))
        else:
            self.update_state()

    # 予約完了の処理(予約内容を伝える)
    def tell_info(self):
        print('{}それでは、{}時の{}で、{}名分の「{}」を予約しました！ご来店お待ちしております。'.format(
            self.bot_name,
            self.reservation['time'],
            self.reservation['obj'],
            self.reservation['num_reservation'],
            self.reservation['menu']
        ))
        self.state['is_exit'] = True

    # 対話終了のメッセージ
    def end_declare(self):
        print('{}ご利用ありがとうございました'.format(self.bot_name))

    # チャットボットの動作開始
    def run(self):
        try:
            self.start_declare() # 開始メッセージ送信
            while not self.state['is_exit']:
                user_response = input()
                print('(user):{}'.format(user_response))

                # お店の予約かテイクアウトかを聞く
                if self.state['state']=='wait_input_obj':
                    self.ask_reason(user_response)
                # 予約人数の確認
                elif self.state['state']=='wait_input_num_reservation':
                    self.ask_num_people(user_response)
                # 予約時間の確認
                elif self.state['state']=='wait_input_time':
                    self.ask_time(user_response)
                # 予約メニューの確認
                elif self.state['state']=='wait_input_menu':  
                    self.ask_menu(user_response)        
                else:
                    print('想定しないエラーが発生した可能性があります')
                    sys.exit(0)
                
                # 予約完了の処理(予約内容を伝える)
                if self.state['state']=='tell_reservation_info':
                    self.tell_info()
            
            self.end_declare() # 終了メッセージ送信
        except:
            traceback.print_exc()
            print('エラーが発生しました')


if __name__=='__main__':
    my_chat_bot = chat_bot()
    my_chat_bot.run()
