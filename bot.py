import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers.user_handlers import user_router
from handlers.other_handlers import other_router
from config.config_data import Config, load_config
from database.requests import async_main, async_session
from middlewares.db import DataBaseSession


logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(filename)s:%(lineno)d #%(levelname)-8s '
                        '[%(asctime)s] - %(name)s - %(message)s')
    logger.info('Starting bot...')

    await async_main()

    config: Config = load_config('.env')

    bot = Bot(config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher()

    dp.include_router(user_router)
    dp.include_router(other_router)

    dp.update.middleware(DataBaseSession(session_pool=async_session))

    await bot.delete_webhook()
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')