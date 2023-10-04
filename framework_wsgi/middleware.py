from urllib.parse import parse_qs, unquote
from uuid import uuid4
from .http import Response, Request


# MiddleWare: Интерфейс и Заглушка
class BaseMiddleWare:
    def process_request(self, request: Request):
        return

    def process_response(self, response: Response):
        return


class CookieMiddleWare(BaseMiddleWare):
    def process_request(self, request: Request):
        cookie_str = request.headers.get("COOKIE", "")

        exempt_keys = [
            "auth_key",
            "session",
        ]

        if cookie_str:
            for item in cookie_str.split(";"):
                key, value = item.strip().split("=", 1)

                if key not in exempt_keys:
                    request.cookies[key] = value  # Не применяем unquote
                else:
                    request.cookies[key] = unquote(value)  # Применяем unquote

    def process_response(self, response: Response):
        cookies_to_set = "; ".join(
            [f"{key}={value}" for key, value in response.request.cookies.items()]
        )
        if cookies_to_set:
            response.headers["Set-Cookie"] = cookies_to_set


class SessionMiddleWare(BaseMiddleWare):
    def process_request(self, request: Request):
        if "session" in request.cookies:
            request.session = request.cookies["session"]

    def process_response(self, response: Response):
        session = getattr(response.request, "session", None)
        if not session:
            set_cookie = response.headers.get("Set-Cookie", "")
            response.headers["Set-Cookie"] = (
                set_cookie + f"; session={uuid4()}; "
                if set_cookie
                else f"; session={uuid4()}"
            )


middlewares = [
    CookieMiddleWare(),
    SessionMiddleWare(),
]
