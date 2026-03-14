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

# ========== ПЕРЕМЕННЫЕ ==========
clients = []
bomb_active = False
target_group = None
total_messages = 0
spam_mode = "text"
image_urls = []
bots_can_spam = False  # Статус могут ли боты спамить

# ========== ЗАГРУЗКА КОНФИГА ==========
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

# ========== ОЧИСТКА ЭКРАНА ==========
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

# ========== KALI LINUX BACKGROUND ==========
KALI_BG = Fore.GREEN + """
┌─────────────────────────────────────────┐
│  ⚡ KALI LINUX ⚡                        │
│  █▀▀ █▀▀ █░░ █▀▄ █▀▀ █░█ █░░ █▀▀ ▀█▀   │
│  █▀░ █▀░ █░▄ █▀▄ █▀░ █▀█ █░▄ █▀░ ░█░    │
│  ░░░ ░░░ ░░▀ ▀░▀ ▀▀▀ ▀░▀ ▀▀▀ ▀▀▀ ░▀░    │
└─────────────────────────────────────────┘
""" + Fore.RESET

def print_kali_bg():
    print(KALI_BG)

# ========== СТИЛЬ КАК НА СКРИНЕ ==========
def style_like_screen(text):
    colors = [94, 94, 96, 96, 94, 94, 96, 96]
    result = ""
    for i, char in enumerate(text):
        color_code = colors[i % len(colors)]
        result += f"\033[{color_code}m{char}"
    return result + "\033[0m"

# ========== БАННЕР ==========
BANNER_TEXT = """
██████╗░░█████╗░███╗░░░███╗██████╗░
██╔══██╗██╔══██╗████╗░████║██╔══██╗
██████╦╝██║░░██║██╔████╔██║██████╦╝
██╔══██╗██║░░██║██║╚██╔╝██║██╔══██╗
██████╦╝╚█████╔╝██║░╚═╝░██║██████╦╝
╚═════╝░░╚════╝░╚═╝░░░░░╚═╝╚═════╝░
"""

def print_banner():
    clear_screen()
    print_kali_bg()
    lines = BANNER_TEXT.strip().split('\n')
    for line in lines:
        print(style_like_screen(line))
    print(Fore.CYAN + """
╔══════════════════════════════════════╗
║         BOMB BOTNET v6.6             ║
║         CLEAN START + STATUS         ║
║            by @DADILK                ║
╚══════════════════════════════════════╝
""" + Fore.RESET)

# ========== АНИМАЦИИ ==========
def bomb_animation():
    frames = ["     💣     ", "    💣      ", "   💣       ", "  💣        ", " 💣         ", "💣          ", "💥 БАБАХ! 💥"]
    for frame in frames:
        print(Fore.RED + Style.BRIGHT + f"\r{frame}", end="", flush=True)
        time.sleep(0.15)
    print()

def progress_bar(current, total, text="ЗАГРУЗКА БОТОВ"):
    """Прогресс бар на одной строке"""
    percent = int((current / total) * 100)
    bar_length = 30
    filled = int(bar_length * current / total)
    bar = "█" * filled + "░" * (bar_length - filled)
    
    if percent < 30:
        color = Fore.RED
    elif percent < 60:
        color = Fore.YELLOW
    elif percent < 90:
        color = Fore.CYAN
    else:
        color = Fore.GREEN
    
    print(f"\r{Fore.CYAN}{text}: {color}[{bar}] {percent}%{Fore.RESET}", end="", flush=True)
    
    if current == total:
        print()  # Новая строка после завершения

# ========== НАСТРОЙКА БОТОВ ==========
async def setup_bots():
    global clients, bots_can_spam
    clients = []
    bots_can_spam = False
    
    print_banner()
    print(Fore.YELLOW + f"\n🔧 ЗАГРУЗКА БОТОВ...\n")
    
    if not BOT_TOKENS:
        print(Fore.RED + "❌ Нет токенов!")
        input(Fore.CYAN + "\nНажми Enter...")
        return
    
    total = len(BOT_TOKENS)
    successful = 0
    
    # Прогресс бар при загрузке
    for i, token in enumerate(BOT_TOKENS):
        if not token or token == ".":
            progress_bar(i + 1, total)
            continue
            
        try:
            client = TelegramClient(f'session_bot_{i}', API_ID, API_HASH)
            await client.start(bot_token=token)
            me = await client.get_me()
            
            # Добавляем обработчики
            @client.on(events.ChatAction)
            async def on_add(event):
                if event.user_added and event.user_id == (await event.client.get_me()).id:
                    chat = await event.get_chat()
                    mode_text = "🖼️ КАРТИНКИ" if spam_mode == "image" else "💥 ТЕКСТ"
                    await event.client.send_message(chat.id, 
                        "🔥 **BOMB BOTNET АКТИВИРОВАН** 🔥\n\n"
                        f"Режим: {mode_text}\n"
                        f"⏱️ КД: {BURST_DELAY}с\n"
                        "💣 /bomb - начать атаку\n"
                        "🛑 /stop - остановить\n"
                        "📊 /status - статус")
            
            @client.on(events.NewMessage(pattern='/bomb'))
            async def bomb_cmd(event):
                global bomb_active, target_group, total_messages
                if bomb_active:
                    await event.reply("⚠️ Бомбардировка уже идёт!")
                    return
                
                chat = await event.get_chat()
                target_group = chat.id
                bomb_active = True
                total_messages = 0
                
                bomb_animation()
                mode_text = "🖼️ КАРТИНКИ" if spam_mode == "image" else "💥 ТЕКСТ"
                await event.reply(f"💣 **BOMB STARTED** 💣\n"
                                 f"📢 Группа: {chat.title}\n"
                                 f"🤖 Ботов: {len(clients)}\n"
                                 f"⚡ Режим: {mode_text}\n"
                                 f"⏱️ КД: {BURST_DELAY}с\n"
                                 f"💬 Сообщение: {MESSAGE if spam_mode == 'text' else f'{len(image_urls)} картинок'}")
                
                print(Fore.RED + Style.BRIGHT + f"\n💥 БОМБАРДИРОВКА {chat.title} начата!")
                asyncio.create_task(spam_group(chat.id))
            
            @client.on(events.NewMessage(pattern='/stop'))
            async def stop_cmd(event):
                global bomb_active, total_messages
                if bomb_active:
                    bomb_active = False
                    await event.reply(f"🛑 **BOMB STOPPED**\n📊 Отправлено: {total_messages}\n\n0. ⬅️ exit")
                    print(Fore.YELLOW + f"\n⛔ Атака остановлена. Всего: {total_messages}")
                else:
                    await event.reply("❌ Нет активной атаки")
            
            @client.on(events.NewMessage(pattern='/status'))
            async def status_cmd(event):
                me = await event.client.get_me()
                mode_text = "🖼️ КАРТИНКИ" if spam_mode == "image" else "📝 ТЕКСТ"
                can_spam = "✅ ДА" if bots_can_spam else "❌ НЕТ"
                await event.reply(f"📊 **Статус**\n"
                                 f"🤖 @{me.username}\n"
                                 f"🔥 Режим: {mode_text}\n"
                                 f"⏱️ КД: {BURST_DELAY}с\n"
                                 f"💥 Атака: {'АКТИВНА' if bomb_active else 'ОЖИДАНИЕ'}\n"
                                 f"📨 Отправлено: {total_messages}\n"
                                 f"⚡ Могут спамить: {can_spam}")
            
            clients.append(client)
            successful += 1
            
        except Exception as e:
            pass  # Не показываем ошибки
        
        # Обновляем прогресс бар
        progress_bar(i + 1, total)
        await asyncio.sleep(0.05)
    
    # Стираем прогресс бар и показываем результат
    print("\033[2K\r", end="")  # Стираем строку прогресса
    
    if clients:
        bots_can_spam = True
        print(Fore.GREEN + f"✅ ЗАПУЩЕНО БОТОВ: {successful}/{total}")
        print(Fore.CYAN + "\n🔥 БОТНЕТ АКТИВЕН 🔥")
        print("📱 Добавь ботов в группы")
        print("💣 Введи /bomb в группе для атаки")
        print("🛑 /stop для остановки")
        print(Fore.RED + "⛔ Ctrl+C для возврата в меню\n")
        
        await asyncio.gather(*[client.run_until_disconnected() for client in clients])
    else:
        bots_can_spam = False
        print(Fore.RED + "❌ Не удалось запустить ни одного бота!")
        input(Fore.CYAN + "\nНажми Enter...")

# ========== ФУНКЦИЯ СПАМА ==========
async def spam_group(chat_id):
    global bomb_active, total_messages, bots_can_spam
    
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
                mode_icon = "🖼️" if spam_mode == "image" else "💥"
                bots_can_spam = True
                print(Fore.RED + f"\r{mode_icon} БОМБАРДИРОВКА: {total_messages} | Ботов: {sent} | КД: {BURST_DELAY}с", end="", flush=True)
            except FloodWaitError as e:
                print(Fore.YELLOW + f"\n⏳ Флуд контроль: ждём {e.seconds}с")
                await asyncio.sleep(e.seconds)
            except:
                bots_can_spam = False
                pass
        
        await asyncio.sleep(BURST_DELAY)

# ========== МЕНЮ ==========
def show_menu():
    print_banner()
    mode_display = "🖼️ КАРТИНКИ" if spam_mode == "image" else "📝 ТЕКСТ"
    can_spam = "✅ ДА" if bots_can_spam else "❌ НЕТ"
    print(Fore.CYAN + f"\n📋 ГЛАВНОЕ МЕНЮ (Режим: {mode_display} | КД: {BURST_DELAY}с | Спам: {can_spam}):\n")
    print(Fore.WHITE + "1. 🚀 ЗАПУСТИТЬ БОТНЕТ")
    print("2. 🤖 ДОБАВИТЬ ТОКЕН")
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

# ========== ДОБАВЛЕНИЕ ТОКЕНА ==========
def add_token():
    print_banner()
    print(Fore.YELLOW + "🤖 ДОБАВЛЕНИЕ ТОКЕНОВ\n")
    print(Fore.CYAN + "0 - назад в меню\n")
    
    count = 0
    while True:
        token = input(f"Токен #{len(BOT_TOKENS) + 1}: ").strip()
        if token == "0":
            break
        if token and token != ".":
            BOT_TOKENS.append(token)
            save_config()
            count += 1
            print(Fore.GREEN + f"✅ Токен добавлен! Всего: {len(BOT_TOKENS)}")
        else:
            print(Fore.RED + "❌ Токен не может быть пустым")
    
    if count > 0:
        print(Fore.GREEN + f"\n✅ Добавлено токенов: {count}")
    input(Fore.CYAN + "\nНажми Enter...")

# ========== ПРОСМОТР ТОКЕНОВ ==========
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

# ========== УДАЛЕНИЕ ТОКЕНА ==========
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

# ========== НАСТРОЙКИ API ==========
def edit_api():
    global API_ID, API_HASH
    print_banner()
    print(Fore.YELLOW + "⚙️ НАСТРОЙКИ API\n")
    new_api = input(f"API ID [{API_ID}]: ").strip()
    if new_api:
        try:
            API_ID = int(new_api)
        except:
            print(Fore.RED + "❌ API ID должен быть числом")
    new_hash = input(f"API HASH [{API_HASH[:5]}...]: ").strip()
    if new_hash:
        API_HASH = new_hash
    save_config()
    print(Fore.GREEN + "✅ API сохранены")
    input(Fore.CYAN + "\nНажми Enter...")

# ========== ИЗМЕНИТЬ ТЕКСТ ==========
def edit_message():
    global MESSAGE
    print_banner()
    print(Fore.YELLOW + "✏️ ИЗМЕНИТЬ ТЕКСТ\n")
    new_msg = input(f"Новый текст [{MESSAGE}]: ").strip()
    if new_msg:
        MESSAGE = new_msg
        save_config()
        print(Fore.GREEN + f"✅ Текст изменен: {MESSAGE}")
    input(Fore.CYAN + "\nНажми Enter...")

# ========== ПЕРЕКЛЮЧЕНИЕ РЕЖИМА ==========
def toggle_spam_mode():
    global spam_mode
    print_banner()
    print(Fore.YELLOW + "🖼️ РЕЖИМ СПАМА\n")
    print(f"Сейчас: {'🖼️ КАРТИНКИ' if spam_mode == 'image' else '📝 ТЕКСТ'}")
    print("1. 📝 Текст")
    print("2. 🖼️ Картинки")
    print("0. 🔙 Назад")
    
    choice = input("\nВыбери: ").strip()
    if choice == "1":
        spam_mode = "text"
        save_config()
        print(Fore.GREEN + "✅ Текстовый режим")
    elif choice == "2":
        if image_urls:
            spam_mode = "image"
            save_config()
            print(Fore.GREEN + "✅ Режим картинок")
        else:
            print(Fore.YELLOW + "⚠️ Сначала добавь картинки (пункт 8)!")
    input(Fore.CYAN + "\nНажми Enter...")

# ========== ДОБАВИТЬ КАРТИНКУ ==========
def add_image_url():
    global image_urls
    print_banner()
    print(Fore.YELLOW + "📸 ДОБАВЛЕНИЕ КАРТИНОК\n")
    print(Fore.CYAN + "0 - назад в меню\n")
    
    count = 0
    while True:
        url = input(f"Ссылка #{len(image_urls) + 1}: ").strip()
        if url == "0":
            break
        if url:
            image_urls.append(url)
            save_config()
            count += 1
            print(Fore.GREEN + f"✅ Картинка добавлена! Всего: {len(image_urls)}")
        else:
            print(Fore.RED + "❌ Ссылка не может быть пустой")
    
    if count > 0:
        print(Fore.GREEN + f"\n✅ Добавлено картинок: {count}")
    input(Fore.CYAN + "\nНажми Enter...")

# ========== ИЗМЕНИТЬ КД ==========
def edit_delay():
    global BURST_DELAY
    print_banner()
    print(Fore.YELLOW + "⏱️ ИЗМЕНИТЬ КД\n")
    print(f"Текущая задержка: {BURST_DELAY}с")
    try:
        new_delay = input(f"Новая задержка: ").strip()
        if new_delay:
            new_delay = float(new_delay)
            if new_delay >= 0:
                BURST_DELAY = new_delay
                save_config()
                print(Fore.GREEN + f"✅ КД изменено на {BURST_DELAY}с")
            else:
                print(Fore.RED + "❌ Задержка не может быть отрицательной")
    except:
        print(Fore.RED + "❌ Введи число")
    input(Fore.CYAN + "\nНажми Enter...")

# ========== СТАТУС ==========
def show_status():
    print_banner()
    print(Fore.MAGENTA + "📊 СТАТУС:\n")
    print(f"🔑 API ID: {API_ID}")
    print(f"🔑 API HASH: {API_HASH[:5]}...{API_HASH[-5:]}")
    print(f"🤖 Ботов в конфиге: {len(BOT_TOKENS)}")
    print(f"⚡ Активных сессий: {len(clients)}")
    print(f"📝 Режим: {'🖼️ КАРТИНКИ' if spam_mode == 'image' else '📝 ТЕКСТ'}")
    print(f"🖼️ Картинок в базе: {len(image_urls)}")
    print(f"⏱️ КД: {BURST_DELAY}с")
    print(f"💥 Атака активна: {'ДА' if bomb_active else 'НЕТ'}")
    print(f"📨 Всего отправлено: {total_messages}")
    can_spam = "✅ МОГУТ СПАМИТЬ" if bots_can_spam else "❌ НЕ МОГУТ СПАМИТЬ"
    print(f"⚡ Статус ботов: {can_spam}")
    input(Fore.CYAN + "\nНажми Enter...")

# ========== ИНСТРУКЦИЯ ==========
def show_help():
    print_banner()
    print(Fore.BLUE + "📖 ИНСТРУКЦИЯ:\n")
    print("1️⃣ API: https://my.telegram.org/apps")
    print("2️⃣ Токены: @BotFather")
    print("3️⃣ Команды в группе:")
    print("   • /bomb - атака")
    print("   • /stop - стоп")
    print("   • /status - статус")
    print("4️⃣ В статусе видно могут ли боты спамить")
    input(Fore.CYAN + "\nНажми Enter...")

# ========== ГЛАВНАЯ ==========
async def main():
    load_config()
    
    while True:
        show_menu()
        choice = input(Fore.CYAN + "👉 Выбери пункт: ").strip()
        
        if choice == "1":
            await setup_bots()  # Здесь меню стирается и показывается только прогресс
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
            bomb_animation()
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
        print(Fore.GREEN + "\n✅ Боты отключены")
