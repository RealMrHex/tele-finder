import re
import time
from pyrogram import Client
from pyrogram import filters
from pyrogram.errors import FloodWait, BadRequest
import math
import os

api_id   = xxxx
api_hash = 'xxxx'

app = Client('finder_account', api_id, api_hash)

try:
    # noinspection PyUnresolvedReferences
    @app.on_message(filters.text & filters.outgoing)
    async def commands(client, message):
        if message.text.startswith('[join] '):
            link = message.text.replace('[join] ', '')

            x_message = await message.reply_text('Warming engine...')

            try:
                target = await app.join_chat(link)
            except BadRequest:
                target = await app.get_chat(link)

            if target.type == 'supergroup' or target.type == 'group':
                await scan_target(target, x_message)
            else:
                await x_message.edit_text('<b><i>Target is a ' + target.type + '!!</b></i>')
                await target.leave()
        elif message.text == 'ping':
            await message.reply_text('<b><i>Pong!!</b></i>', quote=True)


    async def scan_target(target, message):
        await message.edit_text('<b><i>Joined to ' + target.title + '!!</b></i>')

        members_count = await app.get_chat_members_count(target.id)

        await message.edit_text('<b><i>'
                                'Status: Scanning...\n'
                                'Target: '
                                + target.title
                                + '\n'
                                + 'Members: '
                                + str(members_count)
                                + '</b></i>'
                                )

        loop = math.ceil(members_count / 200)
        await get_members(target, message, loop, members_count)


    async def get_members(target, message, loop, members_count):
        chat_members = []
        rounds = range(loop)
        last_scan_count = 0

        for current_round in rounds:
            offset = current_round * 200
            new_members = await target.get_members(offset=offset)
            chat_members = chat_members + new_members

            if last_scan_count != len(chat_members):
                await message.edit_text('<b><i>'
                                        'Status: Scanning...!\n'
                                        + 'Target: '
                                        + target.title
                                        + '\n'
                                        + 'Members: '
                                        + str(members_count)
                                        + '\n'
                                        + 'Scanned: '
                                        + str(len(chat_members))
                                        + '</b></i>'
                                        )

            last_scan_count = len(chat_members)

            if last_scan_count != len(chat_members):
                await message.edit_text('<b><i>'
                                        'Status: Scan end, Please wait...!\n'
                                        + 'Target: '
                                        + target.title
                                        + '\n'
                                        + 'Members: '
                                        + str(members_count)
                                        + '\n'
                                        + 'Scanned: '
                                        + str(len(chat_members))
                                        + '</b></i>'
                                        )

        await send_result(target, message, chat_members, members_count)


    async def send_result(target, message, chat_members, members_count):
        await message.edit_text('<b><i>'
                                'Status: Finding phone numbers...!\n'
                                + 'Target: '
                                + target.title
                                + '\n'
                                + 'Members: '
                                + str(members_count)
                                + '\n'
                                + 'Scanned: '
                                + str(len(chat_members))
                                + '</b></i>'
                                )
        phones_count = await get_phones(target, message, chat_members)

        await message.edit_text('<b><i>'
                                'Status: Finding usernames...!\n'
                                + 'Target: '
                                + target.title
                                + '\n'
                                + 'Members: '
                                + str(members_count)
                                + '\n'
                                + 'Scanned: '
                                + str(len(chat_members))
                                + '\n'
                                + 'Founded Phones: '
                                + str(phones_count)
                                + '</b></i>'
                                )

        usernames_count = await get_usernames(target, message, chat_members)

        await message.edit_text('<b><i>'
                                'Status: Finding User IDs...!\n'
                                + 'Target: '
                                + target.title
                                + '\n'
                                + 'Members: '
                                + str(members_count)
                                + '\n'
                                + 'Scanned: '
                                + str(len(chat_members))
                                + '\n'
                                + 'Founded Phones: '
                                + str(phones_count)
                                + '\n'
                                + 'Founded Usernames: '
                                + str(usernames_count)
                                + '</b></i>'
                                )

        ids_count = await get_user_ids(target, message, chat_members)

        await message.edit_text('<b><i>'
                                + 'Status: Generate Hex file!\n'
                                + 'Target: '
                                + target.title
                                + '\n'
                                + 'Members: '
                                + str(members_count)
                                + '\n'
                                + 'Scanned: '
                                + str(len(chat_members))
                                + '\n'
                                + 'Founded Phones: '
                                + str(phones_count)
                                + '\n'
                                + 'Founded Usernames: '
                                + str(usernames_count)
                                + '\n'
                                + 'Founded User IDs: '
                                + str(ids_count)
                                + '</b></i>'
                                )

        total_count = await get_total(target, message, chat_members)

        await message.edit_text('<b><i>'
                                + 'Status: Scanning messages...\n'
                                + 'Target: '
                                + target.title
                                + '\n'
                                + 'Members: '
                                + str(members_count)
                                + '\n'
                                + 'Scanned: '
                                + str(len(chat_members))
                                + '\n'
                                + 'Founded Phones: '
                                + str(phones_count)
                                + '\n'
                                + 'Founded Usernames: '
                                + str(usernames_count)
                                + '\n'
                                + 'Founded User IDs: '
                                + str(ids_count)
                                + '\n'
                                + 'Hex : '
                                + str(total_count)
                                + '</b></i>'
                                )

        scanned_messages = 0
        phones = []

        timestamp = time.time()
        next_edit = timestamp + 120

        async for chat_message in app.iter_history(target.id):
            if chat_message.text:
                text = chat_message.text
                text = text.translate(text.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789'))

                matches = re.finditer(r"(\+9809|\+989|989|09|9)([0-9]){9}", text, re.MULTILINE)

                for matchNum, match in enumerate(matches, start=1):
                    phones.append(match.group())

            scanned_messages += 1
            current_time = time.time()

            if current_time >= next_edit:
                await message.edit_text('<b><i>'
                                        + 'Status: Scanning messages...\n'
                                        + 'Target: '
                                        + target.title
                                        + '\n'
                                        + 'Members: '
                                        + str(members_count)
                                        + '\n'
                                        + 'Scanned: '
                                        + str(len(chat_members))
                                        + '\n'
                                        + 'Founded Phones: '
                                        + str(phones_count)
                                        + '\n'
                                        + 'Founded Usernames: '
                                        + str(usernames_count)
                                        + '\n'
                                        + 'Founded User IDs: '
                                        + str(ids_count)
                                        + '\n'
                                        + 'Hex : '
                                        + str(total_count)
                                        + '\n'
                                        + 'Founded M-Phones : '
                                        + str(len(phones))
                                        + '\n'
                                        + 'Scanned Messages : '
                                        + str(scanned_messages)
                                        + '</b></i>'
                                        )
                next_edit = time.time() + 120

        await message.edit_text('<b><i>'
                                + 'Status: Filing M-Phones...\n'
                                + 'Target: '
                                + target.title
                                + '\n'
                                + 'Members: '
                                + str(members_count)
                                + '\n'
                                + 'Scanned: '
                                + str(len(chat_members))
                                + '\n'
                                + 'Founded Phones: '
                                + str(phones_count)
                                + '\n'
                                + 'Founded Usernames: '
                                + str(usernames_count)
                                + '\n'
                                + 'Founded User IDs: '
                                + str(ids_count)
                                + '\n'
                                + 'Hex : '
                                + str(total_count)
                                + '\n'
                                + 'Founded M-Phones : '
                                + str(len(phones))
                                + '\n'
                                + 'Scanned Messages : '
                                + str(scanned_messages)
                                + '</b></i>'
                                )

        await file_phones(target, message, phones)

        await message.edit_text('<b><i>'
                                'Status: Leaving...!\n'
                                + 'Target: '
                                + target.title
                                + '\n'
                                + 'Members: '
                                + str(members_count)
                                + '\n'
                                + 'Scanned: '
                                + str(len(chat_members))
                                + '\n'
                                + 'Founded Phones: '
                                + str(phones_count)
                                + '\n'
                                + 'Founded Usernames: '
                                + str(usernames_count)
                                + '\n'
                                + 'Founded User IDs: '
                                + str(ids_count)
                                + '\n'
                                + 'Hex : '
                                + str(total_count)
                                + '\n'
                                + 'Founded M-Phones : '
                                + str(len(phones))
                                + '\n'
                                + 'Scanned Messages : '
                                + str(scanned_messages)
                                + '</b></i>'
                                )
        await target.leave()

        await message.edit_text('<b><i>'
                                + 'Status: Done!\n'
                                + 'Target: '
                                + target.title
                                + '\n'
                                + 'Members: '
                                + str(members_count)
                                + '\n'
                                + 'Scanned: '
                                + str(len(chat_members))
                                + '\n'
                                + 'Founded Phones: '
                                + str(phones_count)
                                + '\n'
                                + 'Founded Usernames: '
                                + str(usernames_count)
                                + '\n'
                                + 'Founded User IDs: '
                                + str(ids_count)
                                + '\n'
                                + 'Hex : '
                                + str(total_count)
                                + '\n'
                                + 'Founded M-Phones : '
                                + str(len(phones))
                                + '\n'
                                + 'Scanned Messages : '
                                + str(scanned_messages)
                                + '\n'
                                + 'Powered by @Logcats'
                                + '</b></i>'
                                )

        await message.reply_text('<b><i>Scan Done!!</b></i> 🥳🥳', quote=True)

    async def get_phones(target, message, chat_members):
        phones_count = 0

        doc = 'phones' + str(target.id) + '.txt'
        cap = '<b><i>' + target.title + ' Phones!!</b></i> 📱'

        with open(doc, 'w', encoding="utf-8") as f:
            for chat_member in chat_members:
                if chat_member.user.phone_number and chat_member.user.phone_number != '':
                    f.writelines('\n' + str(chat_member.user.phone_number))
                    phones_count += 1

        if phones_count > 0:
            await app.send_document(message.chat.id, document=doc, caption=cap, reply_to_message_id=message.message_id)
            os.remove(doc)

        return phones_count


    async def get_usernames(target, message, chat_members):
        usernames_count = 0

        doc = 'usernames' + str(target.id) + '.txt'
        cap = '<b><i>' + target.title + ' Usernames!!</b></i> 💠'

        with open(doc, 'w', encoding="utf-8") as f:
            for chat_member in chat_members:
                if chat_member.user.username and chat_member.user.username != '':
                    f.writelines('\n' + str(chat_member.user.username))
                    usernames_count += 1

        if usernames_count > 0:
            await app.send_document(message.chat.id, document=doc, caption=cap, reply_to_message_id=message.message_id)
            os.remove(doc)

        return usernames_count


    async def get_user_ids(target, message, chat_members):
        user_ids_count = 0

        doc = 'user_ids' + str(target.id) + '.txt'
        cap = '<b><i>' + target.title + ' User ids!!</b></i> 💎'

        with open(doc, 'w', encoding="utf-8") as f:
            for chat_member in chat_members:
                if chat_member.user.id and chat_member.user.id != '':
                    f.writelines('\n' + str(chat_member.user.id))
                    user_ids_count += 1

        if user_ids_count > 0:
            await app.send_document(message.chat.id, document=doc, caption=cap, reply_to_message_id=message.message_id)
            os.remove(doc)

        return user_ids_count


    async def get_total(target, message, chat_members):
        total_count = 0

        doc = 'hex-format' + str(target.id) + '.txt'
        cap = '<b><i>' + target.title + ' Hex-Format!!</b></i> 👑'

        with open(doc, 'w', encoding="utf-8") as f:
            for chat_member in chat_members:
                line = str(chat_member.user.phone_number) + ':' + str(chat_member.user.username) + ':' + str(
                    chat_member.user.id)
                f.writelines('\n' + line)
                total_count += 1

        await app.send_document(message.chat.id, document=doc, caption=cap, reply_to_message_id=message.message_id)
        os.remove(doc)

        return total_count

    async def file_phones(target, message, phones):
        doc = 'M-Phones' + str(target.id) + '.txt'
        cap = '<b><i>' + target.title + ' M-Phones!!</b></i> ☕️'

        if len(phones) > 0:
            with open(doc, 'w', encoding="utf-8") as f:
                for phone in phones:
                    line = str(phone)
                    f.writelines('\n' + line)

            await app.send_document(message.chat.id, document=doc, caption=cap, reply_to_message_id=message.message_id)
            os.remove(doc)


except FloodWait as e:
    time.sleep(e.x)

app.run()
