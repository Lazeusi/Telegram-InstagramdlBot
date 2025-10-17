from .register import RegisterMiddleware
from .force_join import ForceJoinMiddleware


from src.logger import get_logger

log = get_logger()


def setup_middlewares(dp):
    try:
        dp.message.middleware(RegisterMiddleware())
        dp.message.middleware(ForceJoinMiddleware())
        
    except Exception as e:
        log.error(f"We got an error: {e}")