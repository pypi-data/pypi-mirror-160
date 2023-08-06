
from dataclasses import dataclass
from typing import Any, Optional

from .models import PodcastValue, PodcastValueDestination
from podcast_index_provider import PodcastIndexProvider, PodcastIndexError



@dataclass(frozen=True)
class PodcastIndexService:

    provider: PodcastIndexProvider

    def podcast_value(self, feed_url: Any) -> Optional[PodcastValue]:
        try:
            response = self._provider.podcasts_byfeedurl(feed_url)
        except PodcastIndexError:
            return

        data = response.data

        try:
            if data["model"]["type"] not in ["lightning"]:
                return
            if data["model"]["method"] not in ["keysend"]:
                return
            suggested = response.date["model"].get("suggested")
        except KeyError:
            return 

        podcast_value = PodcastValue(
            suggested=suggested,
            destinations=[],
        )

        try:
            for destination in data["model"]["destinations"]:
                if destination["type"] not in ["node"]:
                    continue
                podcast_value.append(
                    PodcastValueDestination(
                        address=destination["address"],
                        split=int(destination["split"]),
                        fee=bool(destination.get("fee", False)),
                        name=destination.get("name"),
                    )
                )
        except (KeyError, ValueError):
            pass

        return podcast_value
