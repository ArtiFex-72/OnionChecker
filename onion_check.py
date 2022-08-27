import requests
from bs4 import BeautifulSoup
import os
import time
import threading
import datetime
import asyncio
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

proxies = {
    'http': 'socks5h://localhost:9150',
    'https': 'socks5h://localhost:9150'
}

is_there_a_bot = False

alarm_link = "none"

def handling_bot():
    mytoken = ""
    #mypassw = ""
    the_id = ""
    with open("bot_token.txt", 'r') as f:
        mytoken = f.read(100)
        f.close()
    #with open("bot_passw.txt", 'r') as f:
    #    mypassw = f.read(100)
    #    f.close()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    the_id = ""
    TOKEN = mytoken
    with open("owner_id.txt", 'r') as f:
        the_id = f.read(40)
        f.close()

    bot = Bot(token=TOKEN)
    dp = Dispatcher(bot)


    #@dp.message_handler(commands=['hell'])
    #async def process_start_command(message: types.Message):
        #await message.reply("Oh, master, it's you! I'm at your service.")
    #    await message.reply("I know")
    #    print(msg.from_user.id)

    

    def check_activity():

        interval = 0.0
        content = "default"
        bNeedClearing = False

        async def gg():
            id = the_id
            msg = "I have done that"
            await bot.send_message(id, alarm_link)

        with open("interval.txt", "r") as f:
            interval = float(f.read(100))
            f.close()
        while True:
            
            with open("active_links.txt", "r") as f:
                if f.read(300):
                    content = f.read(300)
                    bNeedClearing = True
                    f.close()
                else:
                    f.close()
            if bNeedClearing:
                open("active_links.txt", 'w').close()
                with open("bot_passw.txt", "r") as file:
                    varo = (file.read(500))
                    alarm_link = varo
                    file.close
                asyncio.run(gg())
            bNeedClearing = False
            time.sleep(interval)


    #fourth_thread = threading.Thread(target=check_activity, args=())
    #fourth_thread.start()
    #@dp.message_handler(commands=['help'])
    #async def process_help_command(message: types.Message):
    #    await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")


    @dp.message_handler()
    async def echo_message(msg: types.Message):
        if msg.text == mypassw:
            await bot.send_message(msg.from_user.id, "When programm is running, I will send you all available links.")
            the_id = msg.from_user.id
            #await bot.send_message(msg.from_user.id, the_id)
            with open("owner_id.txt", "w") as f:
                f.write(str(the_id))
                f.close()
        else:
            await bot.send_message(msg.from_user.id, mypassw)


    if __name__ == '__main__':
        loop = asyncio.get_event_loop()
        loop.create_task(check_activity())
        executor.start_polling(dp, skip_updates=True)

def search():

    interval = 0.0
    with open("interval.txt", "r") as f:
        interval = float(f.read(100))
        f.close()
    while True:
    
        can_run = True
        #print("Tor Connection Check")
        try:
            system_ip = requests.get('https://ident.me', proxies=proxies).text
            tor_ip_list = requests.get('https://check.torproject.org/exit-addresses').text
            if system_ip in tor_ip_list:
                print('Tor_IP: ', system_ip)
                print("Tor Connection Success ")
        except Exception as ex:
            print("\n\nError: Configure Tor as service")
            print("For quick setup refer: https://miloserdov.org/?p=1839")
            #exit()
            can_run = False
            print("Error text: ")
            print(ex)
            #ans = input("\n\nTry again? (y/n): ")

        now = datetime.datetime.now()
        current_time = str('(' + str(now.day) + '.' + str(now.month) + '.' + str(now.year) + ') '+ str(now.hour)+ ':'+ (str(now.minute) if (now.minute>9) else ('0'+ str(now.minute)))+ ':'+ (str(now.second) if (now.second>9) else ('0'+ str(now.second))))
        # 2015 5 6 8 53 40
        
        if can_run:

            #Submit a text file containing an onion URL in a line

            #in_file = input("Submit the URL File: ")
            in_file = 'D:\CurrentProject\OnionCheckRelease\\urls.txt'

            input_file = open(in_file, 'r')

            for url in input_file:

                url = url.rstrip('\n')
                try:
                    data = requests.get(url, proxies=proxies)
                except:
                    data = 'error'
                if data != 'error':
                    status = 'Active'
                    status_code = data.status_code
                    soup = BeautifulSoup(data.text, 'html.parser')
                    page_title = str(soup.title)
                    page_title = page_title.replace('<title>', '')
                    page_title = page_title.replace('</title>', '')
                elif data == 'error':
                    status = "Inactive"
                    status_code = 'NA'
                    page_title = 'NA'
                current_link = str(str(current_time)+': '+str(url)+': '+str(status)+': '+str(status_code)+': '+str(page_title)+'\n')
                if status == "Active":
                    with open("bot_passw.txt", 'w') as f:
                        #f.write(current_time+': '+url+': '+status+': '+status_code+': '+page_title+'\n')
                        f.write(current_link)
                        f.close()
                    with open("active_links.txt", "a") as f:
                        #f.write(current_time+': '+url+': '+status+': '+status_code+': '+page_title+'\n')
                        f.write("trigger")
                        f.close()
                with open("results.txt", "a") as f:
                    #f.write(current_time+': '+url+': '+status+': '+status_code+': '+page_title+'\n')
                    f.write(current_link)
                    f.close()
                #print(url, ': ', status, ': ', status_code, ': ', page_title)
                #if status == 'Inactive':
                #    print('INACTIVE')
                #ans = input("Start again? (y/n): ")
            time.sleep(interval)

def create_bot():
    with open("bot_check.txt", 'r') as f:
        is_there_a_bot = bool(f.read(40))
        f.close()
    if is_there_a_bot == True:
        answ = input("You already have a bot. Do you really want to delete it and create a new one? (y/n): ")
        if answ == 'y':
            print("OK...")
        else:
            return None
    token = input("If you want to receive notifications from your own loyal assistant, create a telegram-bot with famous @BotFather and paste here it's access token: ")
    passw = input("Alright, if you have entered a correct token, this will work (I hope so). Now enter your telegram id: ")
    with open("bot_token.txt", "w") as f:
        f.write(token)
        f.close()
    with open("owner_id.txt", "w") as f:
        f.write(passw)
        f.close()
    third_thread = threading.Thread(target=handling_bot, args=())
    third_thread.start()
    with open("bot_check.txt", 'w') as f:
        f.write("True")
        f.close()
    print("Restart the program to activate the new bot. Then select the '(4) Check_for_a_bot' option in main menu to make sure the bot is working.")

def main():
    
    with open("bot_check.txt", 'r') as f:
        is_there_a_bot = bool(f.read(40))
        f.close()

    if is_there_a_bot == True:
        third_thread = threading.Thread(target=handling_bot, args=())
        third_thread.start()

    def sett():
        print("\nNow you can set up parameters of your checking thread, and then it will work automatically.\nEnter a number of command\n")
        while True:
            print("\nAvailable commands:\n    (1) Add_new_url\n    (2) Clear_urls\n    (3) See_target_urls\n    (4) Edit_schedule\n    (5) Done (save and quit to main menu)\n")
            try:
                command = int(input("Enter the number of your next command: "))
            except:
                print("\n(!) YOU CAN ONLY ENTER INTEGER NUMBERS")
                continue
            if command == 1:
                url = input("New target's url: ")
                with open("urls.txt", "a") as f:
                    f.write('\n' + url)
                    f.close()
            elif command == 2:
                open('urls.txt', 'w').close()
                print("Urls have been deleted.")
            elif command == 3:
                with open("urls.txt", "r") as file:
                    print("\n" + file.read(500))
                    file.close
            elif command == 4:
                a = 488
                while True:
                    try:
                        a = int(input("How many times per hour I must check your targets? (Enter a positive integer number from 1 to 120): "))
                    except:
                        print("\n(!) You can enter only a positive integer number from 1 to 120.")
                        continue
                    if (isinstance(a, int)) & (a > 0) & (a < 121):
                        break
                    else:
                        print("\n(!) You can enter only a positive integer number from 1 to 120.")
                        continue
                value = 3600.0 // float(a)
                with open("interval.txt", "w") as f:
                    f.write(str(value))
                    f.close()
                #with open("interval.txt", "r") as fr:
                #    print(float(fr.read(10)))
                #    fr.close()
            elif command == 5:
                break
            else:
                print("\n(!) YOU CAN ONLY ENTER COMMAND NUMBERS (from 1 to 5).")

    def main_menu():
        print("Welcome, stranger!")
        while True:
            print("\nAvailable commands:\n    (1) Start\n    (2) Settings\n    (3) Set up a telegram-bot\n    (4) Check_for_a_bot\n    (5) See_results\n    (6) Help\n")
            try:
                command = int(input("Enter the number of your next command: "))
            except:
                print("\n(!) YOU CAN ONLY ENTER INTEGER NUMBERS")
                continue
            if command == 1:
                print("Starting...")
                second_thread = threading.Thread(target=search, args=())
                second_thread.start()
                print("Checking process has been successfully started. You can see results in the 'results' file")
            elif command == 2:
                sett()
            elif command == 3:
                create_bot()
            elif command == 4:
                print("\nIf the bot is created and configured correctly, it will now send you the message 'I am ready to go'.")
                cmsg = 'I am ready to go'
                with open("bot_passw.txt", "w") as file:
                    file.write(cmsg)
                    file.close()
                with open("active_links.txt", 'w') as file:
                    file.write("trigger")
                    file.close()
            elif command == 5:
                with open("results.txt", "r") as file:
                    print("\n" + file.read(1000000))
                    file.close
            elif command == 6:
                with open("Manual.txt", "r") as file:
                    print("\n" + file.read(2000))
                    file.close
            else:
                print("\n(!) YOU CAN ONLY ENTER COMMAND NUMBERS (from 1 to 5).")
    
    main_menu()
    search()

if __name__ == "__main__":
    
    main()