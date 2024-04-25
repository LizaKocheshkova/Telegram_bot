application.add_handler(CommandHandler("help_command", help_command))
application.add_handler(CommandHandler("make_an_appointment", make_an_appointment))
application.add_handler(CommandHandler("contact", contact))
application.add_handler(CommandHandler("recording_time", recording_time))

async def help_command(update, context):
    await update.message.reply_text(
        "Чем я могу быть полезен?")


async def make_an_appointment(update, context):
    await update.message.reply_text(
        "Записываю вас в нашу базу.")


async def contact(update, context):
    await update.message.reply_text("Связываю вас с администратором")


async def recording_time(update, context):
    await update.message.reply_text(
        "Вы записаны на ... число, на ... время.")



Update(message=Message(channel_chat_created=False, chat=Chat(first_name='Лиза', id=6618777856, type=<ChatType.PRIVATE>, username='KED_1034'), date=datetime.datetime(2024, 4, 24, 18, 37, 30, tzinfo=<UTC>), delete_chat_photo=False, from_user=User(first_name='Лиза', id=6618777856, is_bot=False, language_code='ru', username='KED_1034'), group_chat_created=False, message_id=1123, supergroup_chat_created=False, text='sdfghjkl'), update_id=858087561)


