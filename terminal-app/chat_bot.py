from states import Complete, State


class ChatBot:
    def __init__(self, name: str, state: State):
        self._name = name
        self._state = state

    @property
    def state(self) -> str:
        return str(self._state)

    def run(self):
        print("いらっしゃいませ！")
        while not isinstance(self._state, Complete):
            self._state.ask()
            user_input = input()  # ユーザーの入力を待つ
            next_state = self._state.choose_next_state(user_input)
            self._change_state(next_state)
        print("ありがとうございました！")

    def _change_state(self, state: State) -> None:
        self._state = state
