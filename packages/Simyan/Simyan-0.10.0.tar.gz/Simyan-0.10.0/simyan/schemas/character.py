"""
The Character module.

This module provides the following classes:

- Character
"""
__all__ = ["Character"]
import re
from datetime import date, datetime
from typing import List, Optional

from pydantic import Field

from simyan.schemas import BaseModel
from simyan.schemas.generic_entries import GenericEntry, ImageEntry, IssueEntry


class Character(BaseModel):
    r"""
    The Character object contains information for a character.

    Attributes:
        aliases: List of names used by the Character, separated by `~\r\n`.
        api_url: Url to the resource in the Comicvine API.
        creators: List of creators which worked on the Character.
        date_added: Date and time when the Character was added.
        date_last_updated: Date and time when the Character was last updated.
        date_of_birth: Date when the Character was born.
        deaths: List of times when the Character has died.
        description: Long description of the Character.
        enemies: List of enemies the Character has.
        enemy_teams: List of enemy teams the Character has.
        first_issue: First issue the Character appeared in.
        friendly_teams: List of friendly teams the Character has.
        friends: List of friends the Character has.
        gender: Character gender.
        id_: Identifier used by Comicvine. **Deprecated:** Use character_id instead
        character_id: Identifier used by Comicvine.
        image: Different sized images, posters and thumbnails for the Character.
        issue_count: Number of issues the Character appears in.
        issues: List of issues the Character appears in.
        name: Real name or public identity of Character.
        origin: The type of Character.
        powers: List of powers the Character has.
        publisher: The publisher of the Character.
        real_name: Name of the Character.
        site_url: Url to the resource in Comicvine.
        story_arcs: List of story arcs the Character appears in.
        summary: Short description of the Character.
        teams: List of teams the Character appears in.
        volumes: List of volumes the Character appears in.
    """

    aliases: Optional[str] = None
    api_url: str = Field(alias="api_detail_url")
    creators: List[GenericEntry] = Field(default_factory=list)
    date_added: datetime
    date_last_updated: datetime
    date_of_birth: Optional[date] = Field(default=None, alias="birth")
    deaths: List[GenericEntry] = Field(default_factory=list, alias="issues_died_in")
    description: Optional[str] = None
    enemies: List[GenericEntry] = Field(default_factory=list, alias="character_enemies")
    enemy_teams: List[GenericEntry] = Field(default_factory=list, alias="team_enemies")
    first_issue: IssueEntry = Field(alias="first_appeared_in_issue")
    friendly_teams: List[GenericEntry] = Field(default_factory=list, alias="team_friends")
    friends: List[GenericEntry] = Field(default_factory=list, alias="character_friends")
    gender: int
    id_: int = Field(alias="id")
    character_id: int = Field(alias="id")
    image: ImageEntry
    issue_count: Optional[int] = Field(default=None, alias="count_of_issue_appearances")
    issues: List[GenericEntry] = Field(default_factory=list, alias="issue_credits")
    name: str
    origin: Optional[GenericEntry] = None
    powers: List[GenericEntry] = Field(default_factory=list)
    publisher: GenericEntry
    real_name: Optional[str] = None
    site_url: str = Field(alias="site_detail_url")
    story_arcs: List[GenericEntry] = Field(default_factory=list, alias="story_arc_credits")
    summary: Optional[str] = Field(default=None, alias="deck")
    teams: List[GenericEntry] = Field(default_factory=list)
    volumes: List[GenericEntry] = Field(default_factory=list, alias="volume_credits")

    @property
    def alias_list(self) -> List[str]:
        r"""
        List of aliases the Character has used.

        Returns:
            List of aliases, split by `~\r\n`
        """
        return re.split(r"[~\r\n]+", self.aliases) if self.aliases else []
