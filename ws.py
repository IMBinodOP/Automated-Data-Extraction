from playwright.sync_api import sync_playwright
import json
import pandas as pd
import pygsheets
from google.oauth2 import service_account

def authenticate_google_sheets():
    # Load Google Sheets credentials
    credentials = {
        "type": "service_account",
        "project_id": "careervira-408510",
        "private_key_id": "b7ce710561227525840a953e0237c5d137f9caae",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCeOtIz355n2CA6\naDscpRUUmC2zwUj2hd5fVo4hsbVeDnvfrRq3VU73Ugf1BCjzBWQQCPciLn10xe8I\n7Tjtx51gSCcD4STlC5p34AAXG3agC5+rdo7q9+kZ2w8DoZAr8axmGNt5qAucghzR\nrghJqk+2avCFIsZV05GB64p1NX7gM+h51uOgQi2Rm/zv3HORe+vAH87VzXoFlB0s\nCrWshMMD+Znb45atUsl0NSDU4MSulhVXu0Z7ZwMB8HU4jADvDt2o313kOifUqd3g\nGoCM4IDsfsL+SEppXVW+3okpelCKg+EgsV7qPQdDPNQiG2E51mapTnpzXlFj1hdl\nPWbd3Sc7AgMBAAECggEAAPRqIPQAI3eafp+6KOqkwOtkX6YSlhP/J2RWa+FnZ4hw\n1yE6mUMKoCj3jcTQGf9LVH7FzE8dD1iK2Qd/L+LHdcPSk//4Vj5cA3h9xBe0qd5W\nTxVUKlN1Sg77xFH0BmqFrQFeDv2ICNlkIudQCURr7LX30AJJmL+lgazZKnj/m1IL\nUlY1Fyffn7ZAsri1guCzQtNIWZOW0SOceUOYmyW/n2aIIcI3MuEBq7y6tOmNLFQi\nwldorSNQk+Yw5ZFMRBuuIaizYTJ911M1ATNtnUXLPKd4FTX1z5cesCCMSAphHl6G\naE+gRSbO49pnhqJ0/Jo6iL8BKr5LMumLaXSJKC9FOQKBgQDN7/kaQbVmjm78MIta\nyxIII4zyaEUFZu0mW6lUUy6+IiRh0ObrlSEpC41hGbzFVlU5cwjyagUmUaEZ8WqK\nwzTaA/KHMwHhDKsYtO1B6RCRpUJPefO5fufkIBmW0uvtkGlo7QGQZLEK0Vba55qj\n40kPTzBocFzSA4ieXZ7hqHaWJwKBgQDEseB1jRy1cSpKtVe1IaDTclu4jcwaYRcj\na2q+Thnj6dxtTJQJjLtgfBro5DCHqIsbK7oV2pO//m6ibetDDb9jhgglqnhFB59S\nLPuEPw+x2PEF0IxxIDxLeyeohCnw16nmN7FxzbbUYhlNXJvi/bj8hTbxTYPfaeQ+\nn1qnRM4GzQKBgQDEm55Omvz8dG8xBYeFnuoQKyCdLT738VPnkwsOHnw5uY7SdAaC\nU1XdQdIwKco2/D1RI6ofBWj1NGmBwyHcaJFEsxAQU3ovyVBvvgvlKQVQh13PUraF\nGct518uWWrgzjfOU4PDlUbxUf5dUVlkkrhFKNGgazWtQdV8xEmBlP9g3cQKBgEqg\ndloDRQ4uNm6L6RAHBz7SV6xo2DR1+9Jrcd9sQHRxiTlK4avR4lHUJF2SHjuKHeUc\nLQkXmhExFoa4D5esQp4e/z5TNDh0kOUbvf3J80l11tRu8KoHIfk9a6mLI2KGYKbB\nIKjd9O0VnyXz6g0wWJwuas8Yqtz8DyYXTczC1SxNAoGBAIyhaciT/A2dGsiaJXMh\nEow5i3r4bB34UJAkdQzV8TtorGdlYYQaU5YrDAvO9InZwhDB4vIYw37FTu+7/RxJ\nIdrpBNyPd/gaZjLJfSzT2idzV3FS+XTvXQU6JQ5gNyU5zQOB7TDQkiOCK7OCujg+\nxeHUA2PmSWkcfQjo0V4iE/HW\n-----END PRIVATE KEY-----\n",
        "client_email": "aviral@careervira-408510.iam.gserviceaccount.com",
        "client_id": "104491109567605195141",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/aviral%40careervira-408510.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }
    
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    service_account_info = json.loads(json.dumps(credentials))
    my_credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
    
    gc = pygsheets.authorize(custom_credentials=my_credentials)

    # Assuming you want to append data to the first sheet in the workbook
    sheet = gc.open('LinkedIn').sheet1
    return sheet

def scrape_linkedin_post(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        page = context.new_page()

        page.goto(url)

        names_elements = page.query_selector_all('//a[@class="text-sm link-styled no-underline leading-open comment__author truncate pr-6"]')
        names = [name.text_content().strip() for name in names_elements]

        email_elements = page.query_selector_all('//a[contains(text(), "@")]')
        emails = [email.text_content() for email in email_elements]

        descriptions_elements = page.query_selector_all('//p[@class="!text-xs text-color-text-low-emphasis leading-[1.33333] mb-0.5 truncate comment__author-headline"]')
        descriptions = [desc.text_content() for desc in descriptions_elements]

        linkedin_links_elements = page.query_selector_all('//a[@class="text-sm link-styled no-underline leading-open comment__author truncate pr-6"]')
        linkedin_links = [link.get_attribute('href') for link in linkedin_links_elements]

        browser.close()

        data = {'Name': names, 'Email': emails, 'Description': descriptions, 'LinkedIn Link': linkedin_links}
        df = pd.DataFrame(data)

        sheet = authenticate_google_sheets()

        # Append data to the existing sheet
        sheet.set_dataframe(df, start='A1', copy_head=False, fit=True)

linkedin_post_url = 'https://www.linkedin.com/posts/chirag-d-tarwani_cfa-cfaexam-cfalevel1-activity-7109862664096378881-JcPa?utm_source=share&utm_medium=member_desktop'
scrape_linkedin_post(linkedin_post_url)
