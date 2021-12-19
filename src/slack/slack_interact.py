from datetime import datetime, timedelta
from slack_sdk import WebClient
import redis


class SlackBot:
    """
    슬랙 API 핸들러
    """

    def __init__(self, common):

        self.common = common
        self.conf = self.common.conf
        self.client = WebClient(self.conf['slack_bot_token'])


    def get_messages(self, channel_id:str, history_period:int=60) -> list:
        """
        주어진 channel_id에서
        최근 history_period(minute) 이내의 메시지 반환
        """
        now = datetime.now()
        before_dt = now - timedelta(minutes=history_period)

        result = self.client.conversations_history(channel=channel_id, oldest=before_dt.timestamp())
        messages = result.data['messages']
        print(f"최근 메시지 개수: {len(messages)}")

        return messages


    def post_thread_message(self, channel_id:str, message_ts:str, text:str):
        """
        슬랙 채널 내 메세지의 Thread에 댓글 달기
        """
        result = self.client.chat_postMessage(
            channel=channel_id,
            text=text,
            thread_ts=message_ts
        )
        return result

    def post_message(self, channel_id:str, text:str):
        result = self.client.chat_postMessage(
            channel=channel_id,
            text=text
        )
        return result
