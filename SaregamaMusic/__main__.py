import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from SaregamaMusic import LOGGER, app, userbot
from SaregamaMusic.core.call import AMBOTOP
from SaregamaMusic.misc import sudo
from SaregamaMusic.plugins import ALL_MODULES
from SaregamaMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        exit()
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("SaregamaMusic.plugins" + all_module)
    LOGGER("SaregamaMusic.plugins").info("Successfully Imported Modules...")
    await userbot.start()
    await AMBOTOP.start()
    try:
        await AMBOTOP.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("SaregamaMusic").error(
            "Please turn on the videochat of your log group\\channel.\n\nStopping Bot..."
        )
        exit()
    except:
        pass
    await AMBOTOP.decorators()
    LOGGER("SaregamaMusic").info(
        "BsdK Resso Music Start Hoga Be Ab"
    )
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("SaregamaMusic").info("Stopping AMBOTOP Music Bot...")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
