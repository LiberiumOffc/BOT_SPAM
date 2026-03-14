import os
import asyncio
import time
import json
import random
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError
from colorama import Fore, init, Style

init(autoreset=True)

# ========== ФАЙЛ КОНФИГУРАЦИИ ==========
CONFIG_FILE = "bomb_config.json"

# ========== ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ==========
clients = []
bomb_active = False
target_group = None
total_messages = 0
spam_mode = "text"
image_urls = []

# ========== ЗАГРУЗКА/СОХРАНЕНИЕ КОНФИГА ==========
def load_config():
    global API_ID, API_HASH, BOT_TOKENS, MESSAGE, BURST_DELAY, spam_mode, image_urls
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            API_ID = config.get('api_id', 12345)
            API_HASH = config.get('api_hash', 'your_api_hash')
            BOT_TOKENS = config.get('bot_tokens', [])
            MESSAGE = config.get('message', '💥')
            BURST_DELAY = config.get('burst_delay', 0.05)
            spam_mode = config.get('spam_mode', 'text')
            image_urls = config.get('image_urls', [])
            print(Fore.GREEN + f"✅ Конфиг загружен: {len(BOT_TOKENS)} ботов")
            return True
    except:
        API_ID = 12345
        API_HASH = "your_api_hash"
        BOT_TOKENS = []
        MESSAGE = "💥"
        BURST_DELAY = 0.05
        spam_mode = "text"
        image_urls = []
        return False

def save_config():
    config = {
        'api_id': API_ID,
        'api_hash': API_HASH,
        'bot_tokens': BOT_TOKENS,
        'message': MESSAGE,
        'burst_delay': BURST_DELAY,
        'spam_mode': spam_mode,
        'image_urls': image_urls
    }
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)
    print(Fore.GREEN + "✅ Конфиг сохранён")

# ========== АНИМАЦИЯ ==========
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def bomb_animation():
    print(Fore.RED + "\r💣", end="", flush=True)
    time.sleep(0.2)
    print(Fore.RED + "\r 💣", end="", flush=True)
    time.sleep(0.2)
    print(Fore.RED + "\r  💣", end="", flush=True)
    time.sleep(0.2)
    print(Fore.RED + Style.BRIGHT + "\r💥 BOMB LAUNCHED! 💥")

# ========== БАННЕР ==========
BANNER = Fore.RED + """
██████╗░░█████╗░███╗░░░███╗██████╗░
██╔══██╗██╔══██╗████╗░████║██╔══██╗
██████╦╝██║░░██║██╔████╔██║██████╦╝
██╔══██╗██║░░██║██║╚██╔╝██║██╔══██╗
██████╦╝╚█████╔╝██║░╚═╝░██║██████╦╝
╚═════╝░░╚════╝░╚═╝░░░░░╚═╝╚═════╝░
""" + Fore.CYAN + """
╔══════════════════════════════════════╗
║         BOMB BOTNET v5.2             ║
║         **РАБОЧАЯ ВЕРСИЯ**           ║
║            by @DADILK                ║
╚══════════════════════════════════════╝
""" + Fore.RESET

def print_banner():
    clear_screen()
    print(BANNER)

# ========== ОБРАБОТЧИКИ СОБЫТИЙ ==========
# ВАЖНО: Обработчики должны быть определены ДО того, как добавляются в клиента

async def on_add(event):
    """Когда бота добавляют в группу"""
    if event.user_added and event.user_id == (await event.client.get_me()).id:
        chat = await event.get_chat()
        print(Fore.GREEN + f"\n[+] Бот добавлен в {chat.title}")
        await event.client.send_message(chat.id, 
            "🔥 **BOMB BOTNET АКТИВИРОВАН** 🔥\n\n"
            "💣 /bomb - начать атаку\n"
            "🛑 /stop - остановить\n"
            "📊 /status - статус")

async def bomb_cmd(event):
    """Команда /bomb - начало атаки"""
    global bomb_active, target_group, total_messages
    
    if bomb_active:
        await event.reply("⚠️ Бомбардировка уже идёт!")
        return
    
    chat = await event.get_chat()
    target_group = chat.id
    bomb_active = True
    total_messages = 0
    
    print(Fore.RED + Style.BRIGHT + f"\n💥 БОМБАРДИРОВКА {chat.title} начата!")
    await event.reply(f"💣 **BOMB STARTED** 💣\n"
                     f"📢 Группа: {chat.title}\n"
                     f"🤖 Ботов: {len(clients)}\n"
                     f"⏱️ КД: {BURST_DELAY}с")
    
    # Запускаем спам
    asyncio.create_task(spam_group(chat.id))

async def stop_cmd(event):
    """Команда /stop - остановка атаки"""
    global bomb_active, total_messages
    
    if bomb_active:
        bomb_active = False
        await event.reply(f"🛑 **BOMB STOPPED**\n📊 Отправлено: {total_messages}")
        print(Fore.YELLOW + f"\n⛔ Атака остановлена. Всего: {total_messages}")
    else:
        await event.reply("❌ Нет активной атаки")

async def status_cmd(event):
    """Команда /status - статус бота"""
    me = await event.client.get_me()
    mode_text = "🖼️ КАРТИНКИ" if spam_mode == "image" else "📝 ТЕКСТ"
    await event.reply(f"📊 **Статус**\n"
                     f"🤖 @{me.username}\n"
                     f"🔥 Режим: {mode_text}\n"
                     f"⏱️ КД: {BURST_DELAY}с\n"
                     f"💥 Атака: {'АКТИВНА' if bomb_active else 'ОЖИДАНИЕ'}\n"
                     f"📨 Отправлено: {total_messages}")

# ========== СПАМ ==========
async def spam_group(chat_id):
    global bomb_active, total_messages
    
    while bomb_active:
        tasks = []
        for client in clients:
            try:
                if spam_mode == "text":
                    tasks.append(client.send_message(chat_id, MESSAGE))
                else:
                    if image_urls:
                        url = random.choice(image_urls)
                        tasks.append(client.send_file(chat_id, url))
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
            except:
                pass
        
        await asyncio.sleep(BURST_DELAY)

# ========== ЗАПУСК БОТОВ ==========
async def setup_bots():
    global clients
    clients = []
    
    print_banner()
    print(Fore.YELLOW + f"\n🤖 ЗАПУСК {len(BOT_TOKENS)} БОТОВ...\n")
    
    if not BOT_TOKENS:
        print(Fore.RED + "❌ Нет токенов!")
        input(Fore.CYAN + "\nНажми Enter...")
        return
    
    for i, token in enumerate(BOT_TOKENS):
        try:
            if not token or token == "":
                continue
            
            # Создаём клиента
            client = TelegramClient(f'session_bot_{i}', API_ID, API_HASH)
            await client.start(bot_token=token)
            me = await client.get_me()
            
            # Добавляем обработчики КАЖДОМУ клиенту
            client.add_event_handler(on_add, events.ChatAction)
            client.add_event_handler(bomb_cmd, events.NewMessage(pattern='/bomb'))
            client.add_event_handler(stop_cmd, events.NewMessage(pattern='/stop'))
            client.add_event_handler(status_cmd, events.NewMessage(pattern='/status'))
            
            clients.append(client)
            print(Fore.GREEN + f"[✓] Бот {i+1}: @{me.username}")
            
        except Exception as e:
            print(Fore.RED + f"[✗] Бот {i+1} ошибка: {e}")
    
    if clients:
        print(Fore.MAGENTA + f"\n✅ ЗАПУЩЕНО БОТОВ: {len(clients)}/{len(BOT_TOKENS)}")
        print(Fore.CYAN + "\n🔥 БОТНЕТ АКТИВЕН 🔥")
        print("📱 Добавь ботов в группы")
        print("💣 Введи /bomb в группе для атаки")
        print("🛑 /stop для остановки")
        print(Fore.RED + "⛔ Ctrl+C для возврата в меню\n")
        
        # Держим всех ботов в работе
        await asyncio.gather(*[client.run_until_disconnected() for client in clients])
    else:
        print(Fore.RED + "❌ Не удалось запустить ни одного бота!")
        input(Fore.CYAN + "\nНажми Enter...")

# ========== МЕНЮ ==========
def show_menu():
    print_banner()
    mode_display = "🖼️ КАРТИНКИ" if spam_mode == "image" else "📝 ТЕКСТ"
    print(Fore.CYAN + f"\n📋 ГЛАВНОЕ МЕНЮ (Режим: {mode_display} | КД: {BURST_DELAY}с):\n")
    print(Fore.WHITE + "1. 🚀 ЗАПУСТИТЬ БОТНЕТ")
    print("2. 🤖 ДОБАВИТЬ ТОКЕН БОТА")
    print("3. 👀 ПОСМОТРЕТЬ ТОКЕНЫ")
    print("4. 🗑️ УДАЛИТЬ ТОКЕН")
    print("5. ⚙️ НАСТРОЙКИ API")
    print("6. ✏️ ИЗМЕНИТЬ ТЕКСТ")
    print("7. 🖼️ РЕЖИМ СПАМА")
    print("8. 📸 ДОБАВИТЬ КАРТИНКУ")
    print("9. ⏱️ ИЗМЕНИТЬ КД")
    print("10. 📊 СТАТУС")
    print("11. 🧹 ОЧИСТИТЬ ЭКРАН")
    print("12. 📖 ИНСТРУКЦИЯ")
    print("0. 🚪 ВЫХОД\n")
    print(Fore.YELLOW + f"🤖 Ботов: {len(BOT_TOKENS)} | 📸 Картинок: {len(image_urls)}")

# ========== ФУНКЦИИ МЕНЮ ==========
def add_token():
    print_banner()
    print(Fore.YELLOW + "🤖 ДОБАВЛЕНИЕ ТОКЕНА\n")
    token = input("Введи токен: ").strip()
    if token:
        BOT_TOKENS.append(token)
        save_config()
        print(Fore.GREEN + f"✅ Токен добавлен! Всего: {len(BOT_TOKENS)}")
    input(Fore.CYAN + "\nНажми Enter...")

def show_tokens():
    print_banner()
    print(Fore.CYAN + "👀 ТОКЕНЫ:\n")
    if not BOT_TOKENS:
        print(Fore.YELLOW + "Нет токенов")
    else:
        for i, token in enumerate(BOT_TOKENS):
            shown = token[:10] + "..." + token[-5:] if len(token) > 20 else token
            print(f"{i+1}. {shown}")
    input(Fore.CYAN + "\nНажми Enter...")

def delete_token():
    print_banner()
    print(Fore.YELLOW + "🗑️ УДАЛЕНИЕ ТОКЕНА\n")
    if not BOT_TOKENS:
        print(Fore.YELLOW + "Нет токенов")
        input(Fore.CYAN + "\nНажми Enter...")
        return
    for i, token in enumerate(BOT_TOKENS):
        shown = token[:10] + "..." + token[-5:] if len(token) > 20 else token
        print(f"{i+1}. {shown}")
    try:
        choice = int(input(Fore.RED + "\nНомер токена (0 - отмена): "))
        if 1 <= choice <= len(BOT_TOKENS):
            BOT_TOKENS.pop(choice-1)
            save_config()
            print(Fore.GREEN + f"✅ Токен {choice} удалён")
    except:
        print(Fore.RED + "❌ Ошибка")
    input(Fore.CYAN + "\nНажми Enter...")

def edit_api():
    global API_ID, API_HASH
    print_banner()
    print(Fore.YELLOW + "⚙️ НАСТРОЙКИ API\n")
    new_api = input(f"API ID [{API_ID}]: ").strip()
    if new_api:
        API_ID = int(new_api)
    new_hash = input(f"API HASH [{API_HASH[:5]}...]: ").strip()
    if new_hash:
        API_HASH = new_hash
    save_config()
    input(Fore.CYAN + "\nНажми Enter...")

def edit_message():
    global MESSAGE
    print_banner()
    print(Fore.YELLOW + "✏️ ИЗМЕНИТЬ ТЕКСТ\n")
    new_msg = input(f"Новый текст [{MESSAGE}]: ").strip()
    if new_msg:
        MESSAGE = new_msg
        save_config()
    input(Fore.CYAN + "\nНажми Enter...")

def toggle_spam_mode():
    global spam_mode
    print_banner()
    print(Fore.YELLOW + "🖼️ РЕЖИМ СПАМА\n")
    print(f"Сейчас: {'КАРТИНКИ' if spam_mode == 'image' else 'ТЕКСТ'}")
    print("1. Текст")
    print("2. Картинки")
    choice = input("Выбери: ").strip()
    if choice == "1":
        spam_mode = "text"
        save_config()
    elif choice == "2":
        if image_urls:
            spam_mode = "image"
            save_config()
        else:
            print(Fore.YELLOW + "⚠️ Сначала добавь картинки!")
    input(Fore.CYAN + "\nНажми Enter...")

def add_image_url():
    global image_urls
    print_banner()
    print(Fore.YELLOW + "📸 ДОБАВИТЬ КАРТИНКУ\n")
    url = input("Ссылка на картинку: ").strip()
    if url:
        image_urls.append(url)
        save_config()
        print(Fore.GREEN + f"✅ Добавлено! Всего: {len(image_urls)}")
    input(Fore.CYAN + "\nНажми Enter...")

def edit_delay():
    global BURST_DELAY
    print_banner()
    print(Fore.YELLOW + "⏱️ ИЗМЕНИТЬ КД\n")
    try:
        new_delay = float(input(f"Новая задержка [{BURST_DELAY}]: ").strip())
        if new_delay >= 0:
            BURST_DELAY = new_delay
            save_config()
    except:
        print(Fore.RED + "❌ Ошибка")
    input(Fore.CYAN + "\nНажми Enter...")

def show_status():
    print_banner()
    print(Fore.MAGENTA + "📊 СТАТУС:\n")
    print(f"API ID: {API_ID}")
    print(f"Ботов в конфиге: {len(BOT_TOKENS)}")
    print(f"Активных сессий: {len(clients)}")
    print(f"Режим: {'КАРТИНКИ' if spam_mode == 'image' else 'ТЕКСТ'}")
    print(f"Картинок: {len(image_urls)}")
    print(f"КД: {BURST_DELAY}с")
    print(f"Атака: {'ДА' if bomb_active else 'НЕТ'}")
    print(f"Отправлено: {total_messages}")
    input(Fore.CYAN + "\nНажми Enter...")

def show_help():
    print_banner()
    print(Fore.BLUE + "📖 ИНСТРУКЦИЯ:\n")
    print("1. API ключи: https://my.telegram.org/apps")
    print("2. Токены ботов: @BotFather")
    print("3. Команды в группе:")
    print("   • /bomb - атака")
    print("   • /stop - стоп")
    print("   • /status - статус")
    input(Fore.CYAN + "\nНажми Enter...")

# ========== ГЛАВНАЯ ==========
async def main():
    load_config()
    
    while True:
        show_menu()
        choice = input(Fore.CYAN + "👉 Выбери пункт: ").strip()
        
        if choice == "1":
            await setup_bots()
        elif choice == "2":
            add_token()
        elif choice == "3":
            show_tokens()
        elif choice == "4":
            delete_token()
        elif choice == "5":
            edit_api()
        elif choice == "6":
            edit_message()
        elif choice == "7":
            toggle_spam_mode()
        elif choice == "8":
            add_image_url()
        elif choice == "9":
            edit_delay()
        elif choice == "10":
            show_status()
        elif choice == "11":
            clear_screen()
        elif choice == "12":
            show_help()
        elif choice == "0":
            print(Fore.RED + "\n👋 Пока!")
            break
        else:
            print(Fore.RED + "❌ Неверный выбор!")
            time.sleep(1)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n⛔ ОСТАНОВКА...")
        loop = asyncio.get_event_loop()
        for client in clients:
            loop.run_until_complete(client.disconnect())
        print(Fore.GREEN + "✅ Боты отключены")
