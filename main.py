#!/usr/bin/env python3
# BOT SPAMER CLAN - MAIN.PY (ИСПРАВЛЕННАЯ ВЕРСИЯ)

import os
import sys
import time
import random
from colorama import Fore, init

init(autoreset=True)

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def show_banner():
    clear()
    print(Fore.RED + """
██████╗░░█████╗░███╗░░░███╗██████╗░
██╔══██╗██╔══██╗████╗░████║██╔══██╗
██████╦╝██║░░██║██╔████╔██║██████╦╝
██╔══██╗██║░░██║██║╚██╔╝██║██╔══██╗
██████╦╝╚█████╔╝██║░╚═╝░██║██████╦╝
╚═════╝░░╚════╝░╚═╝░░░░░╚═╝╚═════╝░
""" + Fore.CYAN + """
╔══════════════════════════════════════╗
║         BOT SPAMER CLAN v1.0         ║
║            by @DADILK                ║
╚══════════════════════════════════════╝
""")

def main_menu():
    show_banner()
    print(Fore.YELLOW + "ГЛАВНОЕ МЕНЮ:\n")
    print("1. 🚀 ЗАПУСТИТЬ БОМБАРДИРОВКУ")
    print("2. 📋 ИНСТРУКЦИЯ")
    print("3. 🧹 ОЧИСТИТЬ ЭКРАН")
    print("0. 🚪 ВЫХОД\n")
    
    choice = input("👉 Выбери пункт: ")
    return choice

def run_spam():
    show_banner()
    print(Fore.YELLOW + "⚙️ РЕЖИМ БОМБАРДИРОВКИ (в разработке)\n")
    print("Скоро здесь будет полный функционал с ботами!")
    input("\nНажми Enter, чтобы вернуться...")

def show_help():
    show_banner()
    print(Fore.MAGENTA + "📘 ИНСТРУКЦИЯ:\n")
    print("1. Получи API ID и HASH на my.telegram.org")
    print("2. Создай ботов через @BotFather")
    print("3. Добавь ботов в группу")
    print("4. Запусти атаку\n")
    input("Нажми Enter, чтобы вернуться...")

def main():
    while True:
        choice = main_menu()
        
        if choice == "1":
            run_spam()
        elif choice == "2":
            show_help()
        elif choice == "3":
            clear()
            print(Fore.GREEN + "✅ Экран очищен!")
            time.sleep(1)
        elif choice == "0":
            clear()
            print(Fore.RED + "Выход...")
            sys.exit(0)
        else:
            print(Fore.RED + "❌ Неверный выбор!")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n⛔ Выход по Ctrl+C")
        sys.exit(0)