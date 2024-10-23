from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

with sync_playwright() as p:
    browser = p.chromium.launch(headless = False, slow_mo =50)
    page = browser.new_page()
    page.goto('https://github.com/login')
    page.fill('input#login_field', 'aviralgautam472@gmail.com')
    page.fill('input#password', 'Aviral#281125')
    page.click('input[type = submit]')
    html = page.inner_html('#dashboard') # "#" is used for selecting the div->id tag
    soup = BeautifulSoup(html, 'html.parser')
    h1 = soup.find('h1', {'class':'sr-only'}).text
    print(f'h1 = {h1}')