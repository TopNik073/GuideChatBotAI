from aiogram import Router

from .user_handlers import router as user_router

router = Router(name="main_router")

router.include_routers(user_router)
