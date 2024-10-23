from playwright.async_api import async_playwright
import asyncio
import re

class LinkedIn(object):
    def __init__(self):
        self.browser = None
        self.page = None

    async def login(self, username, password):
        await self.page.goto("https://www.linkedin.com/")
        
        await self.page.wait_for_load_state("domcontentloaded")

        await asyncio.sleep(2)
        
        # Type the Username
        await self.page.locator("//input[@id='session_key']").press_sequentially(username, delay=2)
        await asyncio.sleep(1)

        # Type the Password
        await self.page.locator("//input[@id='session_password']").press_sequentially(password, delay=2)
        await asyncio.sleep(1)

        # Click the Sign in button
        await self.page.get_by_role("button", name="Sign in").click()

        await self.page.wait_for_load_state("domcontentloaded")

        await asyncio.sleep(2)

        if "www.linkedin.com/feed/" in self.page.url:
            print("Successfully logged in. Homepage reached.")

    
    async def scrape_linkedin_post(self, url):
        await self.page.goto(url)
        await self.page.wait_for_load_state("load")

        while True:
            try:
                await self.page.locator("//button[@class='comments-comments-list__load-more-comments-button artdeco-button artdeco-button--muted artdeco-button--1 artdeco-button--tertiary ember-view']").click()
                await self.page.wait_for_load_state("domcontentloaded")
                await asyncio.sleep(1)
            except:
                break

        email_elements = await self.page.locator(
            "//article[contains(@class, 'comments-comment-item')]//a[contains(@href, 'mailto:')]"
        ).all()

        if email_elements:
            for elements in email_elements:
                email = await elements.text_content()
                print(email)

                names = await elements.locator(
                    "//ancestor::div[contains(@class, 'break-words')]//preceding-sibling::div[contains(@class, 'post-meta')]//div[contains(@class, 'profile-info-wrapper display-flex')]/a/h3/span[contains(@class, 'text-body-small-open')]/span[contains(@class, 'hoverable-link-text')]"
                ).text_content()
                print('Names:', names)

                descriptions_element = await elements.locator(
                    "//ancestor::div[contains(@class, 'break-words')]//preceding-sibling::div[contains(@class, 'post-meta')]//div[contains(@class, 'profile-info-wrapper display-flex')]/a/h3/span"
                ).all()
                descriptions = await descriptions_element[1].text_content()
                print('Descriptions:', descriptions)

                linkedin_links_elements = await elements.locator(
                "//ancestor::div[contains(@class, 'break-words')]//preceding-sibling::div[contains(@class, 'post-meta')]//a[contains(@class, 'actor-link')]"
                ).all()
                linkedin_links = [await link.get_attribute('href') for link in linkedin_links_elements]
                print('LinkedIn Links:', linkedin_links)

        else:
            print("No comments with emails found.")

    async def main(self):
        LinkedIn_client = LinkedIn()

        username = "aviralgautam472@gmail.com"
        password = "Aviral#281125"

        linkedin_post_url = 'https://www.linkedin.com/posts/chirag-d-tarwani_cfa-cfaexam-cfalevel1-activity-7109862664096378881-JcPa?utm_source=share&utm_medium=member_desktop'

        async with async_playwright() as p:
            LinkedIn_client.browser = await p.firefox.launch(headless = False)
            context = await LinkedIn_client.browser.new_context(
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0"
            )
            LinkedIn_client.page = await context.new_page()

            await LinkedIn_client.login(username, password)

            await LinkedIn_client.scrape_linkedin_post(linkedin_post_url)

            await asyncio.sleep(5)

        await LinkedIn_client.browser.close()

if __name__ == '__main__':
    asyncio.run(LinkedIn().main())
