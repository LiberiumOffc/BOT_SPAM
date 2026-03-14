import os
import asyncio
from pyrogram import Client
from colorama import Fore, init, Style

init(autoreset=True)

# Функция очистки экрана
def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

# Главное меню
def show_menu():
    clear_screen()
    print(Fore.GREEN + Style.BRIGHT + r"""
╔══════════════════════════════════════╗
║     BOT SPAMER CLAN v3.0 PREMIUM     ║
║         by @DADILK (LEDIAN)          ║
╠══════════════════════════════════════╣
║ [1] 🚀 Запустить спам (один бот)     ║
║ [2] 🤖 Многопоточный спам (неск. ботов)║
║ [3] 📋 Инструкция (API/токен)         ║
║ [4] 🧹 Очистить экран                  ║
║ [0] ⬅️ Выход                           ║
╚══════════════════════════════════════╝
""")

# Функция спама с одним ботом
async def spam_single():
    clear_screen()
    print(Fore.YELLOW + "⚙️ Настройка одного бота:\n")
    api_id = int(input("API ID: "))
    api_hash = input("API HASH: ")
    bot_token = input("Токен бота: ")
    group = input("Username группы (например @chat): ")
    msg = input("Текст сообщения: ")
    count = int(input("Количество: "))
    delay = float(input("Задержка (сек): "))

    app = Client("spam_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
    await app.start()
    try:
        chat = await app.get_chat(group)
        for i in range(count):
            await app.send_message(chat.id, f"{msg} [#{i+1}]")
            print(Fore.GREEN + f"[✓] {i+1}/{count} отправлено")
            await asyncio.sleep(delay)
    except Exception as e:
        print(Fore.RED + f"[!] Ошибка: {e}")
    finally:
        await app.stop()
    input(Fore.CYAN + "\nНажми Enter, чтобы вернуться в меню...")

# Заглушка для многопоточности
async def spam_multi():
    clear_screen()
    print(Fore.YELLOW + "⚙️ Многопоточный спам (в разработке)")
    print("Скоро: спам через несколько ботов одновременно")
    input(Fore.CYAN + "\nНажми Enter, чтобы вернуться в меню...")

# Инструкция
def show_help():
    clear_screen()
    print(Fore.MAGENTA + Style.BRIGHT + "📘 ИНСТРУКЦИЯ:\n")
    print("1. API ID и HASH: https://my.telegram.org")
    print("2. Токен бота: @BotFather -> /newbot")
    print("3. Группа: юзернейм группы или ссылка")
    print("4. Задержка: рекомендуется 0.5-2 сек\n")
    input("Нажми Enter, чтобы вернуться...")

# Основной цикл
async def main():
    while True:
        show_menu()
        choice = input(Fore.CYAN + "Выбери пункт: ")

        if choice == "1":
            await spam_single()
        elif choice == "2":
            await spam_multi()
        elif choice == "3":
            show_help()
        elif choice == "4":
            clear_screen()
            print(Fore.GREEN + "✅ Экран очищен!")
            await asyncio.sleep(1)
        elif choice == "0":
            clear_screen()
            print(Fore.RED + "Выход...")
            break
        else:
            print(Fore.RED + "Неверный ввод!")
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
