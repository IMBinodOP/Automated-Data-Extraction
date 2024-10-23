from playwright.async_api import async_playwright, expect
import pandas as pd
import io, json, re
import logging, asyncio


class ChatGPT(object):
    def __init__(self):
        self.browser = None
        self.page = None
        self.conversation_id = 3
        self.resume_data = []
        self.__candidate_info = None
        self.query = """Write Python Code to print fibonacci series upto 12000"""

    async def login(self, username, password):
        await self.page.goto("https://chat.openai.com/auth/login")
        await asyncio.sleep(2)

        await self.page.get_by_test_id("login-button").click()
        await asyncio.sleep(2)

        await self.page.wait_for_load_state("domcontentloaded")
        await asyncio.sleep(2)

        # Enter the username.
        await self.page.get_by_label('Email address').fill(username)
        await asyncio.sleep(1)

        await self.page.get_by_role("button", name="Continue", exact=True).click()
        await asyncio.sleep(3)

        await self.page.wait_for_load_state("domcontentloaded")
        await asyncio.sleep(2)

       # Enter the username.
        await self.page.get_by_label('Password').fill(password)
        await asyncio.sleep(1)

        await self.page.get_by_role("button", name="Continue", exact=True).click()
        await asyncio.sleep(3)

        await self.page.wait_for_load_state("domcontentloaded")
        await asyncio.sleep(5)

        logging.info('Login Successful')

    async def new_chat(self):
        # Delete old chat to start new chat
        await self.page.locator("//nav[@aria-label='Chat history']/div[2]/div[2]/div/span/div/ol[1]/li[1]/div/div/button").click()
        await asyncio.sleep(1)

        await self.page.locator("//div[@role='menuitem' and text() = 'Delete chat']").click()
        await asyncio.sleep(2)

        await self.page.locator("//button[./div[text()='Delete']]").click()
        await asyncio.sleep(2)

        await self.page.wait_for_load_state('networkidle')
        await asyncio.sleep(2)

        self.conversation_id = 3

    async def send_chat(self):
        prompt = self.query
        try:
            await self.page.evaluate('''(prompt) => {
                const inputField = document.querySelector('#prompt-textarea');
                inputField.value = prompt;
                inputField.dispatchEvent(new Event('input', { bubbles: true }));
            }''', prompt)

            await self.page.get_by_test_id("send-button").click()
            await asyncio.sleep(2)

            await self.page.wait_for_load_state('networkidle')
            await asyncio.sleep(1)

            await expect(self.page.get_by_test_id(f"conversation-turn-{self.conversation_id}").locator("//pre//code/span[text()='}']")).to_be_visible()
            span = await self.page.get_by_test_id(f"conversation-turn-{self.conversation_id}").locator("//pre//code/span").all()
            data = "".join([await item.text_content() for item in span])
            
            logging.info(data)
            return True
        
        except Exception as e:
            logging.error(e)
            await asyncio.sleep(2)
            return False


async def main():
    chatgpt_client = ChatGPT()

    username = "your email address"
    password = "your password"

    logging.info(f'Launching Browser...')
    async with async_playwright() as p:
        chatgpt_client.browser = await p.firefox.launch(headless=False)
        context = await chatgpt_client.browser.new_context(
            user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"
        )
        chatgpt_client.page = await context.new_page()
        
        await chatgpt_client.login(username, password)
        
        chat_status = await chatgpt_client.send_chat()
        await asyncio.sleep(30)
        
        logging.info(f'Closing Browser...')
        await chatgpt_client.browser.close()


if __name__ == '__main__':
    asyncio.run(main())

