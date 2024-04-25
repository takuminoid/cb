from abc import ABC, abstractmethod
from datetime import datetime, timedelta


class State(ABC):
    """Chatbotの状態を表すインターフェイス"""

    @abstractmethod
    def ask(self) -> None:
        pass

    @abstractmethod
    def choose_next_state(self, user_input: str) -> "State":
        pass

    @abstractmethod
    def __str__(self):
        pass


class WaitInputObject(State):
    """Note: 初期の状態"""

    def __init__(self) -> None:
        self.object: str = ""

    def ask(self) -> None:
        print("ご用件はなんでしょうか？")

    def choose_next_state(self, user_input: str) -> State:
        self.object = user_input
        if user_input == "来店予約":
            return WaitInputNumPeople()
        elif user_input == "テイクアウト予約":
            return WaitInputMenu()
        else:
            print("来店予約かテイクアウト予約のみ受け付けています。")
            return WaitInputObject()

    def __str__(self):
        return "お客様の要件を聞いています。"


class WaitInputNumPeople(State):
    def __init__(self) -> None:
        self.num_people: int = 0

    def ask(self) -> None:
        print("何名様でしょうか？")

    def choose_next_state(self, user_input: str) -> State:
        try:
            self.num_people = int(user_input)
        except ValueError:
            print("数字で入力してください")
            return WaitInputNumPeople()
        return WaitInputDatetime()

    def __str__(self):
        return "人数を聞いています。"


class WaitInputDatetime(State):
    def __init__(self):
        self._datetime: str = ""

    def ask(self) -> None:
        print("いつご来店されますか？")

    def choose_next_state(self, user_input: str) -> State:
        self._datetime = user_input
        if user_input == "今日" or user_input == "明日":
            return WaitInputMenu()
        else:
            print("今日か明日のみ受け付けています。")
            return WaitInputDatetime()

    @property
    def datetime(self) -> str:
        if self._datetime == "今日":
            return datetime.today().strftime("%Y/%m/%d")
        elif self._datetime == "明日":
            tommorow_date: datetime = datetime.today() + timedelta(days=1)
            return tommorow_date.strftime("%Y/%m/%d")
        else:
            return ""

    def __str__(self):
        return "来店日時を聞いています。"


class WaitInputMenu(State):
    def __init__(self) -> None:
        self.menu: str = ""

    def ask(self) -> None:
        print("メニューはどうされますか？")

    def choose_next_state(self, user_input: str) -> State:
        self.menu = user_input
        if user_input == "魚定食":
            return Complete()
        else:
            print("うちは魚定食しかないです。")
            return WaitInputMenu()

    def __str__(self):
        return "メニューを聞いています。"


class Complete(State):
    """完了用のStateクラス"""

    def ask(self) -> None:
        pass

    def choose_next_state(self, user_input: str):
        pass

    def __str__(self):
        return "すでに完了しています。"
