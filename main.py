import os
import sys
import time
import asyncio
import random
from pyrogram import Client, filters
from colorama import Fore, init, Style

init(autoreset=True)

# ========== ПРОСТАЯ АНИМАЦИЯ ==========
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def loading_animation(text="ЗАГРУЗКА", duration=1.5):
    """Простая анимация загрузки"""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        print(Fore.YELLOW + f"\r{text} {frames[i % len(frames)]}", end="", flush=True)
        time.sleep(0.1)
        i += 1
    print("\r" + " " * 30 + "\r", end="")

def bomb_animation():
    """Простая анимация бомбы"""
    for _ in range(3):
        print(Fore.RED + "\r💣", end="", flush=True)
        time.sleep(0.2)
        print(Fore.RED + "\r 💣", end="", flush=True)
        time.sleep(0.2)
        print(Fore.RED + "\r  💣", end="", flush=True)
        time.sleep(0.2)
    print(Fore.RED + Style.BRIGHT + "\r💥 БАБАХ! 💥")

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
║     BOMB SPAMER CLAN v5.0 ПРОСТО     ║
║            by @DADILK                ║
╚══════════════════════════════════════╝
""" + Fore.RESET

# ========== ОСТАЛЬНОЙ КОД БЕЗ ИЗМЕНЕНИЙ ==========
# (весь функционал как в v4.2, только добавил анимации выше)

def show_banner():
    clear_screen()
    print(BANNER)

def get_api_credentials():
    show_banner()
    print(Fore.YELLOW + "\n🔑 ВВЕДИ API ДАННЫЕ")
    print("(получить на my.telegram.org)\n")
    api_id = input("API ID: ").strip()
    api_hash = input("API HASH: ").strip()
    
    with open("api_config.txt", "w") as f:
        f.write(f"{api_id}\n{api_hash}")
    
    loading_animation("Сохранение", 1)
    return int(api_id), api_hash

def load_api():
    try:
        with open("api_config.txt", "r") as f:
            lines = f.readlines()
            return int(lines[0].strip()), lines[1].strip()
    except:
        return None, None

def input_tokens():
    show_banner()
    print(Fore.YELLOW + "\n🤖 ВВЕДИ ТОКЕНЫ БОТОВ")
    print(Fore.GREEN + "(когда закончишь, напиши end)\n")
    
    tokens = []
    count = 1
    while True:
        token = input(f"Бот #{count}: ").strip()
        if token.lower() == "end":
            break
        if token:
            tokens.append(token)
            print(Fore.GREEN + f"✓ Добавлен бот #{count}")
            count += 1
    
    loading_animation(f"Загружено {len(tokens)} ботов", 1)
    return tokens

def input_group():
    print(Fore.YELLOW + "\n⚙️ НАСТРОЙКИ ГРУППЫ")
    group = input("Username или ID группы: ").strip()
    
    if group.startswith('-') and group[1:].isdigit():
        group = int(group)
    
    msg = input("Текст сообщения: ")
    count = int(input("Количество сообщений на бота: "))
    delay = float(input("Задержка (сек): "))
    
    return group, msg, count, delay

async def start_bots(api_id, api_hash, tokens, group, msg, count, delay):
    show_banner()
    bomb_animation()
    print(Fore.RED + Style.BRIGHT + "\n💣 ЗАПУСК БОТОВ...\n")
    
    active = []
    
    for i, token in enumerate(tokens):
        try:
            app = Client(
                f"bot_{i}",
                api_id=api_id,
                api_hash=api_hash,
                bot_token=token,
                in_memory=True
            )
            
            await app.start()
            me = await app.get_me()
            print(Fore.GREEN + f"[✓] Бот @{me.username} запущен")
            
            @app.on_message(filters.command("bomb") & filters.group)
            async def bomb_handler(client, msg):
                chat = msg.chat
                print(Fore.RED + f"\n[💥] Бот активирован в {chat.title}")
                
                for j in range(count):
                    try:
                        await client.send_message(chat.id, f"{msg} [#{j+1}]")
                        print(Fore.GREEN + f"    [{j+1}/{count}] отправлено")
                        await asyncio.sleep(delay)
                    except:
                        print(Fore.RED + "    [✗] ошибка отправки")
                        break
            
            active.append(app)
            
        except Exception as e:
            print(Fore.RED + f"[✗] Ошибка бота {i+1}: {e}")
    
    print(Fore.MAGENTA + f"\n✅ АКТИВНО: {len(active)}/{len(tokens)} ботов")
    print(Fore.YELLOW + "\n🔥 Жду команду /bomb в группах...")
    print(Fore.RED + "⛔ Ctrl+C для остановки\n")
    
    try:
        await asyncio.gather(*(app.idle() for app in active))
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n⛔ Останавливаю...")
        for app in active:
            await app.stop()

async def main():
    api_id, api_hash = load_api()
    if not api_id:
        api_id, api_hash = get_api_credentials()
    
    while True:
        show_banner()
        print(Fore.CYAN + f"\n🔑 API ID: {api_id}")
        print("\n1. 💣 ЗАПУСТИТЬ")
        print("2. 🔄 СМЕНИТЬ API")
        print("3. 📋 ПОМОЩЬ")
        print("0. 🚪 ВЫХОД\n")
        
        choice = input("👉 Выбери: ")
        
        if choice == "1":
            tokens = input_tokens()
            if tokens:
                group, msg, count, delay = input_group()
                await start_bots(api_id, api_hash, tokens, group, msg, count, delay)
        
        elif choice == "2":
            api_id, api_hash = get_api_credentials()
        
        elif choice == "3":
            show_banner()
            print(Fore.MAGENTA + "\n📋 ПОМОЩЬ")
            print("1. API ключи: my.telegram.org")
            print("2. Токены ботов: @BotFather")
            print("3. Боты должны быть админами в группе")
            input("\nНажми Enter...")
        
        elif choice == "0":
            bomb_animation()
            print(Fore.RED + "\nПока! 👋")
            break

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n⛔ Выход")
