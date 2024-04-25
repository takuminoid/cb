from chat_bot import ChatBot
from states import WaitInputObject


def run():
    chat_bot = ChatBot("ウェイターボット君", WaitInputObject())
    chat_bot.run()


if __name__ == "__main__":
    run()
