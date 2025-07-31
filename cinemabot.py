# type: ignore
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from random import choice
from sqlite3 import Connection
from os import environ
import asyncio
import aiohttp
import textwrap
from utils import greetings, search_url, create_message, get_time, hist_str, stat_str


dp = Dispatcher()


@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.answer(
        f"Здорова, {choice(greetings)}! Если хочешь посмотреть кинчик, то ты попал(-а) по адресу!\n"
        "Вводи название или /help\n"
    )


@dp.message(Command('help'))
async def send_help(message: types.Message):
    await message.answer(
        f"{choice(greetings)}, чтобы выполнить поиск, просто укажи название фильма\n"
        "/help - для вызова справки\n"
        "/history - показать историю\n"
        "/stats - показать статистику"
    )


@dp.message(Command('stats'))
async def show_stats(message: types.Message):
    user_id = message.chat.id
    connection = Connection("search_database.db")
    cursor = connection.cursor()
    cursor.execute(textwrap.dedent(
        """
        SELECT result, COUNT(result) FROM search_records
        WHERE user_id = :user_id_
        AND result != "Not Found"
        GROUP BY result
        """).strip(),
        {"user_id_": user_id}
    )
    stats = cursor.fetchall()
    cursor.close()
    connection.close()
    await message.answer(
        "```Статистика\n" +
        "Фильм                 Число показов\n" +
        "\n".join([stat_str(stat) for stat in stats]) +
        "\n```",
        parse_mode="Markdown"
    )


@dp.message(Command('history'))
async def show_history(message: types.Message):
    user_id = message.chat.id
    connection = Connection("search_database.db")
    cursor = connection.cursor()
    cursor.execute(textwrap.dedent(
        """
        SELECT query, result, time FROM search_records
        WHERE user_id = :user_id_
        """).strip(),
        {"user_id_": user_id}
    )
    history = cursor.fetchall()
    cursor.close()
    connection.close()
    await message.answer(
        "```История\n" +
        "Запрос                 Фильм                  Время\n" +
        "\n".join([hist_str(hist) for hist in history]) +
        "\n```",
        parse_mode="Markdown"
    )


SEARCH_TOKEN = environ["SEARCH_TOKEN"]
search_headers = {
    "accept": "application/json",
    "X-API-KEY": SEARCH_TOKEN
}


async def add_record(user_id, query, html, success):
    connection = Connection("search_database.db")
    cursor = connection.cursor()
    cursor.execute(textwrap.dedent(
        """
        INSERT INTO search_records (user_id, query, result, time)
        VALUES (?, ?, ?, ?)
        """).strip(),
        (user_id, query, html["docs"][0]["name"] if success else "Not Found", get_time())
    )
    connection.commit()
    cursor.close()
    connection.close()


@dp.message()
async def search_movie(message: types.Message):
    movie = message.text
    async with aiohttp.ClientSession() as session:
        async with session.get(search_url(movie), headers=search_headers) as response:
            html = await response.json()
            success = "docs" in html and html["docs"]
            if not success:
                await message.answer("Ничего не найдено")
            else:
                await message.answer_photo(
                    photo=html["docs"][0]["poster"]["url"],
                    caption=create_message(html["docs"][0]),
                    parse_mode="Markdown"
                )
    await add_record(message.chat.id, movie, html, success)


BOT_TOKEN = environ["BOT_TOKEN"]


async def main() -> None:
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
