import time
import json
from playwright.sync_api import sync_playwright
from additional_tools import parse_caption_tag,send_ai_request
import ast

parsed_reels = []
# reel_index = 1

def read_cookies():
    with open('cookies.txt','r') as f:
        cookies = f.read()
        return ast.literal_eval(cookies) #convert sting to list 
    
def write_cookies(cookies):
    with open('cookies.txt','w') as f:
        f.write(str(cookies))

def main_func():
    reel_index = 0
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='chrome',
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
                 "--disable-web-security"
            ]
            )
        # page = browser.new_page()

        context = browser.new_context(
            permissions=[ ],  # Allow media autoplay
            bypass_csp=True  # Relax CSP enforcement
        )
        page = context.new_page()
        cookies = read_cookies()
        context.add_cookies(cookies)
        print("going to page")
        page.goto('https://instagram.com/reels')
        
        print('waiting for page domcontentloaded')
        page.wait_for_load_state('domcontentloaded')

        while True:
            try:
                print('finding more')
                time.sleep(1)
                
                # page.wait_for_timeout(2000)  # Brief pause for scroll completion

                # get the current reel container
                current_reel = page.locator('div.x78zum5.xl56j7k.x1n2onr6.xh8yej3').nth(reel_index)

                # Then find the MORE button WITHIN this specific container
                more_button = current_reel.locator('span.xlej3yl:visible')
                more_button.click() #this expands the caption and tags
                
                #once the caption and tags are expanded extract the current_reel container again
                div_content = page.locator('div.x78zum5.xl56j7k.x1n2onr6.xh8yej3').nth(reel_index)

                #send the ai only the text from the current reel caption
                ai_response = send_ai_request(div_content.inner_text())
                print(div_content.inner_text())
                
                
                print(f'AI response = {ai_response}')
                ai_response = json.loads(ai_response)
                ai_response['reply'] = str(ai_response['reply']).lower()
                # input('continue?')
                
                if ai_response['reply'] == 'health' or ai_response['reply'] == 'motivation' or ai_response['reply'] == 'informational':
                    time.sleep(10)

                reel_index += 1
                # input('continue?')
                page.keyboard.press('ArrowDown')
                # time.sleep(1)
            except Exception as e:
                print(f'ERROR {e}')
                reel_index += 1
                page.keyboard.press('ArrowDown')
                # time.sleep(1)
        input('close?')
        write_cookies(context.cookies())


main_func()