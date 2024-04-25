import logging
from telegram.ext import Application, MessageHandler, filters, ConversationHandler
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from data import db_session
from config import BOT_TOKEN
from dispatcher import User, Dispatcher

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

disp = Dispatcher()


async def start(update, context):
    reply_keyboard = [['/submit_your_application']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=True)
    await update.message.reply_text(
        "Привет. Я SysAdminBot.\n"
        "С какой проблеммой вы пришли ко мне?",
        reply_markup=markup
    )


async def submit_your_application(update, context):
    id_user = update["message"]["from_user"]["id"]
    if not disp.check_user(id_user):
        disp.users[id_user] = User(id_user)
    disp.users[id_user].state = 1
    await update.message.reply_text(
        "Для начала напишите свое ФИО "
    )


async def echo(update, context):
    id_user = update["message"]["from_user"]["id"]
    if not disp.check_user(id_user):
        reply_keyboard = [['/submit_your_application']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=True)
        await update.message.reply_text(
            "Привет. Я SysAdminBot.\n"
            "С какой проблеммой вы пришли ко мне?",
            reply_markup=markup
        )
    else:
        if disp.users[id_user].state == 1:
            fio = update.message.text
            disp.users[id_user].fio = fio
            disp.users[id_user].state = 2
            print(disp.users[id_user].fio)
            await update.message.reply_text(
                "Ваше данные сохранены. Опишите проблемму!")
        elif disp.users[id_user].state == 2:
            problem = update.message.text
            disp.users[id_user].problem = problem
            disp.users[id_user].state = 3
            print(disp.users[id_user].problem)
            await update.message.reply_text(
                "Введите место, куда подойти для решение проблеммы.")
        elif disp.users[id_user].state == 3:
            address = update.message.text
            disp.users[id_user].address = address
            disp.users[id_user].state = 3
            print(disp.users[id_user].address)
            await update.message.reply_text(
                "Черновик заявки принят, выберите нужное действие.",
            )
        else:
            await update.message.reply_text(
            "Что то пошло не так, введите команду \start.")





async def check(update, context):
    reply_keyboard = [['/viewing', '/send'],
                      ['/change']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=True)
    await update.message.reply_text(
        "Выбирите действие",
        reply_markup=markup
    )


async def viewing(update, context):
    id_user = update["message"]["from_user"]["id"]
    await update.message.reply_text(
        f"от: {disp.users[id_user].fio}\n описание: {disp.users[id_user].problem}\nместо: {disp.users[id_user].address}")


async def send(update, context):
    await update.message.reply_text(
        "Ваша заявка успешно отправлена!")


async def change(update, context):
    await update.message.reply_text("Выбирите, что бы вы хотели изменить в своей заявке")


async def change(update, context):
    pass


async def close_keyboard(update, context):
    await update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("submit_your_application", submit_your_application))

    application.add_handler(CommandHandler("close_keyboard", close_keyboard))
    text_handler = MessageHandler(filters.TEXT, echo)
    application.add_handler(text_handler)
    #db_session.global_init("db/applications.db")
    #db_sess = db_session.create_session()
    application.run_polling()


if __name__ == '__main__':
    main()
