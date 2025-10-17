from .start import router as start_router
from .admin import router as admin_router
from .channel import router as channel_router
from .force_join import router as force_join_router


from src.logger import get_logger

log = get_logger()

def setup_handlers(dp):
    try:
        dp.include_router(start_router)
        dp.include_router(admin_router)
        dp.include_router(channel_router)
        dp.include_router(force_join_router)
        
    except Exception as e:
        log.error(f"We got an error: {e}")
