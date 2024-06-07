import asyncio
from dotenv import load_dotenv
from database import init_db
from screens import StartScreen


load_dotenv()
init_db()



async def main():

    screen = StartScreen()
    screen.render()
    while True:
        user_input = input().strip().lower()

        if user_input in screen:
            screen = await screen(user_input)
            screen.render()
        else:
            print('Такой команды нет')

if __name__ == "__main__":
    asyncio.run(main())
