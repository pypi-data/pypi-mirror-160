from dataclasses import dataclass
from typing import Optional, List


@dataclass
class PodcastValueDestination:
    split: int
    address: str
    name: Optional[str] = None
    fee: bool = False


@dataclass
class PodcastValue:
    destinations: List[PodcastValueDestination]
    suggested: Optional[str] = None

