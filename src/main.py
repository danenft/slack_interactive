from datetime import datetime

import redis

from slack import SlackBot
from common import Common


class Main:
    def __init__(self):
        self.common = Common()
        self.slack_bot = SlackBot(self.common)
        self.channel_id = self.common.get_slack_channel_id("general")


    def run(self):
        messages = self.slack_bot.get_messages(self.channel_id, 10)
        messages = [message for message in messages if not self.common.from_redis(f"{message['user']}_{message['ts']}")]

        for message in messages:
            now_txt = datetime.now().strftime("%Y-%m-%d %H:%M")

            if message['text'] == "지금 시각은?":
                text = f"현재 시각은 {now_txt}입니다."
                self.slack_bot.post_thread_message(self.channel_id, message['ts'], text)

            if message['text'] == "redis에 메시지 몇 개 적재됐어?":
                redis_data_count = len(list(self.common.redis.scan_iter("*")))
                text = f"현재 redis에 적재된 메시지 수는 {redis_data_count:,}개 입니다."
                self.slack_bot.post_thread_message(self.channel_id, message['ts'], text)

            self.common.to_redis(f"{message['user']}_{message['ts']}", now_txt)

if __name__ == "__main__":
    main = Main()
    main.run()