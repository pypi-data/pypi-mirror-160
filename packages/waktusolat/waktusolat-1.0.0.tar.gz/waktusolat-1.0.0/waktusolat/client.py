from typing import Any, Optional

from requests import Response, Session
from requests.exceptions import ConnectionError as ReqConnErr

from .exceptions import APIError
from .exceptions import ConnectionError as APIConnErr


class WaktuSolat:
    BASE_URL = "https://waktu-solat-api.herokuapp.com/api/v1"

    def __init__(self) -> None:
        self.session = Session()

    def _get(self, url: str) -> Response:
        try:
            resp = self.session.get(url)
            if resp.status_code == 404:
                raise APIError("API not found", resp.status_code)
            return resp
        except ReqConnErr:
            raise APIConnErr("Can't fetch API")

    def _fix_param(self, param: str) -> str:
        return "_".join(param.lower().split(" "))

    def states(self, /, *, negeri: Optional[str] = None) -> dict[Any, Any]:
        url = f"{self.BASE_URL}/states.json"
        resp = self._get(url)

        if negeri is not None:
            negeri = self._fix_param(negeri)
            url = f"{url}?negeri={negeri}"
            resp = self._get(url)

        return resp.json()["data"]

    def zones(self, /, *, zon: Optional[str] = None) -> dict[Any, Any]:
        url = f"{self.BASE_URL}/zones.json"
        resp = self._get(url)

        if zon is not None:
            zon = self._fix_param(zon)
            url = f"{url}?zon={zon}"
            resp = self._get(url)

        return resp.json()["data"]

    def prayer_times(
        self, /, *, zon: Optional[str] = None, negeri: Optional[str] = None
    ) -> dict[Any, Any]:
        url = f"{self.BASE_URL}/prayer_times.json"
        resp = self._get(url)

        if zon is not None and negeri is None:
            zon = self._fix_param(zon)
            url = f"{url}?zon={zon}"
            resp = self._get(url)
        elif zon is None and negeri is not None:
            negeri = self._fix_param(negeri)
            url = f"{url}?negeri={negeri}"
            resp = self._get(url)
        elif zon is not None and negeri is not None:
            zon = self._fix_param(zon)
            negeri = self._fix_param(negeri)
            url = f"{url}?zon={zon}&negeri={negeri}"
            resp = self._get(url)

        return resp.json()["data"]
