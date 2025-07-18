import asyncio
from telethon import TelegramClient, types

api_id   = 21259078
api_hash = "75a8bcba05507643bb7cda9961ad3aa3"
chat_id  = 2424176843


def get_chat():
    with TelegramClient('my_account', api_id, api_hash) as client:
        dialogs = client.get_dialogs()      # 同步結果
        for dialog in dialogs:
            entity = dialog.entity
            # print(entity)
            if getattr(entity, 'title', None):
                print(f'群組名稱：{entity.title}')
                # 如果群組有 migrated_to，表示已遷移成超級群組（頻道）
                if getattr(entity, 'migrated_to', None):
                    # migrated_to 是 InputChannel，需要用 channel_id
                    migrated = entity.migrated_to
                    chat_id = migrated.channel_id
                    print(f'已遷移，使用新的頻道ID：100{chat_id}')
                else:
                    chat_id = entity.id
                    print(f'chat_id：{chat_id}')
                print('-' * 40)

async def del_my_messages(del_name):

    # del_name = "88.BRIT"
    # del_name = "super ks"
    # del_name = "T-E 新增vpn白名單群"
    # del_name = "娛樂城部署通知"
    # del_name = "E_Login_Game_Backend"
    # del_name = "T處-娛樂城專用機器人"
    # del_name = "9J 滿冠彩票"
    # del_name = "T處-娛樂城查詢群"
    # del_name = "佰樂透客戶串接"
    # del_name = "大佬們"
    # del_name = "前端小群"
    # del_name = "UP-娛樂城 後端技術"
    # del_name = "（上版用）Super Backend R&D"
    # del_name = "UP-PM&RD同步群"
    # del_name = "客服問題怎麼搞-交接"
    # del_name = "新團隊🌤新氣象"
    # del_name = "UP-娛樂城 客服 交流群"

    client = TelegramClient("my_session", api_id, api_hash)
    await client.start()

    me = await client.get_me()

    # 找出指定聊天的 entity (這裡改成用聊天名稱搜尋示範)
    chat_entity = None
    async for dialog in client.iter_dialogs():
        if dialog.name == del_name:
            print(f'{dialog.name} - ID: {dialog.id}')
            chat_entity = dialog.entity
            break

    if not chat_entity:
        print('找不到指定聊天')
        await client.disconnect()
        return

    batch = []
    async for msg in client.iter_messages(chat_entity, from_user=me):
        batch.append(msg.id)
        if len(batch) == 100:
            print('delete_messages')
            await client.delete_messages(chat_entity, batch, revoke=True)
            batch.clear()
            await asyncio.sleep(0.5)

    if batch:
        await client.delete_messages(chat_entity, batch, revoke=True)

    print("完成刪除")
    await client.disconnect()



chat_names = [
    "88.BRIT",
    "super ks",
    "T-E 新增vpn白名單群",
    "娛樂城部署通知",
    # "E_Login_Game_Backend",
    "T處-娛樂城專用機器人",
    "9J 滿冠彩票",
    "T處-娛樂城查詢群",
    "佰樂透客戶串接",
    "大佬們",
    "前端小群",
    "UP-娛樂城 後端技術",
    "（上版用）Super Backend R&D",
    "UP-PM&RD同步群",
    "客服問題怎麼搞-交接",
    "新團隊🌤新氣象",
    "UP-娛樂城 客服 交流群"
]

async def purge_my_msgs(chat_entity, client, me):
    batch = []
    async for msg in client.iter_messages(chat_entity, from_user=me):
        batch.append(msg.id)
        if len(batch) == 100:
            await client.delete_messages(chat_entity, batch, revoke=True)
            batch.clear()
            await asyncio.sleep(0.5)
    if batch:
        await client.delete_messages(chat_entity, batch, revoke=True)

async def main():
    client = TelegramClient("my_session", api_id, api_hash)
    await client.start()
    me = await client.get_me()

    targets = set(chat_names)
    async for dialog in client.iter_dialogs():
        name = dialog.name or ""
        if name in targets:
            entity = dialog.entity
            # 如果是被遷移的超級群組，改用新 channel 實體
            if getattr(entity, "migrated_to", None):
                entity = types.InputChannel(
                    entity.migrated_to.channel_id,
                    entity.migrated_to.access_hash
                )
            print(f"開始刪除：{name}")
            await purge_my_msgs(entity, client, me)
            print(f"完成：{name}")

    await client.disconnect()

if __name__ == "__main__":
    # asyncio.run(main())
    # asyncio.run(del_my_messages("SuperKs 閒聊區"))
    for name in chat_names:
        asyncio.run(del_my_messages(name))


