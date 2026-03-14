import asyncio
from pyrogram import Client
from colorama import Fore, init

init(autoreset=True)

print(Fore.GREEN + r"""
╔══════════════════════════════════╗
║        BOT SPAMER CLAN v2.0      ║
║         by @DADILK (PREMIUM)      ║
╚══════════════════════════════════╝
""")

api_id = int(input(Fore.YELLOW + "Введите API ID (my.telegram.org): "))
api_hash = input(Fore.YELLOW + "Введите API HASH: ")
bot_token = input(Fore.YELLOW + "Введите токен бота (от @BotFather): ")

group_username = input(Fore.YELLOW + "Username группы (например @chat): ")
message = input(Fore.YELLOW + "Введите текст для спама: ")
count = int(input(Fore.YELLOW + "Количество сообщений: "))
delay = float(input(Fore.YELLOW + "Задержка между сообщениями (сек): "))

async def main():
    app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
    await app.start()
    try:
        group = await app.get_chat(group_username)
        for i in range(count):
            await app.send_message(group.id, f"{message} [#{i+1}]")
            print(Fore.GREEN + f"[✓] Сообщение {i+1} отправлено")
            await asyncio.sleep(delay)
    except Exception as e:
        print(Fore.RED + f"[!] Ошибка: {e}")
    finally:
        await app.stop()

asyncio.run(main())
