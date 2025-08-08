import time
import json
from playwright.sync_api import sync_playwright
from additional_tools import parse_caption_tag,send_ai_request
from process_comments import extract_from_html
import ast

parsed_reels = []
# reel_index = 1



def open_comments(page,reel_index):
    print('clicking the comment button...')
# Step 1: Get all visible comment buttons on page by SVG label
    comment_buttons = page.locator('svg[aria-label="Comment"]').locator('..')  # parent div with click handler

    # Step 2: Print how many buttons are visible
    print(f"Total comment buttons found: {comment_buttons.count()}")

    # Step 3: Click the one matching the reel_index
    print(f"Clicking comment button for reel index {reel_index}")
    comment_buttons.nth(reel_index).click()

def extract_comments(page, max_comments=10):
    time.sleep(2)
    print("⏳ Extracting comments using XPath...")
    # Wait for comment section using your XPath
    comment_section = page.locator('xpath=/html/body/div[1]/div/div/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div/div[1]/div/div[2]')
    comment_section.wait_for(timeout=5000)
    print("✅ Comment section found via XPath")

    html = comment_section.inner_html()
    comments = extract_from_html(html)
    page.keyboard.press('Escape')

    return comments

    
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

        for i in range(21):
            try:
                print('finding more')
                time.sleep(1)
                
                # page.wait_for_timeout(2000)  # Brief pause for scroll completion

                # get the current reel container
                current_reel = page.locator('div.x78zum5.xl56j7k.x1n2onr6.xh8yej3').nth(reel_index)
                current_reel.click()
                html = current_reel.inner_html()
                # print(f'here it is \n{html}')

                # page.keyboard.press('Space')
                # quit()

                print("FOUND IT")

                # Then find the MORE button WITHIN this specific container
                # more_button = current_reel.locator('span.xlej3yl:visible')
                # more_button.click() #this expands the caption and tags
                # Check if the "More" button exists before interacting
                more_button_locator = current_reel.locator('span.xlej3yl:visible')
                if more_button_locator.count() > 0:
                    more_button = more_button_locator.first
                    more_button.click()  # or your action
                    # Add your button-handling logic here
                else:
                    print("More button not available - skipping")
                    raise Exception
                    # Continue execution without interruption
                print("CLICKED THE MORE BUTTON!!")
                
                #once the caption and tags are expanded extract the current_reel container again
                div_content = page.locator('div.x78zum5.xl56j7k.x1n2onr6.xh8yej3').nth(reel_index)
                print("CONTAINER TEXT = ",div_content.inner_text())

                # Clicking the comment section
                open_comments(page, reel_index)


                # Extract comments
                comments = extract_comments(page, max_comments=10)




                # input('continue?')


                #send the ai only the text from the current reel caption
                print(div_content.inner_text())
                print("SENT AI REQUEST !!")
                ai_response = send_ai_request(div_content.inner_text(), comments)
                
                
                print(f'AI response = {ai_response}')
                # ai_response = json.loads(ai_response)
                ai_response = str(ai_response).lower()
                # input('continue?')
                
                if ai_response == 'health' or ai_response == 'motivation' or ai_response == 'informational':
                    current_reel.click()
                    time.sleep(20)

                reel_index += 1
                # input('continue?')
                page.keyboard.press('ArrowDown')
                # time.sleep(1)
            except Exception as e:
                print(f'ERROR {e}')
                reel_index += 1
                page.keyboard.press('ArrowDown')
                # time.sleep(1)
        # input('close?')
        # write_cookies(context.cookies())

while True:
    main_func()
    print("20 REELS DONE, restarting in 1 minute...")
    time.sleep(60)