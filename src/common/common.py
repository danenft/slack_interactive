import json

import redis

class Common:

    def __init__(self):
        self.load_conf()
        self.redis = redis.StrictRedis(**self.conf['redis'])

    def load_conf(self):
        with open("../conf/conf.json", 'r') as f:
            self.conf = json.load(f)


    def to_redis(self, key, value):
        self.redis.set(key, value)

    def from_redis(self, key):
        return self.redis.get(key)

    def get_slack_channel_id(self,  channel_name:str):
        channel_id = self.conf.get('slack_channel_ids', {}).get(channel_name)
        if not channel_id:
            raise Exception(f"슬랙 채널 아이디가 존재하지 않습니다: {channel_name}")
        return channel_id
