from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
import emoji

from src.cinema import Cinema
from src import message as msg
from src import keyboards as kb

from src.sqlalchemy_declarative import Base, Movies, User, engine
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///movies.db')
Base.metadata.bind = engine

DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()

bot = Bot(token='5885167047:AAFlKgCUBX13LYSMveIzlsjaSyE_NinJNLI')
dp = Dispatcher(bot)

cinema = Cinema()


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message) -> None:
    await bot.send_message(message.chat.id, msg.START_MSG)
    await rating_message(message)
    with Session(engine) as session:
        new_user = User(id_of_user=message.chat.id)
        session.add_all([new_user])
        session.commit()


@dp.message_handler(commands=["help"])
async def send_help(message: types.Message) -> None:
    await bot.send_message(message.chat.id, msg.HELP_MSG)


@dp.message_handler(Text(equals="Команда"))
async def with_puree(message: types.Message):
    await message.reply("Which one? Please, write the name of the movie.")


@dp.message_handler()
async def get_info(message: types.Message) -> None:
    try:
        if "stupid bot" in message.text:
            await message.delete()
            await bot.send_message(message.chat.id, msg.EXEPT_MSG)
        else:
            movie_title = message.text
            for userr in session.query(User).filter(User.id_of_user == message.chat.id):
                info = await cinema.search(movie_title, userr.rating)
            if info == msg.ERROR_MSG:
                info = ''
                for film in session.query(Movies).filter(Movies.title == movie_title):
                    info += film.title + '\n' + film.description + '\n' + film.movie_url + '\n'
                if len(info) == 0:
                    info = msg.ERROR_MSG

            await bot.send_message(message.chat.id, text=info)
    except Exception:
        await bot.send_message(message.chat.id, msg.CON_LOST_MSG)


@dp.callback_query_handler(lambda callback_query: True)
async def process_callback(callback_query: types.CallbackQuery):
    data = callback_query.data.split('_')
    await bot.answer_callback_query(callback_query.id)
    if data[0] == 'rating':
        for userr in session.query(User).filter(User.id_of_user == callback_query.from_user.id):
            userr.rating = data[1]


async def rating_message(message: types.Message):
    adult_text = 'Do you want to turn on the rating filter(will be shown movies with rating higher than 6.0)?'

    await bot.send_message(message.chat.id, emoji.emojize(adult_text), reply_markup=kb.inline_rating_kb)


if __name__ == '__main__':
    executor.start_polling(dp)
