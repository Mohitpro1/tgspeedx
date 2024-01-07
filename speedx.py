
import asyncio
from pyrogram import Client
from colorama import Fore, Style, init

init(autoreset=True)

async def get_chat_ids(app):
    chat_ids = []
    async for dialog in app.get_dialogs():
        if str(dialog.chat.id).startswith('-'):
            chat_ids.append(dialog.chat.id)
    return chat_ids

async def send_last_message_to_groups(app, timee, numtime, chat_ids):
    async for message in app.get_chat_history('me', limit=1):
        last_message = message.id

    for _ in range(numtime):
        for chat_id in chat_ids:
            try:
                await app.forward_messages(chat_id, "me", last_message)
                print(f"{Fore.GREEN}Message sent to chat_id {chat_id}")
            except Exception as e:
                print(f"{Fore.RED}Failed to send message to chat_id {chat_id}: {e}")
            await asyncio.sleep(2)
        await asyncio.sleep(timee)

async def leave_chats(app, chat_ids):
    for chat_id in chat_ids:
        try:
            await app.leave_chat(chat_id)
            print(f"{Fore.CYAN}Left chat_id {chat_id}")
        except Exception as e:
            print(f"{Fore.RED}Failed to leave chat_id {chat_id}: {e}")

async def join_group(app, chat_id):
    try:
        await app.join_chat(chat_id)
        print(f"{Fore.MAGENTA}Joined chat_id {chat_id}")
    except Exception as e:
        print(f"{Fore.RED}Failed to join chat_id {chat_id}: {e}")

async def handle_clients(api_id, api_hash, accounts):
    clients = [Client(f"my_account_{account}", api_id, api_hash, phone_number=account) for account in accounts]
    for client in clients:
        await client.start()

    while True:
        a = int(input(f"{Style.BRIGHT}{Fore.YELLOW}1. Scrape Group List\n2. AutoSender\n3. Auto Group Joiner\n4. Leave all groups\n5. Exit\nEnter the choice: {Style.RESET_ALL}"))

        if a == 1:
            for client in clients:
                chat_ids = await get_chat_ids(client)
                print(f"{Fore.CYAN}Group IDs for {client.phone_number}: {chat_ids}")

        elif a == 2:
            numtime = int(input("How many times you want to send the message: "))
            timee = int(input("Enter the time delay: "))
            for client in clients:
                chat_ids = await get_chat_ids(client)
                await send_last_message_to_groups(client, timee, numtime, chat_ids)

        elif a == 3:
            chat_id = input("Enter the Chat ID to join: ")
            for client in clients:
                await join_group(client, chat_id)

        elif a == 4:
            for client in clients:
                chat_ids = await get_chat_ids(client)
                await leave_chats(client, chat_ids)

        elif a == 5:
            for client in clients:
                await client.stop()
            break

async def main():
    api_id = int(input("Enter api id: "))
    api_hash = input("Enter api_hash: ")
    num_accounts = int(input("Enter the number of accounts: "))
    accounts = [input(f"Enter phone number for account {i+1}: ") for i in range(num_accounts)]
    
    await handle_clients(api_id, api_hash, accounts)

if __name__ == "__main__":
    asyncio.run(main())
