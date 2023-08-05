from sleeper.api.SleeperAPIClient import SleeperAPIClient
from sleeper.enum.Sport import Sport
from sleeper.model.League import League
from sleeper.model.Matchup import Matchup
from sleeper.model.PlayoffMatchup import PlayoffMatchup
from sleeper.model.Roster import Roster
from sleeper.model.SportState import SportState
from sleeper.model.TradedPick import TradedPick
from sleeper.model.Transaction import Transaction
from sleeper.model.User import User


class LeagueAPIClient(SleeperAPIClient):

    @classmethod
    def get_league(cls, *, league_id: str) -> League:
        url = cls._build_route(cls._SLEEPER_APP_BASE_URL, cls._VERSION, cls._LEAGUE_ROUTE, league_id)
        return League.from_dict(cls._get(url))

    @classmethod
    def get_user_leagues_for_year(cls, *, user_id: str, sport: Sport, year: str) -> list[League]:
        url = cls._build_route(cls._SLEEPER_APP_BASE_URL, cls._VERSION, cls._USER_ROUTE, user_id, cls._LEAGUES_ROUTE,
                               sport.value.lower(), year)
        return League.from_dict_list(cls._get(url))

    @classmethod
    def get_rosters(cls, *, league_id: str) -> list[Roster]:
        url = cls._build_route(cls._SLEEPER_APP_BASE_URL, cls._VERSION, cls._LEAGUE_ROUTE, league_id,
                               cls._ROSTERS_ROUTE)
        return Roster.from_dict_list(cls._get(url))

    @classmethod
    def get_users_in_league(cls, *, league_id: str) -> list[User]:
        url = cls._build_route(cls._SLEEPER_APP_BASE_URL, cls._VERSION, cls._LEAGUE_ROUTE, league_id, cls._USERS_ROUTE)
        return User.from_dict_list(cls._get(url))

    @classmethod
    def get_matchups_for_week(cls, *, league_id: str, week: int) -> list[Matchup]:
        url = cls._build_route(cls._SLEEPER_APP_BASE_URL, cls._VERSION, cls._LEAGUE_ROUTE, league_id,
                               cls._MATCHUPS_ROUTE, week)
        return Matchup.from_dict_list(cls._get(url))

    @classmethod
    def get_winners_bracket(cls, *, league_id: str) -> list[PlayoffMatchup]:
        url = cls._build_route(cls._SLEEPER_APP_BASE_URL, cls._VERSION, cls._LEAGUE_ROUTE, league_id,
                               cls._WINNERS_BRACKET_ROUTE)
        return PlayoffMatchup.from_dict_str(cls._get(url))

    @classmethod
    def get_losers_bracket(cls, *, league_id: str) -> list[PlayoffMatchup]:
        url = cls._build_route(cls._SLEEPER_APP_BASE_URL, cls._VERSION, cls._LEAGUE_ROUTE, league_id,
                               cls._LOSERS_BRACKET_ROUTE)
        return PlayoffMatchup.from_dict_str(cls._get(url))

    @classmethod
    def get_transactions(cls, *, league_id: str, week: int) -> list[Transaction]:
        url = cls._build_route(cls._SLEEPER_APP_BASE_URL, cls._VERSION, cls._LEAGUE_ROUTE, league_id,
                               cls._TRANSACTIONS_ROUTE, week)
        return Transaction.from_dict_list(cls._get(url))

    @classmethod
    def get_traded_picks(cls, *, league_id: str) -> list[TradedPick]:
        url = cls._build_route(cls._SLEEPER_APP_BASE_URL, cls._VERSION, cls._LEAGUE_ROUTE, league_id,
                               cls._TRADED_PICKS_ROUTE)
        return TradedPick.from_dict_list(cls._get(url))

    @classmethod
    def get_sport_state(cls, *, sport: Sport) -> SportState:
        url = cls._build_route(cls._SLEEPER_APP_BASE_URL, cls._VERSION, cls._STATE_ROUTE, sport.value.lower())
        return SportState.from_dict(cls._get(url))
