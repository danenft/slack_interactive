from datetime import datetime
import time

import redis

from slack import SlackBot
from common import Common


class Main:
    def __init__(self):
        self.common = Common()
        self.slack_bot = SlackBot(self.common)
        self.slack_interact_channel = self.common.get_slack_channel_id("interact")
        self.slack_report_channel = self.common.get_slack_channel_id("report")
        self.history_period = self.common.conf['history_period']

    def run(self):
        try:
            self._run()
        except Exception as e:
            text = f"동작 중 에러가 발생하였습니다: {e}"
            self.slack_bot.post_message(self.slack_report_channel, t옴xt)
            ## 에러 났을 땐 1분간 쉬기
            time.sleep(60)

    def _response_now_time(self, message:dict) -> None:
        now_txt = datetime.now().strftime("%Y-%m-%d %H:%M")
        text = f"현재 시각은 {now_txt}입니다."
        self.slack_bot.post_thread_message(self.slack_interact_channel, message['ts'], text)
        return

    def _response_redis_message_count(self, message:dict) -> None:
        redis_data_count = len(list(self.common.redis.scan_iter("*")))
        text = f"현재 redis에 적재된 메시지 수는 {redis_data_count:,}개 입니다."
        self.slack_bot.post_thread_message(self.slack_interact_channel, message['ts'], text)

    def _response_redis_truncate(self, message:dict) -> None:
        redis_data = list(self.common.redis.scan_iter("*"))
        redis_data_count = len(redis_data)
        for key in redis_data:
            self.common.redis.delete(key)
        text = f"{redis_data_count}개의 데이터를 제거하였습니다"
        self.slack_bot.post_thread_message(self.slack_interact_channel, message['ts'], text)

    def execute_each_message(self, message):
        now_txt = datetime.now().strftime("%Y-%m-%d %H:%M")

        if message['text'] == "지금 시각은?":
            self._response_now_time(message)

        if message['text'] == "redis에 메시지 몇 개 적재됐어?":
            self._response_redis_message_count(message)

        if message['text'] == "redis 싹 비워!":
            self._response_redis_truncate(message)

        self.common.to_redis(f"{message['user']}_{message['ts']}", message['text'])

    def _run(self):
        messages = self.slack_bot.get_messages(self.slack_interact_channel, self.history_period)
        messages = [message for message in messages if not self.common.from_redis(f"{message['user']}_{message['ts']}")]

        for message in messages:
            self.execute_each_message(message)




if __name__ == "__main__":
    main = Main()
    while True:
        main.run()
        time.sleep(1)