import logging

from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram.ext import Application, MessageHandler, filters
from telegram.ext import CommandHandler

from config import BOT_TOKEN
from data import db_session
from data.problem import Problem
from dispatcher import User, Dispatcher
from table import create_table_problem
from jinja2 import Template
from templates_messages import temp_mes, temp_mes_edit, temp_mes_user

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

disp = Dispatcher()
ADMIN = {5054360906: {
    'status': 0,
    'id_user': None
}}

async def start(update, context):
    id_user = update["message"]["from_user"]["id"]
    if id_user in ADMIN:
        reply_keyboard = [['/view_active_problems'], ['/get_all_problems'], ['/edit_status_problems'], ['/write_user']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=True)
        await update.message.reply_text(
            "Привет. Я SysAdminBot.\n"
            "Выбирите действие!",
            reply_markup=markup
        )
    else:
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
    if id_user in ADMIN:
        if ADMIN[id_user]['status'] == 1:
            try:
                id_problem = int(update.message.text)
                db_sess = db_session.create_session()
                problem = db_sess.query(Problem).filter(Problem.id == id_problem).first()
                problem.status = True
                db_sess.commit()
                ADMIN[id_user]['status'] = 0
                await context.bot.send_message(chat_id=problem.id_user, text=f'Ваша заявка {problem.id} выполнена!')
                await update.message.reply_text(
                    "Статус заявки изменен, автору заявки отправлено уведомление"
                )
            except Exception:
                await update.message.reply_text(
                    "Я вас не понял, давйте начнем сначала\n"
                    "Введите id заявки еще раз или введите команду /start"
                )

        elif ADMIN[id_user]['status'] == 2:
            try:
                id_problem = int(update.message.text)
                db_sess = db_session.create_session()
                problem = db_sess.query(Problem).filter(Problem.id == id_problem).first()
                ADMIN[id_user]['status'] = 3
                ADMIN[id_user]['id_user'] = problem.id_user
                await update.message.reply_text(
                    "Пользователь найден. Введите текст сообщения"
                )
            except Exception:
                await update.message.reply_text(
                    "Я вас не понял, давайте начнем сначала\n"
                    "Введите id заявки еще раз или введите команду /start"
                )
        elif ADMIN[id_user]['status'] == 3 and ADMIN[id_user]['id_user']:
            try:
                reply_keyboard = [['/write_message'], ['/start_over']]
                markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=True)
                await context.bot.send_message(chat_id=ADMIN[id_user]['id_user'], text=update.message.text)
                await update.message.reply_text(
                    "Сообщение отправлено, выберите действие",
                    reply_markup=markup
                )
            except Exception:
                await update.message.reply_text(
                    "Я вас не понял, давйте начнем сначала\n"
                    "Введите id заявки еще раз или введите команду /start")
        else:
            reply_keyboard = [['/view_active_problems'], ['/get_all_problems'], ['/edit_status_problems'], ['/write_user']]
            markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=True)
            await update.message.reply_text(
                "Я вас не понял, давйте начнем сначала\n"
                "Выбирите действие!",
                reply_markup=markup
            )
    elif not disp.check_user(id_user):
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
            if disp.users[id_user].update:
                disp.users[id_user].state = 4
                disp.users[id_user].update = False
                reply_keyboard = [['/viewing', '/send'],
                                  ['/update']]
                markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=True)
                await update.message.reply_text(
                    "Черновик заявки принят, выберите нужное действие.\nВыбирите действие",
                    reply_markup=markup)
            else:
                await update.message.reply_text(
                    "Ваше данные сохранены. Опишите проблемму!")
        elif disp.users[id_user].state == 2:
            problem = update.message.text
            disp.users[id_user].problem = problem
            disp.users[id_user].state = 3
            if disp.users[id_user].update:
                disp.users[id_user].state = 4
                disp.users[id_user].update = False
                reply_keyboard = [['/viewing', '/send'],
                                  ['/update']]
                markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=True)
                await update.message.reply_text(
                    "Черновик заявки принят, выберите нужное действие.\nВыбирите действие",
                    reply_markup=markup)
            else:
                await update.message.reply_text(
                    "Введите место, куда подойти для решение проблеммы.")
        elif disp.users[id_user].state == 3:
            address = update.message.text
            disp.users[id_user].address = address
            disp.users[id_user].state = 4
            if disp.users[id_user].update:
                disp.users[id_user].state = 4
                disp.users[id_user].update = False
                reply_keyboard = [['/viewing', '/send'],
                                  ['/update']]
                markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=True)
                await update.message.reply_text(
                    "Черновик заявки принят, выберите нужное действие.\nВыбирите действие",
                    reply_markup=markup)
            else:
                reply_keyboard = [['/viewing', '/send'],
                                  ['/update']]
                markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=True)
                await update.message.reply_text(
                    "Черновик заявки принят, выберите нужное действие.\nВыбирите действие",
                    reply_markup=markup
                )

        else:
            await update.message.reply_text(
            "Что то пошло не так, введите команду \start.")


async def viewing(update, context):
    id_user = update["message"]["from_user"]["id"]
    await update.message.reply_text(
        f"от: {disp.users[id_user].fio}\nописание: {disp.users[id_user].problem}\nместо: {disp.users[id_user].address}")


async def send(update, context):
    id_user = update["message"]["from_user"]["id"]
    db_sess = db_session.create_session()
    problem = Problem()
    problem.id_user = id_user
    problem.fio = disp.users[id_user].fio
    problem.content = disp.users[id_user].problem
    problem.adress = disp.users[id_user].address
    db_sess.add(problem)
    db_sess.commit()
    for id_admin in ADMIN:
        await context.bot.send_message(chat_id=id_admin, text=f'Поступила заявка от {disp.users[id_user].fio}\n'
                                                          f'Описание: {disp.users[id_user].problem}')
    await update.message.reply_text(
        "Ваша заявка успешно отправлена!")


async def update_data(update, context):
    reply_keyboard = [['/update_fio', '/update_problem'],
                      ['/update_address']]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=True)
    await update.message.reply_text("Выбирите, что бы вы хотели изменить в своей заявке", reply_markup=markup)


async def update_fio(update, context):
    id_user = update["message"]["from_user"]["id"]
    disp.users[id_user].state = 1
    disp.users[id_user].update = True
    await update.message.reply_text(
        "Введите новое имя"
    )


async def update_problem(update, context):
    id_user = update["message"]["from_user"]["id"]
    disp.users[id_user].state = 2
    disp.users[id_user].update = True
    await update.message.reply_text(
        "Опишите проблемму снова")


async def update_address(update, context):
    id_user = update["message"]["from_user"]["id"]
    disp.users[id_user].state = 3
    disp.users[id_user].update = True
    await update.message.reply_text(
        "Введите еще раз адрес",
    )

async def view_problems(update, context):
    id_user = update["message"]["from_user"]["id"]
    if id_user in ADMIN:
        db_sess = db_session.create_session()
        problems = db_sess.query(Problem).filter(Problem.status == False).all()
        await update.message.reply_text(
            Template(temp_mes).render(problems=problems))
    else:
        await update.message.reply_text(
            "Недостаточно прав для просмотра заявок\nВведите команду /start для начала работы с ботом")

async def get_problems(update, context):
    id_user = update["message"]["from_user"]["id"]
    if id_user in ADMIN:
        create_table_problem()
        await update.message.reply_text(
            "Выгружаем все заявки")
        await context.bot.send_document(chat_id=id_user, document=open("temp/problems.xlsx", "rb"))
    else:
        await update.message.reply_text(
            "Недостаточно прав для просмотра заявок\nВведите команду /start для начала работы с ботом")


async def edit_status(update, context):
    id_user = update["message"]["from_user"]["id"]
    if id_user in ADMIN:
        ADMIN[id_user]['status'] = 1
        db_sess = db_session.create_session()
        problems = db_sess.query(Problem).filter(Problem.status == False).all()
        await update.message.reply_text(
            Template(temp_mes_edit).render(problems=problems))
    else:
        await update.message.reply_text(
            "Недостаточно прав для просмотра заявок\nВведите команду /start для начала работы с ботом")

async def write_user(update, context):
    id_user = update["message"]["from_user"]["id"]
    if id_user in ADMIN:
        ADMIN[id_user]['status'] = 2
        db_sess = db_session.create_session()
        problems = db_sess.query(Problem).filter(Problem.status == False).all()
        await update.message.reply_text(
            Template(temp_mes_user).render(problems=problems))
    else:
        await update.message.reply_text(
            "Недостаточно прав для просмотра заявок\nВведите команду /start для начала работы с ботом")


async def write_message(update, context):
    id_user = update["message"]["from_user"]["id"]
    if id_user in ADMIN:
        await update.message.reply_text('Введите текст сообщения')
    else:
        await update.message.reply_text(
            "Недостаточно прав для просмотра заявок\nВведите команду /start для начала работы с ботом")


async def start_over(update, context):
    id_user = update["message"]["from_user"]["id"]
    if id_user in ADMIN:
        ADMIN[id_user]['status'] = 2
        ADMIN[id_user]['id_user'] = None
        reply_keyboard = [['/view_active_problems'], ['/get_all_problems'], ['/edit_status_problems'], ['/write_user']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False, resize_keyboard=True)
        await update.message.reply_text(
            "Начнем сначала\n"
            "Выбирите действие!",
            reply_markup=markup
        )
    else:
        await update.message.reply_text(
            "Недостаточно прав для просмотра заявок\nВведите команду /start для начала работы с ботом")


async def close_keyboard(update, context):
    await update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("submit_your_application", submit_your_application))
    application.add_handler(CommandHandler("send", send))
    application.add_handler(CommandHandler("viewing", viewing))
    application.add_handler(CommandHandler("update", update_data))
    application.add_handler(CommandHandler("update_fio", update_fio))
    application.add_handler(CommandHandler("update_problem", update_problem))
    application.add_handler(CommandHandler("update_address", update_address))
    application.add_handler(CommandHandler("close_keyboard", close_keyboard))
    application.add_handler(CommandHandler("view_active_problems", view_problems))
    application.add_handler(CommandHandler("get_all_problems", get_problems))
    application.add_handler(CommandHandler("edit_status_problems", edit_status))
    application.add_handler(CommandHandler("write_user", write_user))
    application.add_handler(CommandHandler("write_message", write_message))
    application.add_handler(CommandHandler("start_over", start_over))
    text_handler = MessageHandler(filters.TEXT, echo)
    application.add_handler(text_handler)
    db_session.global_init("db/applications.db")

    application.run_polling()


if __name__ == '__main__':
    main()
