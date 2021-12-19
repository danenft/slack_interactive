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
        rd = redis.StrictRedis(**self.conf['redis'])

    def get_messages(self, channel_id:str, history_period:int=60):
        """
        주어진 channel_id에서
        최근 history_period(minute) 이내의 메시지 반환
        """
        now = datetime.now()
        before_dt = now - timedelta(minutes=history_period)

        result = self.client.conversations_history(channel=channel_id, oldest=before_dt.timestamp())
        # 채널 내 메세지 정보 딕셔너리 리스트
        messages = result.data['messages']
        print(f"최근 메시지 개수: {len(messages)}")
        return messages

    def post_thread_message(self, channel_id, message_ts, text):
        """
        슬랙 채널 내 메세지의 Thread에 댓글 달기
        """
        # chat_postMessage() 메서드 호출
        result = self.client.chat_postMessage(
            channel=channel_id,
            text=text,
            thread_ts=message_ts
        )
        return result