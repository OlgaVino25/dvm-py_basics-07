import ptbot
import os
from dotenv import load_dotenv
import pytimeparse


def render_progressbar(
        total,
        iteration,
        prefix='',
        suffix='',
        length=30,
        fill='█',
        zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def create_handlers(bot):

    def notify_progress(secs_left, chat_id, message_id, total_seconds):
        progress_bar = render_progressbar(
            total=total_seconds,
            iteration=total_seconds - secs_left,
            length=20
        )
        message = f"Осталось: {secs_left}сек\n{progress_bar}"
        bot.update_message(chat_id, message_id, message)

    def choose(chat_id, message_id):
        bot.send_message(chat_id, "Время вышло!")

    def wait(chat_id, text):
        seconds = pytimeparse.parse(text)
        if seconds:
            message_id = bot.send_message(
                chat_id,
                f"Таймер на: {text} запущен"
            )
            bot.create_countdown(
                seconds,
                notify_progress,
                chat_id=chat_id,
                message_id=message_id,
                total_seconds=seconds
            )
            bot.create_timer(
                seconds,
                choose,
                chat_id=chat_id,
                message_id=message_id
            )
    return wait


def main():
    load_dotenv()
    tg_token = os.getenv("TG_TOKEN")
    bot = ptbot.Bot(tg_token)
    wait_handler = create_handlers(bot)
    bot.reply_on_message(wait_handler)
    bot.run_bot()


if __name__ == '__main__':
    main()
