from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from database import init_db, add_item, remove_item, get_items, add_admin, remove_admin, is_admin, get_admins


def admin_only(func):
    def wrapper(update, context):
        user_id = update.effective_user.id
        if is_admin(user_id):
            return func(update, context)
        else:
            update.message.reply_text('У вас нет прав для выполнения этой команды.')
    return wrapper

@admin_only
def add_account(update, context):
    name = ' '.join(context.args)
    if not name:
        update.message.reply_text('Используйте команду /add_account <название>')
        return
    result = add_item('accounts', name)
    if result:
        update.message.reply_text(f'Счет "{name}" добавлен.')
    else:
        update.message.reply_text(f'Счет "{name}" уже существует.')

@admin_only
def remove_account(update, context):
    name = ' '.join(context.args)
    if not name:
        update.message.reply_text('Используйте команду /remove_account <название>')
        return
    remove_item('accounts', name)
    update.message.reply_text(f'Счет "{name}" удален.')

@admin_only
def add_project(update, context):
    name = ' '.join(context.args)
    if not name:
        update.message.reply_text('Используйте команду /add_project <название>')
        return
    result = add_item('projects', name)
    if result:
        update.message.reply_text(f'Проект "{name}" добавлен.')
    else:
        update.message.reply_text(f'Проект "{name}" уже существует.')

@admin_only
def remove_project(update, context):
    name = ' '.join(context.args)
    if not name:
        update.message.reply_text('Используйте команду /remove_project <название>')
        return
    remove_item('projects', name)
    update.message.reply_text(f'Проект "{name}" удалён.')

@admin_only
def add_article(update, context):
    name = ' '.join(context.args)
    if not name:
        update.message.reply_text('Используйте команду /add_article <название>')
        return
    result = add_item('articles', name)
    if result:
        update.message.reply_text(f'Статья "{name}" добавлена.')
    else:
        update.message.reply_text(f'Статья "{name}" уже существует.')

@admin_only
def remove_article(update, context):
    name = ' '.join(context.args)
    if not name:
        update.message.reply_text('Используйте команду /remove_article <название>')
        return
    remove_item('articles', name)
    update.message.reply_text(f'Статья "{name}" удалена.')

@admin_only
def add_admin_command(update, context):
    if not context.args:
        update.message.reply_text('Используйте команду /add_admin <user_id>')
        return
    try:
        new_admin_id = int(context.args[0])
        if is_admin(new_admin_id):
            update.message.reply_text('Пользователь уже является администратором.')
            return
        result = add_admin(new_admin_id)
        if result:
            update.message.reply_text(f'Пользователь с ID {new_admin_id} добавлен в администраторы.')
        else:
            update.message.reply_text('Не удалось добавить администратора.')
    except ValueError:
        update.message.reply_text('User ID должен быть числом.')

@admin_only
def remove_admin_command(update, context):
    if not context.args:
        update.message.reply_text('Используйте команду /remove_admin <user_id>')
        return
    try:
        admin_id = int(context.args[0])
        if not is_admin(admin_id):
            update.message.reply_text('Пользователь не является администратором.')
            return
        if admin_id == update.effective_user.id:
            update.message.reply_text('Вы не можете удалить сами себя из администраторов.')
            return
        remove_admin(admin_id)
        update.message.reply_text(f'Пользователь с ID {admin_id} удалён из администраторов.')
    except ValueError:
        update.message.reply_text('User ID должен быть числом.')

@admin_only
def list_admins(update, context):
    admins = get_admins()
    if admins:
        admin_list = '\n'.join([str(admin_id) for admin_id in admins])
        update.message.reply_text(f'Список администраторов:\n{admin_list}')
    else:
        update.message.reply_text('Список администраторов пуст.')


def start(update: Update, context: CallbackContext):
    # Change to your server URL
    web_app_url = 'YOUR_URL'

    keyboard = [
        [KeyboardButton(text="Открыть форму", web_app=WebAppInfo(url=web_app_url))]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text('Нажмите кнопку ниже, чтобы открыть форму:', reply_markup=reply_markup)

def main():
    init_db()
    # Change to your token
    updater = Updater("YOUR_TOKEN", use_context=True)

    dp = updater.dispatcher

    updater.bot.set_my_commands([
        ('start', 'Запуск бота'),
        ('add_account', 'Добавить счет'),
        ('remove_account', 'Удалить счет'),
        ('add_project', 'Добавить проект'),
        ('remove_project', 'Удалить проект'),
        ('add_article', 'Добавить статью'),
        ('remove_article', 'Удалить статью'),
        ('add_admin', 'Добавить админа'),
        ('remove_admin', 'Удалить админа'),
        ('list_admins', 'Список админов')
    ])

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('add_account', add_account))
    dp.add_handler(CommandHandler('remove_account', remove_account))
    dp.add_handler(CommandHandler('add_project', add_project))
    dp.add_handler(CommandHandler('remove_project', remove_project))
    dp.add_handler(CommandHandler('add_article', add_article))
    dp.add_handler(CommandHandler('remove_article', remove_article))
    dp.add_handler(CommandHandler('add_admin', add_admin_command))
    dp.add_handler(CommandHandler('remove_admin', remove_admin_command))
    dp.add_handler(CommandHandler('list_admins', list_admins))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
