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
    reel_index = 1
    with sync_playwright() as p:
        browser = p.firefox.launch(
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
                page.click('span.xlej3yl.x1rg5ohu.xdl72j9.x1c4vz4f.x2lah0s.xsgj6o6',timeout=1000)
                # exists = False
                # try:
                #     page.locator('span.xlej3yl.x1rg5ohu.xdl72j9.x1c4vz4f.x2lah0s.xsgj6o6').is_visible(timeout=100)
                #     exists = True
                #     print("More button found")
                # except:
                #     exists = False
                #     print("NOT FOUND!!")

                # if exists:
                #     page.click('span.xlej3yl.x1rg5ohu.xdl72j9.x1c4vz4f.x2lah0s.xsgj6o6')
                #     print('clicked more')

                time.sleep(0.5)
                # print('inner text - ')
                # print(page.inner_text('div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1emribx.x1uhb9sk.x1iyjqo2.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1.x2lwn1j.xeuugli.x6ikm8r.x10wlt62.x1d8287x.xrok2fi.xz4gly6'))

                inner_html = page.inner_html(f'div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1emribx.x1uhb9sk.x1iyjqo2.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1:nth-of-type({reel_index})')
                # print("INNER HTML - ", inner_html)
                parsed_caption = parse_caption_tag(inner_html)
                print(f'Parsed html = \n{parsed_caption}')
                reel_index += 1
                # print("INNER TExT - ",inner_text)
                # input('close?')
                

                ai_response = send_ai_request(parsed_caption)
                print(f'AI response = {ai_response}')
                


                page.keyboard.press('ArrowDown')
                input('continue?')
                time.sleep(1)
            except Exception as e:
                print(e)
                page.keyboard.press('ArrowDown')
                time.sleep(1)
        input('close?')
        write_cookies(context.cookies())


main_func()