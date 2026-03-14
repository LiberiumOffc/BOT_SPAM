import asyncio
import time
import sys
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError
from colorama import Fore, init, Style

init(autoreset=True)

# ==================== CONFIG ====================
API_ID = 34353251                # Твой API ID
API_HASH = "ba0b478f0713dae515ee6feec3e18998"    # Твой API HASH

BOT_TOKENS = [
    ".",
    ".",
    ".",
    ".",
]

MESSAGE = "💥"                 
BURST_DELAY = 0.05            
# =================================================

# ========== АНИМАЦИЯ ==========
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def loading_animation(text="ЗАГРУЗКА", duration=1.5):
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        print(Fore.YELLOW + f"\r{text} {frames[i % len(frames)]}", end="", flush=True)
        time.sleep(0.1)
        i += 1
    print("\r" + " " * 30 + "\r", end="")

def bomb_animation():
    for _ in range(2):
        print(Fore.RED + "\r💣", end="", flush=True)
        time.sleep(0.2)
        print(Fore.RED + "\r 💣", end="", flush=True)
        time.sleep(0.2)
        print(Fore.RED + "\r  💣", end="", flush=True)
        time.sleep(0.2)
    print(Fore.RED + Style.BRIGHT + "\r💥 NUKE LAUNCHED! 💥")

def nuke_count_animation(count, total):
    bar_length = 30
    filled = int(bar_length * count / total)
    bar = "█" * filled + "░" * (bar_length - filled)
    print(Fore.GREEN + f"\r💣 [{bar}] {count}/{total}", end="", flush=True)

# ========== БАННЕР ==========
BANNER = Fore.RED + Style.BRIGHT + """
██████╗░░█████╗░███╗░░░███╗██████╗░
██╔══██╗██╔══██╗████╗░████║██╔══██╗
██████╦╝██║░░██║██╔████╔██║██████╦╝
██╔══██╗██║░░██║██║╚██╔╝██║██╔══██╗
██████╦╝╚█████╔╝██║░╚═╝░██║██████╦╝
╚═════╝░░╚════╝░╚═╝░░░░░╚═╝╚═════╝░
""" + Fore.CYAN + """
╔══════════════════════════════════════╗
║         NUKE BOTNET v2.0             ║
║         TELEPHON EDITION 🔥          ║
║            by @DADILK                ║
╚══════════════════════════════════════╝
""" + Fore.RESET

# ========== ОСНОВНОЙ КОД ==========
clients = []
nuke_active = False
target_group = None
total_messages = 0

async def setup_bots():
    print(BANNER)
    print(Fore.YELLOW + "\n🤖 ЗАПУСК БОТОВ...\n")
    
    for i, token in enumerate(BOT_TOKENS):
        try:
            client = TelegramClient(f'session_{i}', API_ID, API_HASH)
            await client.start(bot_token=token)
            me = await client.get_me()
            print(Fore.GREEN + f"[✓] Бот {i+1}: @{me.username}")
            clients.append(client)
            loading_animation(f"Загрузка бота {i+1}", 0.3)
        except Exception as e:
            print(Fore.RED + f"[✗] Бот {i+1} ошибка: {e}")
    
    print(Fore.MAGENTA + f"\n✅ ГОТОВО БОТОВ: {len(clients)}/{len(BOT_TOKENS)}")
    return clients

async def spam_group(chat_id):
    global nuke_active, total_messages
    message_count = 0
    
    while nuke_active:
        tasks = []
        for client in clients:
            try:
                tasks.append(client.send_message(chat_id, MESSAGE))
            except:
                pass
        
        if tasks:
            try:
                await asyncio.gather(*tasks)
                message_count += len(tasks)
                total_messages += len(tasks)
                print(Fore.RED + f"\r💥 БОМБАРДИРОВКА: {total_messages} сообщений | Скорость: {len(tasks)*20}/сек", end="", flush=True)
            except FloodWaitError as e:
                print(Fore.YELLOW + f"\n⏳ Флуд контроль: ждём {e.seconds}с")
                await asyncio.sleep(e.seconds)
            except Exception as e:
                pass
        
        await asyncio.sleep(BURST_DELAY)

@events.register(events.ChatAction)
async def on_add(event):
    if event.user_added and event.user_id == (await event.client.get_me()).id:
        chat = await event.get_chat()
        print(Fore.GREEN + f"\n[+] Бот добавлен в {chat.title}")
        bomb_animation()
        await event.client.send_message(chat.id, "🔥 **NUKE BOT ACTIVATED**\n💣 /nuke - начать атаку\n🛑 /stop - остановить")

@events.register(events.NewMessage(pattern='/nuke'))
async def nuke_cmd(event):
    global nuke_active, target_group, total_messages
    if nuke_active:
        await event.reply("⚠️ Атака уже идёт!")
        return
    
    chat = await event.get_chat()
    target_group = chat.id
    nuke_active = True
    total_messages = 0
    
    bomb_animation()
    await event.reply(f"💣 **NUKE STARTED**\n"
                     f"📢 Группа: {chat.title}\n"
                     f"🤖 Ботов: {len(clients)}\n"
                     f"⚡ Задержка: {BURST_DELAY}с\n"
                     f"💬 Сообщение: {MESSAGE}")
    
    print(Fore.RED + Style.BRIGHT + f"\n💥 АТАКА НА {chat.title} начата!")
    await spam_group(chat.id)

@events.register(events.NewMessage(pattern='/stop'))
async def stop_cmd(event):
    global nuke_active, total_messages
    if nuke_active:
        nuke_active = False
        await event.reply(f"🛑 **NUKE STOPPED**\n📊 Отправлено: {total_messages} сообщений")
        print(Fore.YELLOW + f"\n⛔ Атака остановлена. Всего сообщений: {total_messages}")
    else:
        await event.reply("❌ Нет активной атаки")

async def main():
    # Загрузка API из файла, если есть
    global API_ID, API_HASH, BOT_TOKENS
    
    # Проверка настройки
    if API_ID == 12345 or API_HASH == "your_api_hash":
        print(Fore.RED + "⚠️ Сначала настрой API_ID и API_HASH в файле!")
        print(Fore.YELLOW + "Получи их на https://my.telegram.org/apps")
        return
    
    await setup_bots()
    if not clients:
        print(Fore.RED + "❌ Нет активных ботов!")
        return
    
    for client in clients:
        client.add_event_handler(on_add)
        client.add_event_handler(nuke_cmd)
        client.add_event_handler(stop_cmd)
    
    print(Fore.CYAN + Style.BRIGHT + "\n" + "="*50)
    print("🔥 БОТНЕТ АКТИВЕН 🔥")
    print("="*50)
    print("📱 Добавь ботов в группы")
    print("💣 Введи /nuke в группе для атаки")
    print("🛑 /stop для остановки")
    print("="*50 + "\n")
    
    await asyncio.gather(*[client.run_until_disconnected() for client in clients])

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n⛔ ОСТАНОВКА...")
        loop = asyncio.get_event_loop()
        for client in clients:
            loop.run_until_complete(client.disconnect())
        print(Fore.GREEN + "✅ Боты отключены")
