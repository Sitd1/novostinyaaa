from dataclasses import dataclass

from sources.value_objects import (
    Url,
    SourceId,
    SourceType,
    SourceName,
    SourceTitle,
    SourceDescription,
    ExternalSourceId,

    TgSourceName,
)


@dataclass(frozen=True)
class Source:
    id: SourceId | None            # auto-increment in DB
    type: SourceType               # enum: TELEGRAM, RSS, API, OTHER
    name: SourceName               # username: "meduza_tg_main"
    title: SourceTitle             # display name: "Meduza"
    external_id: ExternalSourceId | None = None
    description: SourceDescription | None = None
    url: Url | None = None

    @classmethod
    def telegram(
        cls,
        username: str,  #@sitd1
        title: str,
        channel_code: str | None = None,
        url: str | None = None,
        description: str | None = None,
    ) -> "Source":

        return cls(
            id=None,
            type=SourceType.TELEGRAM,
            name=TgSourceName(username),
            title=SourceTitle(title),
            external_id=ExternalSourceId(channel_code) if channel_code else None,
            description=SourceDescription(description) if description else None,
            url=Url(url) if url else None,
        )
