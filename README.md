## Leonardo GiveMovie Telegram bot

Telegram tag: `@leo_give_movie_bot`

*Ever had someone mention a movie in a chat, and you realized you had no idea what it was or where to watch it?*
**This is where our smart Telegram bot comes in.** 

Built using the asynchronous `aiogram` library and powered by the `KinoPoisk API`, the bot can identify movies even from partial or approximate titles, returning the correct name, release year, rating, poster, and a brief description. It also provides a direct link to a third-party website where you can watch the film.

All user queries are stored in a `SQLite` database, allowing each user to view their search history with timestamps. Additionally, the bot aggregates all requests to show how many times each movie has been searched.

This project was developed as part of the Advanced Python Programming course at Yandex School of Data Analysis (Moscow). That is why the interface has Russian language. The main goal was to explore asynchronous network interaction with clients, design an application capable of handling user requests, integrate a modern database, and finally deploy the service to Amazon AWS for stable, production-ready performance.
