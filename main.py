import os
import asyncio
import time
import json
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError
from telethon.tl.types import MessageMediaPhoto
from colorama import Fore, init, Style

init(autoreset=True)

# ========== ФАЙЛ КОНФИГУРАЦИИ ==========
CONFIG_FILE = "bomb_config.json"

# ========== ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ==========
clients = []
bomb_active = False
target_group = None
total_messages = 0
spam_mode = "text"  # "text" или "image"
image_urls = []

# ========== ЗАГРУЗКА/СОХРАНЕНИЕ КОНФИГА ==========
def load_config():
    """Загружает настройки из файла"""
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
    except FileNotFoundError:
        # Значения по умолчанию
        API_ID = 12345
        API_HASH = "your_api_hash"
        BOT_TOKENS = []
        MESSAGE = "💥"
        BURST_DELAY = 0.05
        spam_mode = "text"
        image_urls = []
        return False
    except Exception as e:
        print(Fore.RED + f"❌ Ошибка загрузки: {e}")
        return False

def save_config():
    """Сохраняет настройки в файл"""
    config = {
        'api_id': API_ID,
        'api_hash': API_HASH,
        'bot_tokens': BOT_TOKENS,
        'message': MESSAGE,
        'burst_delay': BURST_DELAY,
        'spam_mode': spam_mode,
        'image_urls': image_urls
    }
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
        print(Fore.GREEN + "✅ Конфиг сохранён")
        return True
    except Exception as e:
        print(Fore.RED + f"❌ Ошибка сохранения: {e}")
        return False

# ========== ФУНКЦИИ АНИМАЦИИ ==========
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
    print(Fore.RED + Style.BRIGHT + "\r💥 BOMB LAUNCHED! 💥")

# ========== ГРАДИЕНТНЫЙ БАННЕР (КРАСНЫЙ) ==========
def gradient_red(text, step=0):
    """Красный градиент"""
    colors = [91, 92, 93, 94, 95, 96, 97, 91, 92, 93, 94, 95, 96, 97]
    result = ""
    for i, char in enumerate(text):
        color_code = colors[(i + step) % len(colors)]
        result += f"\033[{color_code}m{char}"
    return result + "\033[0m"

BANNER = """
██████╗░░█████╗░███╗░░░███╗██████╗░
██╔══██╗██╔══██╗████╗░████║██╔══██╗
██████╦╝██║░░██║██╔████╔██║██████╦╝
██╔══██╗██║░░██║██║╚██╔╝██║██╔══██╗
██████╦╝╚█████╔╝██║░╚═╝░██║██████╦╝
╚═════╝░░╚════╝░╚═╝░░░░░╚═╝╚═════╝░
"""

def print_banner():
    clear_screen()
    lines = BANNER.strip().split('\n')
    for i, line in enumerate(lines):
        print(gradient_red(line, i * 3))
    print(Fore.CYAN + """
╔══════════════════════════════════════╗
║         BOMB BOTNET v5.1             ║
║         КД + EXIT                     ║
║            by @DADILK                ║
╚══════════════════════════════════════╝
""" + Fore.RESET)

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
    print("6. ✏️ ИЗМЕНИТЬ ТЕКСТ СООБЩЕНИЯ")
    print("7. 🖼️ РЕЖИМ СПАМА (текст/картинки)")
    print("8. 📸 ДОБАВИТЬ ССЫЛКУ НА КАРТИНКУ")
    print("9. ⏱️ ИЗМЕНИТЬ ЗАДЕРЖКУ (КД)")
    print("10. 📊 СТАТУС")
    print("11. 🧹 ОЧИСТИТЬ ЭКРАН")
    print("12. 📖 ИНСТРУКЦИЯ")
    print("0. 🚪 ВЫХОД\n")
    print(Fore.YELLOW + f"🤖 Ботов: {len(BOT_TOKENS)} | 📸 Картинок: {len(image_urls)} | ⏱️ КД: {BURST_DELAY}с")

# ========== ИЗМЕНИТЬ ТЕКСТ ==========
def edit_message():
    global MESSAGE
    print_banner()
    print(Fore.YELLOW + "✏️ ИЗМЕНЕНИЕ ТЕКСТА СООБЩЕНИЯ\n")
    print(f"Текущий текст: {MESSAGE}")
    new_message = input("Новый текст: ").strip()
    if new_message:
        MESSAGE = new_message
        save_config()
        print(Fore.GREEN + f"✅ Текст изменён на: {MESSAGE}")
    else:
        print(Fore.RED + "❌ Текст не может быть пустым")
    input(Fore.CYAN + "\n0. ⬅️ Нажми Enter для возврата...")

# ========== ИЗМЕНИТЬ ЗАДЕРЖКУ (КД) ==========
def edit_delay():
    global BURST_DELAY
    print_banner()
    print(Fore.YELLOW + "⏱️ ИЗМЕНЕНИЕ ЗАДЕРЖКИ (КД)\n")
    print(f"Текущая задержка: {BURST_DELAY} секунд")
    print("Рекомендация: 0.05 - быстро, 0.5 - медленно\n")
    try:
        new_delay = float(input("Новая задержка (сек): ").strip())
        if new_delay >= 0:
            BURST_DELAY = new_delay
            save_config()
            print(Fore.GREEN + f"✅ Задержка изменена на: {BURST_DELAY}с")
        else:
            print(Fore.RED + "❌ Задержка не может быть отрицательной")
    except:
        print(Fore.RED + "❌ Введи число (например 0.05)")
    input(Fore.CYAN + "\n0. ⬅️ Нажми Enter для возврата...")

# ========== ПЕРЕКЛЮЧЕНИЕ РЕЖИМА ==========
def toggle_spam_mode():
    global spam_mode
    print_banner()
    print(Fore.YELLOW + "🖼️ РЕЖИМ СПАМА\n")
    print(f"Текущий режим: {'🖼️ КАРТИНКИ' if spam_mode == 'image' else '📝 ТЕКСТ'}")
    print("\n1. 📝 Текстовый режим")
    print("2. 🖼️ Режим картинок")
    print("0. ❌ Отмена")
    
    choice = input(Fore.CYAN + "\nВыбери режим: ").strip()
    if choice == "1":
        spam_mode = "text"
        save_config()
        print(Fore.GREEN + "✅ Режим изменён на ТЕКСТОВЫЙ")
    elif choice == "2":
        if not image_urls:
            print(Fore.YELLOW + "⚠️ Сначала добавь ссылки на картинки!")
        else:
            spam_mode = "image"
            save_config()
            print(Fore.GREEN + "✅ Режим изменён на КАРТИНКИ")
    input(Fore.CYAN + "\n0. ⬅️ Нажми Enter для возврата...")

# ========== ДОБАВЛЕНИЕ КАРТИНКИ ==========
def add_image_url():
    global image_urls
    print_banner()
    print(Fore.YELLOW + "📸 ДОБАВЛЕНИЕ ССЫЛКИ НА КАРТИНКУ\n")
    print("Поддерживаются ссылки на .jpg .png .gif")
    print("Пример: https://example.com/image.jpg\n")
    
    url = input("Введи ссылку: ").strip()
    if url:
        image_urls.append(url)
        save_config()
        print(Fore.GREEN + f"✅ Картинка добавлена! Всего: {len(image_urls)}")
    else:
        print(Fore.RED + "❌ Ссылка не может быть пустой")
    input(Fore.CYAN + "\n0. ⬅️ Нажми Enter для возврата...")

# ========== ДОБАВЛЕНИЕ ТОКЕНА ==========
def add_token():
    print_banner()
    print(Fore.YELLOW + "🤖 ДОБАВЛЕНИЕ ТОКЕНА БОТА\n")
    print("1 токен = 1 бот")
    print("Получить токен: @BotFather → /newbot\n")
    
    token = input("Введи токен бота: ").strip()
    if token:
        BOT_TOKENS.append(token)
        save_config()
        print(Fore.GREEN + f"\n✅ Токен добавлен! Теперь ботов: {len(BOT_TOKENS)}")
    else:
        print(Fore.RED + "❌ Токен не может быть пустым")
    
    input(Fore.CYAN + "\n0. ⬅️ Нажми Enter для возврата...")

# ========== ПРОСМОТР ТОКЕНОВ ==========
def show_tokens():
    print_banner()
    print(Fore.CYAN + "👀 СПИСОК ТОКЕНОВ:\n")
    
    if not BOT_TOKENS:
        print(Fore.YELLOW + "Нет сохранённых токенов")
    else:
        for i, token in enumerate(BOT_TOKENS):
            if len(token) > 20:
                shown = token[:10] + "..." + token[-5:]
            else:
                shown = token
            print(f"{i+1}. {shown}")
    
    input(Fore.CYAN + "\n0. ⬅️ Нажми Enter для возврата...")

# ========== УДАЛЕНИЕ ТОКЕНА ==========
def delete_token():
    print_banner()
    print(Fore.YELLOW + "🗑️ УДАЛЕНИЕ ТОКЕНА\n")
    
    if not BOT_TOKENS:
        print(Fore.YELLOW + "Нет токенов для удаления")
        input(Fore.CYAN + "\n0. ⬅️ Нажми Enter для возврата...")
        return
    
    for i, token in enumerate(BOT_TOKENS):
        shown = token[:10] + "..." + token[-5:] if len(token) > 20 else token
        print(f"{i+1}. {shown}")
    
    try:
        choice = int(input(Fore.RED + "\nНомер токена для удаления (0 - отмена): "))
        if 1 <= choice <= len(BOT_TOKENS):
            deleted = BOT_TOKENS.pop(choice-1)
            save_config()
            print(Fore.GREEN + f"✅ Токен {choice} удалён")
        elif choice != 0:
            print(Fore.RED + "❌ Неверный номер")
    except:
        print(Fore.RED + "❌ Ошибка ввода")
    
    input(Fore.CYAN + "\n0. ⬅️ Нажми Enter для возврата...")

# ========== НАСТРОЙКИ API ==========
def edit_api():
    global API_ID, API_HASH
    
    print_banner()
    print(Fore.YELLOW + "⚙️ НАСТРОЙКИ API\n")
    print("Получить на https://my.telegram.org/apps\n")
    
    print(f"Текущий API ID: {API_ID}")
    new_api = input("Новый API ID (Enter - оставить): ").strip()
    if new_api:
        try:
            API_ID = int(new_api)
        except:
            print(Fore.RED + "❌ API ID должен быть числом")
    
    print(f"\nТекущий API HASH: {API_HASH[:5]}...{API_HASH[-5:]}")
    new_hash = input("Новый API HASH (Enter - оставить): ").strip()
    if new_hash:
        API_HASH = new_hash
    
    save_config()
    input(Fore.CYAN + "\n0. ⬅️ Нажми Enter для возврата...")

# ========== СТАТУС ==========
def show_status():
    print_banner()
    print(Fore.MAGENTA + "📊 СТАТУС:\n")
    print(f"API ID: {API_ID}")
    print(f"API HASH: {API_HASH[:5]}...{API_HASH[-5:]}")
    print(f"Ботов в конфиге: {len(BOT_TOKENS)}")
    print(f"Активных сессий: {len(clients)}")
    print(f"Сообщение: {MESSAGE}")
    print(f"Режим спама: {'🖼️ КАРТИНКИ' if spam_mode == 'image' else '📝 ТЕКСТ'}")
    print(f"Картинок в базе: {len(image_urls)}")
    print(f"Задержка (КД): {BURST_DELAY} сек")
    print(f"Атака активна: {'ДА' if bomb_active else 'НЕТ'}")
    print(f"Всего отправлено: {total_messages}")
    input(Fore.CYAN + "\n0. ⬅️ Нажми Enter для возврата...")

# ========== ИНСТРУКЦИЯ ==========
def show_help():
    print_banner()
    print(Fore.BLUE + "📖 ИНСТРУКЦИЯ:\n")
    print("1️⃣ API КЛЮЧИ:")
    print("   • https://my.telegram.org/apps")
    print("2️⃣ ТОКЕНЫ БОТОВ:")
    print("   • @BotFather → /newbot")
    print("3️⃣ РЕЖИМЫ:")
    print("   • ТЕКСТ: спамит текстом")
    print("   • КАРТИНКИ: спамит картинками по ссылкам")
    print("4️⃣ КД (ЗАДЕРЖКА):")
    print("   • 0.05 - очень быстро (риск бана)")
    print("   • 0.1-0.3 - оптимально")
    print("   • 0.5+ - медленно, безопасно")
    print("5️⃣ КОМАНДЫ В ГРУППЕ:")
    print("   • /bomb - начать атаку 💣")
    print("   • /stop - остановить 🛑")
    print("   • /status - статус бота")
    input(Fore.CYAN + "\n0. ⬅️ Нажми Enter для возврата...")

# ========== ЗАПУСК БОТОВ ==========
async def setup_bots():
    global clients
    clients = []
    
    print_banner()
    print(Fore.YELLOW + f"\n🤖 ЗАПУСК {len(BOT_TOKENS)} БОТОВ...\n")
    
    if not BOT_TOKENS:
        print(Fore.RED + "❌ Нет токенов!")
        input(Fore.CYAN + "\n0. ⬅️ Нажми Enter для возврата...")
        return
    
    successful = 0
    for i, token in enumerate(BOT_TOKENS):
        try:
            if not token or token == "":
                continue
                
            client = TelegramClient(f'session_bot_{i}', API_ID, API_HASH)
            await client.start(bot_token=token)
            me = await client.get_me()
            print(Fore.GREEN + f"[✓] Бот {i+1}: @{me.username}")
            clients.append(client)
            successful += 1
            loading_animation(f"Загрузка бота {i+1}", 0.2)
        except Exception as e:
            print(Fore.RED + f"[✗] Бот {i+1} ошибка: {e}")
    
    if clients:
        print(Fore.MAGENTA + f"\n✅ ЗАПУЩЕНО БОТОВ: {successful}/{len(BOT_TOKENS)}")
        
        for client in clients:
            client.add_event_handler(on_add)
            client.add_event_handler(bomb_cmd)
            client.add_event_handler(stop_cmd)
            client.add_event_handler(status_cmd)
        
        print(Fore.CYAN + "\n🔥 БОТНЕТ АКТИВЕН 🔥")
        print(f"🤖 Активных ботов: {len(clients)}")
        print(f"⏱️ Задержка (КД): {BURST_DELAY}с")
        print("📱 Добавь ботов в группы")
        print("💣 Введи /bomb в группе для атаки")
        print("🛑 /stop для остановки")
        print(Fore.RED + "⛔ Нажми Ctrl+C для возврата в меню\n")
        
        await asyncio.gather(*[client.run_until_disconnected() for client in clients])
    else:
        print(Fore.RED + "❌ Не удалось запустить ни одного бота!")
        input(Fore.CYAN + "\n0. ⬅️ Нажми Enter для возврата...")

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
                    # Выбираем случайную картинку из списка
                    if image_urls:
                        import random
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
                print(Fore.RED + f"\r{mode_icon} БОМБАРДИРОВКА: {total_messages} | Ботов: {sent} | КД: {BURST_DELAY}с", end="", flush=True)
            except FloodWaitError as e:
                print(Fore.YELLOW + f"\n⏳ Флуд контроль: ждём {e.seconds}с")
                await asyncio.sleep(e.seconds)
            except Exception:
                pass
        
        await asyncio.sleep(BURST_DELAY)

# ========== ОБРАБОТЧИКИ ==========
@events.register(events.ChatAction)
async def on_add(event):
    if event.user_added and event.user_id == (await event.client.get_me()).id:
        chat = await event.get_chat()
        print(Fore.GREEN + f"\n[+] Бот добавлен в {chat.title}")
        mode_text = "🖼️ КАРТИНКИ" if spam_mode == "image" else "💥 ТЕКСТ"
        await event.client.send_message(chat.id, 
            "🔥 **BOMB BOTNET АКТИВИРОВАН** 🔥\n\n"
            f"Режим: {mode_text}\n"
            f"⏱️ КД: {BURST_DELAY}с\n"
            "💣 /bomb - начать атаку\n"
            "🛑 /stop - остановить\n"
            "📊 /status - статус")

@events.register(events.NewMessage(pattern='/bomb'))
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
    
    print(Fore.RED + Style.BRIGHT + f"\n💥 БОМБАРДИРОВКА {chat.title} начата! (КД: {BURST_DELAY}с)")
    await spam_group(chat.id)

@events.register(events.NewMessage(pattern='/stop'))
async def stop_cmd(event):
    global bomb_active, total_messages
    if bomb_active:
        bomb_active = False
        await event.reply(f"🛑 **BOMB STOPPED**\n📊 Отправлено: {total_messages}\n\n0. ⬅️ exit (вернуться в меню)")
        print(Fore.YELLOW + f"\n⛔ Атака остановлена. Всего: {total_messages}")
        print(Fore.CYAN + "0. ⬅️ Нажми Enter для возврата в меню...")
    else:
        await event.reply("❌ Нет активной атаки")

@events.register(events.NewMessage(pattern='/status'))
async def status_cmd(event):
    me = await event.client.get_me()
    mode_text = "🖼️ КАРТИНКИ" if spam_mode == "image" else "📝 ТЕКСТ"
    await event.reply(f"📊 **Статус**\n"
                     f"🤖 @{me.username}\n"
                     f"🔥 Режим: {mode_text}\n"
                     f"⏱️ КД: {BURST_DELAY}с\n"
                     f"💥 Атака: {'АКТИВНА' if bomb_active else 'ОЖИДАНИЕ'}\n"
                     f"📨 Отправлено: {total_messages}")

# ========== ГЛАВНАЯ ==========
async def main():
    # Загружаем конфиг
    if not load_config():
        print(Fore.YELLOW + "⚠️ Создан новый конфиг")
    
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
            print(Fore.GREEN + "✅ Экран очищен!")
            await asyncio.sleep(1)
        elif choice == "12":
            show_help()
        elif choice == "0":
            clear_screen()
            bomb_animation()
            print(Fore.RED + "\n👋 Пока!")
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
        print(Fore.CYAN + "\n0. ⬅️ Нажми Enter для выхода...")
