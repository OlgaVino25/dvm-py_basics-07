import os
from dotenv import load_dotenv
import pytimeparse
import ptbot
import logging

logger = logging.getLogger(__name__)


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


class TimerCallbacks:
    def __init__(self, bot, total_seconds=None, chat_id=None, message_id=None):
        self.bot = bot
        self.total_seconds = total_seconds
        self.chat_id = chat_id
        self.message_id = message_id

    def notify_progress(self, secs_left):
        progress_bar = render_progressbar(
            total=self.total_seconds,
            iteration=self.total_seconds - secs_left,
            length=20
        )
        message = f"Осталось: {secs_left}сек\n{progress_bar}"
        self.bot.update_message(self.chat_id, self.message_id, message)

    def choose(self):
        self.bot.send_message(self.chat_id, "Время вышло!")


def wait(bot, chat_id, text):
    seconds = pytimeparse.parse(text)
    message_id = bot.send_message(chat_id, f"Таймер на: {text} запущен")
    callbacks = TimerCallbacks(bot, seconds, chat_id, message_id)
    bot.create_countdown(seconds, callbacks.notify_progress)
    bot.create_timer(seconds, callbacks.choose)


def main():
    load_dotenv()
    tg_token = os.getenv("TG_TOKEN")

    bot = ptbot.Bot(tg_token)
    bot.reply_on_message(lambda chat_id, text: wait(bot, chat_id, text))
    bot.run_bot()


if __name__ == '__main__':
    main()
