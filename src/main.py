from slack import SlackBot
from common import Common


class Main:
    def __init__(self):
        self.common = Common()
        self.slack_bot = SlackBot(self.common)

    def run(self):
        messages = self.slack_bot.get_messages("C4Y232UGL", 10000)
        for message in messages:
            print(message)



if __name__ == "__main__":
    main = Main()
    main.run()