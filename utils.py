from yarl import URL
from typing import Any
from datetime import datetime
import zoneinfo


greetings = ["Бандит", "Салага", "Фраерок", "Щегол", "Мажор", "Деточка", "Дружище"]


def search_url(movie_name: str) -> str:
    return str(URL.build(
        scheme="https",
        host="api.kinopoisk.dev/v1.4",
        path="/movie/search",
        query={
            "page": 1,
            "limit": 10,
            "query": movie_name
        }
    ))


def watch_url(movie_id: int, is_series: bool) -> str:
    return str(URL.build(
        scheme="https",
        host="www.sspoisk.ru",
        path=f"/{"series" if is_series else "film"}/{movie_id}",
    ))


def create_message(doc: dict[str, Any]) -> str:
    message = (
        f"*{doc["name"]}* ({doc["year"]})\n"
        f"_Рейтинг_: {doc["rating"]["kp"]}\n"
        "_Описание:_\n"
    )
    return message + doc["description"] + f"\n\n[Посмотреть]({watch_url(doc["id"], doc["isSeries"])})"


DEFAULT_TZ_NAME = "Europe/Moscow"


def get_time() -> str:
    dt = datetime.now(tz=zoneinfo.ZoneInfo(DEFAULT_TZ_NAME))
    fmt = '%Y-%m-%dT%H:%M'
    return dt.strftime(fmt)


def stat_str(record: tuple[str, int]) -> str:
    result = record[0][:27].ljust(30)
    count = str(record[1]).rjust(5)
    return result + count


def hist_str(record: tuple[str, str, str]) -> str:
    query = record[0][:20].ljust(23)
    result = record[1][:20].ljust(23)
    return query + result + record[2]
