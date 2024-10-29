import asyncio

async def main() -> None:
    from source.database.database_initialisation import init_database
    await init_database()
    from source.bot import bot, dp  
    from .lifespan import on_shutdown, on_startup
    try:
        await bot.delete_webhook(drop_pending_updates=False)
        dp.startup.register(on_startup)
        dp.shutdown.register(on_shutdown)
        await asyncio.gather(dp.start_polling(bot))
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
