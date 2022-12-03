from telethon.tl.custom import Message
from aiohttp import web
from typing import Dict, cast
from collections import defaultdict
import logging
from .configs import request_limit
from .tele import client, transfer
from .utility import unpack_id, get_file_name, get_requester_ip
routes = web.RouteTableDef()
ongoing_requests: Dict[str, int] = defaultdict(lambda: 0)
log = logging.getLogger(__name__)


@routes.get(r"/")
async def handle_home_request(req: web.Request) -> web.Response:
    return web.Response(text="Hello There!")
  
@routes.get(r"/stream/{id:\d+}")
async def handle_get_request(req: web.Request) -> web.Response:
    return await handle_request(req, head=False)

@routes.head(r"/stream/{id:\d+}")
async def handle_head_request(req: web.Request) -> web.Response:
    return await handle_request(req, head=True)

def increment_counter(ip: str) -> None:
    ongoing_requests[ip] += 1

def decrement_counter(ip: str) -> None:
    ongoing_requests[ip] -= 1

def allow_request(ip: str) -> None:
    return ongoing_requests[ip] < request_limit

async def handle_request(req: web.Request, head: bool = False) -> web.Response:
    file_id = int(req.match_info["id"])
    peer, msg_id = unpack_id(file_id)
    if not peer or not msg_id:
        return web.Response(status=404, text="404: Not Found")

    message = cast(Message, await client.get_messages(entity=peer, ids=msg_id))

    size = message.file.size
    offset = req.http_range.start or 0
    limit = req.http_range.stop or size

    if not head:
        ip = get_requester_ip(req)
        if not allow_request(ip):
            return web.Response(status=429)
        log.info(f"Serving file in {message.id} (chat {message.chat_id}) to {ip}")
        body = transfer.download(message.media, file_size=size, offset=offset, limit=limit)
    else:
        body = None
    return web.Response(status=206 if offset else 200,
                        body=body,
                        headers={
                            "Content-Type": message.file.mime_type,
                            "Content-Range": f"bytes {offset}-{size}/{size}",
                            "Content-Length": str(limit - offset),
                            "Accept-Ranges": "bytes",
                        })









