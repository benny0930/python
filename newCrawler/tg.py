import asyncio
from telethon import TelegramClient, types

api_id   = 21259078
api_hash = "75a8bcba05507643bb7cda9961ad3aa3"
chat_id  = 2424176843

async def show_all_name():
    client = TelegramClient("my_session", api_id, api_hash)
    await client.start()

    me = await client.get_me()
    chat_entity = None
    print("------dialog.name------")
    async for dialog in client.iter_dialogs():
        print(dialog.name)
    print("-----------------------")
    await client.disconnect()
    
async def del_my_messages(del_name):
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
        if len(batch) > 0:
            print('刪除訊息')
            await client.delete_messages(chat_entity, batch, revoke=True)
            batch.clear()
            await asyncio.sleep(0.5)

    if batch:
        await client.delete_messages(chat_entity, batch, revoke=True)

    print("完成刪除")
    await client.disconnect()



chat_names = [
    "T-E 新增vpn白名單群",
    "super ks",
    "E_Login_Game_Backend",
    "BRIT",
    "特選福利群",
    "极搜🔍资源搜索@JISOU",
    "SuperKs 閒聊區",
    "T-E娛樂城查詢群",
    "UP-PM&RD同步群",
    "佰樂透客戶串接",
    "極機密",
    "9J 滿冠彩票",
    "Binary",
    "大佬們",
    "Feed Reader Bot",
    "前端小群",
    "super ks 頻道測試",
    "PTT GIF",
    "測試刪除",
    "UP-娛樂城 後端技術",
    "test",
    "（上版用）Super Backend R&D",
    "強哥密技小天地",
    "PTT 好康",
    "客服問題怎麼搞-交接",
    "PTT Beauty",
    "PTT 好康",
    "新團隊🌤新氣象",
    "UP-娛樂城 客服 交流群",    
    #"特選福利群",
]


if __name__ == "__main__":
    # asyncio.run(main())
    # asyncio.run(del_my_messages("SuperKs 閒聊區"))
    asyncio.run(show_all_name())
    for name in chat_names:
        print(f"-----------")
        print(f"開始：{name}")
        asyncio.run(del_my_messages(name))

