import os
import asyncio
from pyrogram import Client, filters
from colorama import Fore, init, Style

init(autoreset=True)

# ========== ЦЕЛЬНЫЙ ASCII АРТ (без разрывов) ==========
BANNER = Fore.RED + Style.BRIGHT + """
██████╗░░█████╗░███╗░░░███╗██████╗░
██╔══██╗██╔══██╗████╗░████║██╔══██╗
██████╦╝██║░░██║██╔████╔██║██████╦╝
██╔══██╗██║░░██║██║╚██╔╝██║██╔══██╗
██████╦╝╚█████╔╝██║░╚═╝░██║██████╦╝
╚═════╝░░╚════╝░╚═╝░░░░░╚═╝╚═════╝░
""" + Fore.CYAN + Style.BRIGHT + """
╔══════════════════════════════════════╗
║     BOMB SPAMER CLAN v4.1 PREMIUM    ║
║         MULTI-BOT /bomb SPAM         ║
║            by @DADILK                ║
╚══════════════════════════════════════╝
""" + Fore.RESET

# ========== ФУНКЦИЯ ОЧИСТКИ ==========
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

# ========== ВВОД ТОКЕНОВ ==========
def input_tokens():
    clear_screen()
    print(BANNER)
    print(Fore.YELLOW + "ВВЕДИТЕ ТОКЕНЫ БОТОВ (каждый с новой строки)")
    print(Fore.GREEN + "Когда закончите, введите: end\n")
    
    tokens = []
    while True:
        token = input("🔑 Токен > ").strip()
        if token.lower() == "end":
            break
        if token:
            tokens.append(token)
            print(Fore.GREEN + f"✓ Токен {len(tokens)} добавлен")
    
    print(Fore.CYAN + f"\n✅ Всего ботов: {len(tokens)}")
    return tokens

# ========== НАСТРОЙКИ ГРУППЫ ==========
def input_group_settings():
    print(Fore.YELLOW + "\n⚙️ НАСТРОЙКИ АТАКИ:")
    print(Fore.WHITE + "(можно ввести username: @chat или ID: -1001234567890)")
    group_input = input("📢 Группа (username или ID): ").strip()
    
    # Если ввели цифровой ID (отрицательный для групп)
    if group_input.startswith('-') and group_input[1:].isdigit():
        group_id = int(group_input)
        print(Fore.GREEN + f"✓ Распознан ID группы: {group_id}")
    else:
        group_id = group_input  # оставляем как строку (username)
        print(Fore.GREEN + f"✓ Распознан username: {group_id}")
    
    message = input("💬 Текст сообщения для спама: ")
    count = int(input("🔢 Количество сообщений на бота: "))
    delay = float(input("⏱️ Задержка между сообщениями (сек, например 0.5): "))
    return group_id, message, count, delay

# ========== ЗАПУСК БОТОВ ==========
async def start_bots(tokens, group, message, count, delay):
    clear_screen()
    print(BANNER)
    print(Fore.RED + Style.BRIGHT + "💣 ЗАПУСК БОМБАРДИРОВКИ 💣\n")
    
    active_bots = []
    
    for i, token in enumerate(tokens):
        try:
            # Создаём клиента для каждого бота
            app = Client(f"bot_{i}", api_id=None, api_hash=None, bot_token=token, in_memory=True)
            await app.start()
            
            # Получаем информацию о боте
            me = await app.get_me()
            print(Fore.GREEN + f"[✓] Бот @{me.username} запущен")
            
            # Подключаем обработчик команды /bomb
            @app.on_message(filters.command("bomb") & filters.group)
            async def bomb_handler(client, msg):
                chat_id = msg.chat.id
                chat_title = msg.chat.title
                print(Fore.RED + f"[💥] @{me.username} получил команду в {chat_title}")
                
                for j in range(count):
                    try:
                        await client.send_message(chat_id, f"{message} [#{j+1}]")
                        print(Fore.GREEN + f"    [✓] {j+1}/{count} от @{me.username}")
                        await asyncio.sleep(delay)
                    except Exception as e:
                        print(Fore.RED + f"    [!] Ошибка: {e}")
                        break
            
            active_bots.append(app)
            print(Fore.CYAN + f"    👂 Бот слушает команду /bomb в группах\n")
            
        except Exception as e:
            print(Fore.RED + f"[✗] Ошибка запуска бота {i+1}: {e}")
    
    print(Fore.MAGENTA + Style.BRIGHT + f"\n✅ АКТИВНО БОТОВ: {len(active_bots)}")
    print(Fore.YELLOW + "🔥 Теперь добавь ботов в группы и пиши /bomb")
    print(Fore.RED + "⛔ Нажми Ctrl+C для остановки\n")
    
    # Держим ботов в работе
    try:
        await asyncio.gather(*(app.idle() for app in active_bots))
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n⛔ Остановка ботов...")
        for app in active_bots:
            await app.stop()

# ========== ГЛАВНОЕ МЕНЮ ==========
async def main():
    while True:
        clear_screen()
        print(BANNER)
        print(Fore.CYAN + "ГЛАВНОЕ МЕНЮ:\n")
        print("1. 💣 ЗАПУСТИТЬ БОМБАРДИРОВКУ (ввод токенов)")
        print("2. 📋 ИНСТРУКЦИЯ (как получить токены)")
        print("3. 🧹 ОЧИСТИТЬ ЭКРАН")
        print("0. 🚪 ВЫХОД\n")
        
        choice = input("👉 Выбери пункт: ")
        
        if choice == "1":
            tokens = input_tokens()
            if not tokens:
                print(Fore.RED + "❌ Нет токенов!")
                await asyncio.sleep(1)
                continue
            
            group, message, count, delay = input_group_settings()
            await start_bots(tokens, group, message, count, delay)
            
        elif choice == "2":
            clear_screen()
            print(Fore.MAGENTA + Style.BRIGHT + "📘 ИНСТРУКЦИЯ:\n")
            print("1. Напиши @BotFather в Telegram")
            print("2. Отправь /newbot и создай бота")
            print("3. Скопируй токен (вида 123456:ABCdef...)")
            print("4. Повтори для нужного количества ботов")
            print("5. Добавь ботов в группу (дай права администратора!)")
            print("6. Введи токены в программу и настрой атаку")
            print("7. В группе напиши /bomb — начнётся ад!\n")
            input("Нажми Enter, чтобы вернуться...")
            
        elif choice == "3":
            clear_screen()
            print(Fore.GREEN + "✅ Экран очищен!")
            await asyncio.sleep(1)
            
        elif choice == "0":
            clear_screen()
            print(Fore.RED + "Выход... Пока!")
            break

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n⛔ Выход по Ctrl+C")
