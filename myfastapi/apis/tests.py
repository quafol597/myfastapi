import asyncio
import random
from fastapi import Request
from common.router import TimedRoute
from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse
import time
from configs import settings

router = APIRouter(route_class=TimedRoute)


@router.get("/sse_stream", description="测试 sse 请求.")
async def sse_stream(request: Request):
    def new_messages():
        # Add logic here to check for new messages
        if random.randint(0, 9) > 6:
            return True
        else:
            return False

    async def event_generator():
        while True:
            # If client closes connection, stop sending events
            if await request.is_disconnected():
                break

            # Checks for new messages and return them to client if any
            if new_messages():
                yield {
                    "event": "new_message",
                    "id": "message_id",
                    "retry": settings.SSE_RETRY_TIMEOUT,
                    "data": f"message_content, time:{int(time.time())}",
                }

            await asyncio.sleep(settings.SSE_LOOP_DELAY)

    return EventSourceResponse(event_generator())
