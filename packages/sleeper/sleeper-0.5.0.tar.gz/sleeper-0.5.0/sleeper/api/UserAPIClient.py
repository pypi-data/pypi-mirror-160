from sleeper.api.SleeperAPIClient import SleeperAPIClient
from sleeper.model.User import User


class UserAPIClient(SleeperAPIClient):

    @classmethod
    def get_user(cls, *, username: str = None, user_id: str = None) -> User:
        if username is None and user_id is None:
            raise ValueError("Must pass 'username' or 'user_id'.")
        user_arg = username if username is not None else user_id
        url = cls._build_route(cls._SLEEPER_APP_BASE_URL, cls._VERSION, cls._USER_ROUTE, f"{user_arg}")
        return User.from_dict(cls._get(url))
