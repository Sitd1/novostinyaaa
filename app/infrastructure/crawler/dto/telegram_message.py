import datetime
from dataclasses import dataclass


@dataclass
class TelegramMessageDTO:
    message_id: int
    channel_username: str
    text: str
    date: datetime
