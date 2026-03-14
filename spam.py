import os
import asyncio
import time
import sys
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError
from colorama import Fore, init, Style

init(autoreset=True)

# ==================== CONFIG ====================
API_ID = 12345                # Твой API ID
API_HASH = "your_api_hash"    # Твой API HASH

BOT_TOKENS = [
    ".",
    ".",
    ".",
    ".",
]

MESSAGE = "💥"                 
BURST_DELAY = 0.05            
# =================================================

# ========== ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ==========
clients = []
nuke_active = False
target_group = None
total_messages = 0

# ========== ФУНКЦИИ АНИМАЦИИ ==========
def clear_screen():
    """Очистка экрана"""
    os.system('clear' if os.name == 'posix' else 'cls')

def loading_animation(text="ЗАГРУЗКА", duration=1.5):
    """Анимация загрузки"""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        print(Fore.YELLOW + f"\r{text} {frames[i % len(frames)]}", end="", flush=True)
        time.sleep(0.1)
        i += 1
    print("\r" + " " * 30 + "\r", end="")

def bomb_animation():
    """Анимация бомбы"""
    for _ in range(2):
        print(Fore.RED + "\r💣", end="", flush=True)
        time.sleep(0.2)
        print(Fore.RED + "\r 💣", end="", flush=True)
        time.sleep(0.2)
        print(Fore.RED + "\r  💣", end="", flush=True)
        time.sleep(0.2)
    print(Fore.RED + Style.BRIGHT + "\r💥 NUKE LAUNCHED! 💥")

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
║         NUKE BOTNET v3.0             ║
║         TELEPHON + MENU              ║
║            by @DADILK                ║
╚══════════════════════════════════════╝
""" + Fore.RESET

# ========== ФУНКЦИЯ ПОКАЗА МЕНЮ ==========
def show_menu():
    clear_screen()
    print(BANNER)
    print(Fore.CYAN + "\n📋 ГЛАВНОЕ МЕНЮ:\n")
    print(Fore.WHITE + "1. 🚀 ЗАПУСТИТЬ БОТНЕТ (начать прослушку)")
    print("2. ⚙️ НАСТРОЙКИ (изменить API/токены)")
    print("3. 📊 СТАТУС (проверить ботов)")
    print("4. 🧹 ОЧИСТИТЬ ЭКРАН")
    print("5. 📖 ИНСТРУКЦИЯ")
    print("0. 🚪 ВЫХОД\n")

# ========== ФУНКЦИЯ НАСТРОЕК ==========
def edit_config():
    global API_ID, API_HASH, BOT_TOKENS, MESSAGE, BURST_DELAY
    
    clear_screen()
    print(BANNER)
    print(Fore.YELLOW + "⚙️ НАСТРОЙКИ:\n")
    
    print(f"Текущий API ID: {API_ID}")
    new_api = input("Новый API ID (Enter - оставить): ").strip()
    if new_api:
        API_ID = int(new_api)
    
    print(f"\nТекущий API HASH: {API_HASH[:5]}...{API_HASH[-5:] if len(API_HASH) > 10 else ''}")
    new_hash = input("Новый API HASH (Enter - оставить): ").strip()
    if new_hash:
        API_HASH = new_hash
    
    print(f"\nТекущее сообщение: {MESSAGE}")
    new_msg = input("Новое сообщение (Enter - оставить): ").strip()
    if new_msg:
        MESSAGE = new_msg
    
    print(f"\nТекущая задержка: {BURST_DELAY} сек")
    try:
        new_delay = input("Новая задержка (Enter - оставить): ").strip()
        if new_delay:
            BURST_DELAY = float(new_delay)
    except:
        print(Fore.RED + "Ошибка! Задержка не изменена")
    
    print(f"\n🤖 Токенов ботов: {len(BOT_TOKENS)}")
    print("1. Добавить токен")
    print("2. Очистить все токены")
    print("3. Показать токены")
    print("0. Назад")
    
    choice = input("\nВыбери: ").strip()
    if choice == "1":
        new_token = input("Введи новый токен: ").strip()
        if new_token:
            BOT_TOKENS.append(new_token)
            print(Fore.GREEN + f"✅ Токен добавлен! Всего: {len(BOT_TOKENS)}")
    elif choice == "2":
        BOT_TOKENS = []
        print(Fore.GREEN + "✅ Все токены удалены")
    elif choice == "3":
        print(Fore.CYAN + "\nТокены:")
        for i, token in enumerate(BOT_TOKENS):
            print(f"{i+1}. {token[:10]}...{token[-5:] if len(token) > 15 else token}")
    
    input(Fore.CYAN + "\nНажми Enter, чтобы вернуться...")

# ========== ФУНКЦИЯ СТАТУСА ==========
def show_status():
    clear_screen()
    print(BANNER)
    print(Fore.MAGENTA + "📊 СТАТУС БОТНЕТА:\n")
    print(f"API ID: {API_ID}")
    print(f"API HASH: {API_HASH[:5]}...{API_HASH[-5:] if len(API_HASH) > 10 else ''}")
    print(f"Количество ботов: {len(BOT_TOKENS)}")
    print(f"Активных сессий: {len(clients)}")
    print(f"Сообщение: {MESSAGE}")
    print(f"Задержка: {BURST_DELAY} сек")
    print(f"Атака активна: {'ДА' if nuke_active else 'НЕТ'}")
    print(f"Всего отправлено: {total_messages}")
    
    if clients:
        print(Fore.GREEN + "\n✅ Боты в сети!")
    else:
        print(Fore.YELLOW + "\n⚠️ Боты не запущены. Запусти через меню (пункт 1)")
    
    input(Fore.CYAN + "\nНажми Enter, чтобы вернуться...")

# ========== ФУНКЦИЯ ИНСТРУКЦИИ ==========
def show_help():
    clear_screen()
    print(BANNER)
    print(Fore.BLUE + "📖 ИНСТРУКЦИЯ:\n")
    print("1️⃣ ПОЛУЧЕНИЕ API:")
    print("   • Зайди на https://my.telegram.org/apps")
    print("   • Войди в аккаунт")
    print("   • Создай приложение")
    print("   • Скопируй API ID и API HASH\n")
    print("2️⃣ ПОЛУЧЕНИЕ ТОКЕНОВ БОТОВ:")
    print("   • Найди @BotFather в Telegram")
    print("   • Отправь /newbot")
    print("   • Скопируй токен")
    print("   • Повтори для нужного количества ботов\n")
    print("3️⃣ ЗАПУСК:")
    print("   • Настрой API и токены в меню (пункт 2)")
    print("   • Запусти ботнет (пункт 1)")
    print("   • Добавь ботов в группы")
    print("   • В группе напиши /nuke для атаки")
    print("   • /stop для остановки\n")
    print("4️⃣ КОМАНДЫ В ГРУППЕ:")
    print("   • /nuke - начать ядерную атаку 💣")
    print("   • /stop - остановить атаку 🛑")
    print("   • /status - статус бота в группе")
    input(Fore.CYAN + "\nНажми Enter, чтобы вернуться...")

# ========== ФУНКЦИЯ ЗАПУСКА БОТОВ ==========
async def setup_bots():
    global clients
    clients = []
    
    clear_screen()
    print(BANNER)
    print(Fore.YELLOW + "\n🤖 ЗАПУСК БОТОВ...\n")
    
    for i, token in enumerate(BOT_TOKENS):
        try:
            if not token or token == ".":
                continue
                
            client = TelegramClient(f'session_{i}', API_ID, API_HASH)
            await client.start(bot_token=token)
            me = await client.get_me()
            print(Fore.GREEN + f"[✓] Бот {i+1}: @{me.username}")
            clients.append(client)
            loading_animation(f"Загрузка бота {i+1}", 0.3)
        except Exception as e:
            print(Fore.RED + f"[✗] Бот {i+1} ошибка: {e}")
    
    if clients:
        print(Fore.MAGENTA + f"\n✅ ГОТОВО БОТОВ: {len(clients)}")
        
        for client in clients:
            client.add_event_handler(on_add)
            client.add_event_handler(nuke_cmd)
            client.add_event_handler(stop_cmd)
            client.add_event_handler(status_cmd)
        
        print(Fore.CYAN + "\n🔥 БОТНЕТ АКТИВЕН 🔥")
        print("📱 Добавь ботов в группы")
        print("💣 Введи /nuke в группе для атаки")
        print("🛑 /stop для остановки")
        print(Fore.RED + "⛔ Нажми Ctrl+C для возврата в меню\n")
        
        await asyncio.gather(*[client.run_until_disconnected() for client in clients])
    else:
        print(Fore.RED + "❌ Нет активных ботов!")
        input(Fore.CYAN + "\nНажми Enter, чтобы вернуться в меню...")

# ========== ФУНКЦИЯ СПАМА ==========
async def spam_group(chat_id):
    global nuke_active, total_messages
    
    while nuke_active:
        tasks = []
        for client in clients:
            try:
                tasks.append(client.send_message(chat_id, MESSAGE))
            except:
                pass
        
        if tasks:
            try:
                results = await asyncio.gather(*tasks, return_exceptions=True)
                sent = sum(1 for r in results if not isinstance(r, Exception))
                total_messages += sent
                print(Fore.RED + f"\r💥 БОМБАРДИРОВКА: {total_messages} | Ботов: {sent}", end="", flush=True)
            except FloodWaitError as e:
                print(Fore.YELLOW + f"\n⏳ Флуд контроль: ждём {e.seconds}с")
                await asyncio.sleep(e.seconds)
            except Exception:
                pass
        
        await asyncio.sleep(BURST_DELAY)

# ========== ОБРАБОТЧИКИ СОБЫТИЙ ==========
@events.register(events.ChatAction)
async def on_add(event):
    if event.user_added and event.user_id == (await event.client.get_me()).id:
        chat = await event.get_chat()
        print(Fore.GREEN + f"\n[+] Бот добавлен в {chat.title}")
        await event.client.send_message(chat.id, 
            "🔥 **NUKE BOTNET АКТИВИРОВАН** 🔥\n\n"
            "💣 /nuke - начать ядерную атаку\n"
            "🛑 /stop - остановить атаку\n"
            "📊 /status - статус бота")

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
    
    await event.reply(f"💣 **NUKE STARTED** 💣\n"
                     f"📢 Группа: {chat.title}\n"
                     f"🤖 Ботов: {len(clients)}\n"
                     f"⚡ Скорость: {1/BURST_DELAY:.0f} сообщений/сек\n"
                     f"💬 Сообщение: {MESSAGE}")
    
    print(Fore.RED + Style.BRIGHT + f"\n💥 ЯДЕРНАЯ АТАКА на {chat.title} начата!")
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

@events.register(events.NewMessage(pattern='/status'))
async def status_cmd(event):
    me = await event.client.get_me()
    await event.reply(f"📊 **Статус бота**\n"
                     f"🤖 Имя: @{me.username}\n"
                     f"🆔 ID: {me.id}\n"
                     f"🔥 Атака: {'АКТИВНА' if nuke_active else 'ОЖИДАНИЕ'}\n"
                     f"📨 Отправлено всего: {total_messages}")

# ========== ГЛАВНАЯ ФУНКЦИЯ ==========
async def main():
    while True:
        show_menu()
        choice = input(Fore.CYAN + "👉 Выбери пункт: ").strip()
        
        if choice == "1":
            if not BOT_TOKENS or all(t == "." for t in BOT_TOKENS):
                print(Fore.RED + "❌ Нет токенов ботов! Сначала настрой (пункт 2)")
                await asyncio.sleep(2)
                continue
            await setup_bots()
        
        elif choice == "2":
            edit_config()
        
        elif choice == "3":
            show_status()
        
        elif choice == "4":
            clear_screen()
            print(Fore.GREEN + "✅ Экран очищен!")
            await asyncio.sleep(1)
        
        elif choice == "5":
            show_help()
        
        elif choice == "0":
            clear_screen()
            bomb_animation()
            print(Fore.RED + "\n👋 Выход... Пока!")
            break
        
        else:
            print(Fore.RED + "❌ Неверный выбор!")
            await asyncio.sleep(1)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n⛔ ОСТАНОВКА...")
        loop = asyncio.get_event_loop()
        for client in clients:
            loop.run_until_complete(client.disconnect())
        print(Fore.GREEN + "✅ Боты отключены")
