# slack_interactive

### Info
- 본 레포는 Slack으로 서버와 통신하여 유저가 정해진 명령어를 입력시 해당 동작을 서버에서 수행하는 코드가 담겨있습니다.
- 서버에는 local에 redis가 구동되고 있다고 가정되어있으며, 해당 정보는 conf에 기술되어 있어야 합니다. (뒤에 자세히 기술)
- 슬랙 token과 channel id는 사전에 기록되어있다고 가정합니다.
- interact 채널에서 명령어를 입력할 수 있으며, 수행된 메시지는 redis에 적재되어 두 번 수행되지 않습니다.
- 작동은 실시간이 아니며 1초 단위로 동작합니다. (준실시간)
- 에러 발생시 report 채널로 알람이 가며, 에러 감지 이후에는 1분간 작동하지 않습니다.

### conf 구성
- conf는 다음과 같이 구성됩니다
{
  "slack_bot_token": "",
  "redis":{
    "host": "",
    "port": "",
    "db":""
  },
  "slack_channel_ids": {
    "general": "",
    "report": "",
    "interact": ""
  }

}

### 
