import logging
from .pt import ParallelTransferrer
from .configs import session_name, api_id, api_hash, public_url
from .utility import pack_id, get_file_name
from telethon import TelegramClient, events
log = logging.getLogger(__name__)

client = TelegramClient(session_name, api_id, api_hash)
transfer = ParallelTransferrer(client)
