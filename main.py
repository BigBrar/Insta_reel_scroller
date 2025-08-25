import time
from playwright.sync_api import sync_playwright
from additional_tools import send_ai_request
from handle_comments import open_comments, extract_comments
import ast

parsed_reels = []
browser_args = [
                "--disable-blink-features=AutomationControlled",
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
                 "--disable-web-security"
            ]
# reel_index = 1

def iterate_and_watch_reels(page, reel_index):
    print('reel index = ', reel_index)
    try:
        # print('finding more')
        time.sleep(1)

        # get the current reel container
        current_reel = page.locator('div.x78zum5.xl56j7k.x1n2onr6.xh8yej3').nth(reel_index)
        current_reel.click()


        # print("FOUND IT")

        # Check if the "More" button exists before interacting
        more_button_locator = current_reel.locator('span.xlej3yl:visible')
        if more_button_locator.count() > 0:
            more_button = more_button_locator.first
            more_button.click()
            # print("CLICKED THE MORE BUTTON!!")
        else:
            print("\n More button not available - skipping")
            raise Exception
            # Continue execution without interruption
                
        #once the caption and tags are expanded extract the current_reel container again
        div_content = page.locator('div.x78zum5.xl56j7k.x1n2onr6.xh8yej3').nth(reel_index)
        # print("CONTAINER TEXT = ",div_content.inner_text())

        # Clicking the comment section
        open_comments(page, reel_index)


        # Extract comments
        comments = extract_comments(page, max_comments=10)




        # input('continue?')


        #send the ai only the text from the current reel caption
        # print(div_content.inner_text())
        print("SENT AI REQUEST !!")
        ai_response = send_ai_request(div_content.inner_text(), comments)
                
                
        ai_response = str(ai_response).lower()
                
        # if reel is health, motivation or informational, then play it and wait for 20 seconds, else scroll down
        if ai_response == 'health' or ai_response == 'motivation' or ai_response == 'informational':
            current_reel.click()
            time.sleep(20)

        reel_index += 1
                
        #scrolling to next reel 
        page.keyboard.press('ArrowDown')

        return reel_index

    except Exception as e:
        print(f'ERROR {e}')
        reel_index += 1
        page.keyboard.press('ArrowDown')

        return reel_index
    
def read_cookies():
    try:
        with open('cookies.txt','r') as f:
            cookies = f.read()
            return ast.literal_eval(cookies) #convert sting to list 
    except:
        print('No cookies found, please run with "-relogin true" first')
        quit()
    
def write_cookies(cookies):
    with open('cookies.txt','w') as f:
        f.write(str(cookies))

def rewrite_cookies(page, context):
    page.goto('https://instagram.com')
    input('\nPlease perform the login and press any key after doing so')
    write_cookies(context.cookies())
    print('Cookies saved as "cookies.txt", now you can rerun the script without relogin')

def main_func(relogin, headless=True):
    reel_index = 0
    with sync_playwright() as p:
        browser = p.chromium.launch(channel='chrome', headless=False, args=browser_args )

        context = browser.new_context(
            permissions=[ ],  # Allow media autoplay
            bypass_csp=True  # Relax CSP enforcement
        )
        page = context.new_page()
        if relogin:
            rewrite_cookies(page,context)
            quit()
            
        cookies = read_cookies()
        context.add_cookies(cookies)
        # print("going to page")
        page.goto('https://instagram.com/reels')
        
        print('waiting for page to load...')
        page.wait_for_load_state('domcontentloaded')

        for i in range(21):
            reel_index = iterate_and_watch_reels(page, reel_index)
            
        # write_cookies(context.cookies())

def starting_point(iterations=True, relogin=False):
    print(f'STARTING POINT with iterations={iterations}, relogin={relogin}')
    if relogin:
        main_func(relogin, headless=False)
    while iterations and not relogin:
        main_func(relogin=False)
        print("20 REELS DONE, restarting in 1 minute...")
        time.sleep(60)