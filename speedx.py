from pyrogram import Client
import asyncio
from colorama import Fore, Style, init

init(autoreset=True)

class MyTelegramBot:
    def __init__(self, api_id, api_hash):
        self.api_id = api_id
        self.api_hash = api_hash
        self.clients = []

    async def add_client(self):
        phone_number = input("Enter phone number: ")
        client = Client(phone_number, self.api_id, self.api_hash)
        await client.start()
        self.clients.append(client)

    async def get_chat_ids(self, client):
    chat_ids = []
    async for dialog in await client.get_dialogs():
        if str(dialog.chat.id).startswith('-'):
            chat_ids.append(dialog.chat.id)
    return chat_ids


    async def send_last_message_to_groups(self, client, timee, numtime, chat_ids):
        async for message in client.iter_history('me', limit=1):
            last_message = message.message_id

        for i in range(numtime):
            for chat_id in chat_ids:
                try:
                    await client.forward_messages(chat_id, "me", last_message)
                    print(f"{Fore.GREEN}Message sent to chat_id {chat_id}")
                    await asyncio.sleep(2)
                except Exception as e:
                    print(f"{Fore.RED}Failed to send message to chat_id {chat_id}: {e}")
                await asyncio.sleep(5)
            await asyncio.sleep(timee)

    async def join_group(self, client, chat_id):
        try:
            await client.join_chat(chat_id)
            print(f"{Fore.MAGENTA}Joined chat_id {chat_id}")
        except Exception as e:
            print(f"{Fore.RED}Failed to join chat_id {chat_id}: {e}")

    async def leave_chats(self, client, chat_ids):
        for chat_id in chat_ids:
            try:
                await client.leave_chat(chat_id)
                print(f"{Fore.CYAN}Left chat_id {chat_id}")
            except Exception as e:
                print(f"{Fore.RED}Failed to leave chat_id {chat_id}: {e}")

    async def run(self):
        while True:
            choice = int(input(
                f"{Style.BRIGHT}{Fore.YELLOW}1. Add Account\n2. AutoSender\n3. Auto Group Joiner\n4. Leave All Groups\n5. Exit\nEnter your choice: {Style.RESET_ALL}"
            ))

            if choice == 1:
                await self.add_client()

            elif choice == 2:
                for client in self.clients:
                    chat_ids = await self.get_chat_ids(client)
                    numtime = int(input("Enter the number of times to send the message: "))
                    timee = int(input("Enter the time delay in seconds: "))
                    await self.send_last_message_to_groups(client, timee, numtime, chat_ids)

            elif choice == 3:
                chat_id = input("Enter the Chat ID to join: ")
                for client in self.clients:
                    await self.join_group(client, chat_id)

            elif choice == 4:
                for client in self.clients:
                    chat_ids = await self.get_chat_ids(client)
                    await self.leave_chats(client, chat_ids)

            elif choice == 5:
                for client in self.clients:
                    await client.stop()
                break

if __name__ == "__main__":
    api_id = '22714655'  # Replace with your API ID
    api_hash = 'e218e19a476b75107fcfeac7dc94233d'  # Replace with your API Hash
    bot = MyTelegramBot(api_id, api_hash)
    asyncio.run(bot.run())
