from sleeper.api.SleeperAPIClient import SleeperAPIClient
from sleeper.enum.Sport import Sport
from sleeper.model.Draft import Draft
from sleeper.model.DraftPick import DraftPick
from sleeper.model.PlayerDraftPick import PlayerDraftPick


class DraftAPIClient(SleeperAPIClient):

    @classmethod
    def get_user_drafts_for_year(cls, *, user_id: str, sport: Sport, year: str) -> list[Draft]:
        url = cls._build_route(cls._SLEEPER_APP_BASE_URL, cls._VERSION, cls._USER_ROUTE, user_id, cls._DRAFTS_ROUTE,
                               sport.name.lower(), year)
        return Draft.from_dict_list(cls._get(url))

    @classmethod
    def get_drafts_in_league(cls, *, league_id: str) -> list[Draft]:
        url = cls._build_route(cls._SLEEPER_APP_BASE_URL, cls._VERSION, cls._LEAGUE_ROUTE, league_id, cls._DRAFTS_ROUTE)
        return Draft.from_dict_list(cls._get(url))

    @classmethod
    def get_draft(cls, *, draft_id: str) -> Draft:
        url = cls._build_route(cls._SLEEPER_APP_BASE_URL, cls._VERSION, cls._DRAFT_ROUTE, draft_id)
        return Draft.from_dict(cls._get(url))

    @classmethod
    def get_player_draft_picks(cls, *, draft_id: str, sport: Sport) -> list[PlayerDraftPick]:
        url = cls._build_route(cls._SLEEPER_APP_BASE_URL, cls._VERSION, cls._DRAFT_ROUTE, draft_id, cls._PICKS_ROUTE)
        return PlayerDraftPick.from_dict_list(cls._get(url), sport)

    @classmethod
    def get_traded_draft_picks(cls, *, draft_id: str) -> list[DraftPick]:
        url = cls._build_route(cls._SLEEPER_APP_BASE_URL, cls._VERSION, cls._DRAFT_ROUTE, draft_id,
                               cls._TRADED_PICKS_ROUTE)
        return DraftPick.from_dict_list(cls._get(url))
