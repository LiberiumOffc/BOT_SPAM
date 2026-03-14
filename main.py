import os
import asyncio
from pyrogram import Client, filters
from colorama import Fore, init, Style

init(autoreset=True)

# ========== ЦЕЛЬНЫЙ ASCII АРТ ==========
BANNER = Fore.RED + Style.BRIGHT + """
██████╗░░█████╗░███╗░░░███╗██████╗░
██╔══██╗██╔══██╗████╗░████║██╔══██╗
██████╦╝██║░░██║██╔████╔██║██████╦╝
██╔══██╗██║░░██║██║╚██╔╝██║██╔══██╗
██████╦╝╚█████╔╝██║░╚═╝░██║██████╦╝
╚═════╝░░╚════╝░╚═╝░░░░░╚═╝╚═════╝░
""" + Fore.CYAN + Style.BRIGHT + """
╔══════════════════════════════════════╗
║     BOMB SPAMER CLAN v4.2 PREMIUM    ║
║         MULTI-BOT /bomb SPAM         ║
║            by @DADILK                ║
╚══════════════════════════════════════╝
""" + Fore.RESET

# ========== ФУНКЦИЯ ОЧИСТКИ ==========
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

# ========== ПОЛУЧЕНИЕ API ДАННЫХ ==========
def get_api_credentials():
    clear_screen()
    print(BANNER)
    print(Fore.YELLOW + "🔑 НАСТРОЙКА API ДОСТУПА (нужно сделать 1 раз)\n")
    print("1. Зайди на https://my.telegram.org")
    print("2. Войди в аккаунт")
    print("3. Создай приложение (APP)")
    print("4. Скопируй API ID и API HASH\n")
    
    api_id = input("👉 Введите API ID (число): ").strip()
    api_hash = input("👉 Введите API HASH (строка): ").strip()
    
    # Сохраняем в файл для следующих запусков
    with open("api_config.txt", "w") as f:
        f.write(f"{api_id}\n{api_hash}")
    
    print(Fore.GREEN + "\n✅ API данные сохранены в api_config.txt")
    return int(api_id), api_hash

# ========== ЗАГРУЗКА API ДАННЫХ ==========
def load_api_credentials():
    try:
        with open("api_config.txt", "r") as f:
            lines = f.readlines()
            api_id = int(lines[0].strip())
            api_hash = lines[1].strip()
            return api_id, api_hash
    except:
        return None, None

# ========== ВВОД ТОКЕНОВ БОТОВ ==========
def input_tokens():
    clear_screen()
    print(BANNER)
    print(Fore.YELLOW + "🤖 ВВЕДИТЕ ТОКЕНЫ БОТОВ (каждый с новой строки)")
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
        group_id = group_input
        print(Fore.GREEN + f"✓ Распознан username: {group_id}")
    
    message = input("💬 Текст сообщения для спама: ")
    count = int(input("🔢 Количество сообщений на бота: "))
    delay = float(input("⏱️ Задержка между сообщениями (сек, например 0.5): "))
    return group_id, message, count, delay

# ========== ЗАПУСК БОТОВ ==========
async def start_bots(api_id, api_hash, tokens, group, message, count, delay):
    clear_screen()
    print(BANNER)
    print(Fore.RED + Style.BRIGHT + "💣 ЗАПУСК БОМБАРДИРОВКИ 💣\n")
    
    active_bots = []
    
    for i, token in enumerate(tokens):
        try:
            # ВАЖНО: Теперь передаём api_id и api_hash
            app = Client(
                f"bot_session_{i}",
                api_id=api_id,
                api_hash=api_hash,
                bot_token=token,
                in_memory=True
            )
            
            await app.start()
            
            # Получаем информацию о боте
            me = await app.get_me()
            print(Fore.GREEN + f"[✓] Бот @{me.username} (ID: {me.id}) запущен")
            
            # Подключаем обработчик команды /bomb
            @app.on
