import os
import sys
import time
import asyncio
import random
import shutil
from pyrogram import Client, filters
from colorama import Fore, init, Style

init(autoreset=True)

# ========== НАСТРОЙКИ АНИМАЦИИ ==========
TYPING_SPEED = 0.03  # Скорость печати (сек)
ANIMATION_FRAMES = 30  # Кадры для загрузки

# ========== ФУНКЦИИ АНИМАЦИИ ==========
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def typing_effect(text, color=Fore.CYAN, delay=TYPING_SPEED):
    """Эффект печатающегося текста"""
    for char in text:
        print(color + char, end='', flush=True)
        time.sleep(delay)
    print()

def loading_animation(text="ЗАГРУЗКА", seconds=2):
    """Анимация загрузки со спиннером"""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + seconds
    i = 0
    while time.time() < end_time:
        print(Fore.YELLOW + f"\r{text} {frames[i % len(frames)]}", end="", flush=True)
        time.sleep(0.1)
        i += 1
    print("\r" + " " * (len(text) + 2) + "\r", end="")

def progress_bar(percent, width=40, color=Fore.GREEN):
    """Прогресс бар"""
    filled = int(width * percent / 100)
    bar = "█" * filled + "░" * (width - filled)
    print(f"\r{color}[{bar}] {percent}%", end="", flush=True)

def bomb_explosion_effect():
    """Эффект взрыва бомбы"""
    explosion_frames = [
        "💣     ",
        "  💣   ",
        "    💣 ",
        "     💥",
        "    💥 ",
        "   💥  ",
        "  💥   ",
        " 💥    ",
        "💥     ",
    ]
    for frame in explosion_frames:
        print(Fore.RED + Style.BRIGHT + f"\r{frame}", end="", flush=True)
        time.sleep(0.1)
    print()

def matrix_effect(text, color=Fore.GREEN):
    """Матричный эффект появления текста"""
    for i in range(len(text) + 1):
        line = text[:i] + ''.join(random.choice("01") for _ in range(len(text) - i))
        print(color + f"\r{line}", end="", flush=True)
        time.sleep(0.05)
    print()

# ========== ASCII АРТ С АНИМАЦИЕЙ ==========
def show_banner_animated():
    clear_screen()
    banner_lines = [
        (Fore.RED + "██████╗░░█████╗░███╗░░░███╗██████╗░"),
        (Fore.RED + "██╔══██╗██╔══██╗████╗░████║██╔══██╗"),
        (Fore.RED + "██████╦╝██║░░██║██╔████╔██║██████╦╝"),
        (Fore.RED + "██╔══██╗██║░░██║██║╚██╔╝██║██╔══██╗"),
        (Fore.RED + "██████╦╝╚█████╔╝██║░╚═╝░██║██████╦╝"),
        (Fore.RED + "╚═════╝░░╚════╝░╚═╝░░░░░╚═╝╚═════╝░"),
        (Fore.CYAN + "╔══════════════════════════════════════╗"),
        (Fore.CYAN + "║     BOMB SPAMER CLAN v5.0 PREMIUM    ║"),
        (Fore.CYAN + "║         MULTI-BOT /bomb SPAM         ║"),
        (Fore.CYAN + "║         ANIMATED EDITION 🔥          ║"),
        (Fore.CYAN + "╚══════════════════════════════════════╝"),
    ]
    
    # Печатаем баннер с эффектом
    for line in banner_lines:
        typing_effect(line, delay=0.01)
    print()

# ========== ПОЛУЧЕНИЕ API ==========
def get_api_credentials():
    show_banner_animated()
    typing_effect("🔑 НАСТРОЙКА API ДОСТУПА", Fore.YELLOW)
    print("\n" + Fore.WHITE + "1. Зайди на https://my.telegram.org")
    print("2. Создай приложение")
    print("3. Скопируй API ID и API HASH\n")
    
    api_id = input(Fore.CYAN + "👉 API ID (число): ").strip()
    api_hash = input(Fore.CYAN + "👉 API HASH (строка): ").strip()
    
    with open("api_config.txt", "w") as f:
        f.write(f"{api_id}\n{api_hash}")
    
    print(Fore.GREEN + "\n✅ API данные сохранены")
    loading_animation("Сохранение", 1)
    return int(api_id), api_hash

# ========== ВВОД ТОКЕНОВ ==========
def input_tokens():
    show_banner_animated()
    typing_effect("🤖 ВВЕДИТЕ ТОКЕНЫ БОТОВ", Fore.YELLOW)
    print(Fore.GREEN + "\n(Когда закончите, введите: end)\n")
    
    tokens = []
    counter = 1
    while True:
        token = input(Fore.CYAN + f"Бот #{counter} > ").strip()
        if token.lower() == "end":
            break
        if token:
            tokens.append(token)
            print(Fore.GREEN + f"✓ Токен {counter} добавлен")
            counter += 1
    
    loading_animation(f"Обработка {len(tokens)} токенов", 1)
    return tokens

# ========== НАСТРОЙКИ АТАКИ ==========
def input_group_settings():
    show_banner_animated()
    typing_effect("⚙️ НАСТРОЙКИ АТАКИ", Fore.YELLOW)
    print()
    
    group_input = input(Fore.CYAN + "📢 Группа (username или ID): ").strip()
    
    if group_input.startswith('-') and group_input[1:].isdigit():
        group_id = int(group_input)
        print(Fore.GREEN + f"✓ ID группы: {group_id}")
    else:
        group_id = group_input
        print(Fore.GREEN + f"✓ Username: {group_id}")
    
    message = input(Fore.CYAN + "💬 Текст сообщения: ")
    count = int(input(Fore.CYAN + "🔢 Количество сообщений на бота: "))
    delay = float(input(Fore.CYAN + "⏱️ Задержка (сек, напр. 0.5): "))
    
    return group_id, message, count, delay

# ========== ЗАПУСК БОТОВ ==========
async def start_bots(api_id, api_hash, tokens, group, message, count, delay):
    show_banner_animated()
    typing_effect("💣 ЗАПУСК БОМБАРДИРОВКИ", Fore.RED, 0.05)
    bomb_explosion_effect()
    print()
    
    active_bots = []
    successful = 0
    
    for i, token in enumerate(tokens):
        progress_bar(int((i+1)/len(tokens)*100))
        
        try:
            app = Client(
                f"bot_session_{i}",
                api_id=api_id,
                api_hash=api_hash,
                bot_token=token,
                in_memory=True
            )
            
            await app.start()
            me = await app.get_me()
            
            # Матричный эффект для успешного запуска
            matrix_effect(f"✓ БОТ @{me.username} ЗАПУЩЕН", Fore.GREEN)
            
            @app.on_message(filters.command("bomb") & filters.group)
            async def bomb_handler(client, msg):
                chat_id = msg.chat.id
                chat_title = msg.chat.title
                print(Fore.RED + Style.BRIGHT + f"\n[💥] @{me.username} АКТИВИРОВАН в {chat_title}")
                
                for j in range(count):
                    try:
                        await client.send_message(chat_id, f"{message} [#{j+1}]")
                        print(Fore.GREEN + f"    [{j+1}/{count}] @{me.username} → {message[:20]}...")
                        await asyncio.sleep(delay)
                    except Exception as e:
                        print(Fore.RED + f"    [!] Ошибка: {e}")
                        break
            
            active_bots.append(app)
            successful += 1
            
        except Exception as e:
            print(Fore.RED + f"\n[✗] Ошибка бота {i+1}: {e}")
    
    print()
    matrix_effect(f"✅ АКТИВНО БОТОВ: {successful}/{len(tokens)}", Fore.MAGENTA)
    typing_effect("🔥 Теперь пиши /bomb в группах!", Fore.YELLOW)
    typing_effect("⛔ Ctrl+C для остановки\n", Fore.RED, 0.02)
    
    try:
        await asyncio.gather(*(app.idle() for app in active_bots))
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n⛔ Остановка...")
        for app in active_bots:
            await app.stop()

# ========== МЕНЮ С АНИМАЦИЕЙ ==========
async def main():
    # Загружаем API
    api_id, api_hash = None, None
    try:
        with open("api_config.txt", "r") as f:
            lines = f.readlines()
            api_id = int(lines[0].strip())
            api_hash = lines[1].strip()
    except:
        pass
    
    if not api_id or not api_hash:
        api_id, api_hash = get_api_credentials()
    
    while True:
        show_banner_animated()
        print(Fore.CYAN + f"🔑 API ID: {api_id}\n")
        
        menu_items = [
            ("1", "💣 ЗАПУСТИТЬ БОМБАРДИРОВКУ"),
            ("2", "🔄 СМЕНИТЬ API КЛЮЧИ"),
            ("3", "📋 ИНСТРУКЦИЯ"),
            ("4", "🧹 ОЧИСТИТЬ ЭКРАН"),
            ("0", "🚪 ВЫХОД")
        ]
        
        for key, text in menu_items:
            typing_effect(f"{key}. {text}", Fore.WHITE, 0.005)
        
        print()
        choice = input(Fore.CYAN + "👉 Выбери пункт: ")
        
        if choice == "1":
            tokens = input_tokens()
            if tokens:
                group, message, count, delay = input_group_settings()
                await start_bots(api_id, api_hash, tokens, group, message, count, delay)
            
        elif choice == "2":
            api_id, api_hash = get_api_credentials()
            
        elif choice == "3":
            show_banner_animated()
            typing_effect("📘 ИНСТРУКЦИЯ", Fore.MAGENTA, 0.03)
            print("\n" + Fore.WHITE + 
                  "1️⃣ API КЛЮЧИ: https://my.telegram.org/apps\n"
                  "2️⃣ ТОКЕНЫ: @BotFather → /newbot\n"
                  "3️⃣ Добавь ботов в группу (админы!)\n"
                  "4️⃣ В группе пиши /bomb\n")
            input(Fore.CYAN + "Нажми Enter...")
            
        elif choice == "4":
            clear_screen()
            matrix_effect("✅ ЭКРАН ОЧИЩЕН", Fore.GREEN)
            await asyncio.sleep(1)
            
        elif choice == "0":
            show_banner_animated()
            typing_effect("👋 ВЫХОД... ДО ВСТРЕЧИ!", Fore.RED, 0.03)
            bomb_explosion_effect()
            break

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n⛔ Выход по Ctrl+C")
