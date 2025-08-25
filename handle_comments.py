from bs4 import BeautifulSoup
import time

def extract_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    comments = []
    
    # Find all comment containers
    comment_containers = soup.find_all('div', class_=lambda x: x and 'x1uhb9sk' in x and 'x1plvlek' in x and 'xryxfnj' in x)
    
    for container in comment_containers:
        try:
            # Extract username
            username_tag = container.find('a', class_='_a6hd')
            if username_tag:
                username_span = username_tag.find('span', class_='_ap3a')
                username = username_span.text if username_span else None
            else:
                username = None
                
            # Skip elements that aren't actual comments
            if not username:
                continue
                
            # Extract comment text
            comment_text_div = container.find('div', class_=lambda x: x and 'x1cy8zhl' in x)
            comment_text = comment_text_div.text.strip() if comment_text_div else None
            
            # Extract time
            time_tag = container.find('time')
            time = {
                'absolute': time_tag.get('title') if time_tag else None,
                'relative': time_tag.text if time_tag else None
            }
            
            # Only include valid comments
            if comment_text:
                comments.append({
                    'username': username,
                    'comment': comment_text,
                    'time': time
                })
                
        except Exception as e:
            print(f"Error parsing comment block: {e}")
            continue
    
    
    return get_unique_comments(comments)
    # return comments

def get_unique_comments(comments):
    unique_comments = []
    seen_comments = set()
    
    for comment in comments:
        if comment['comment'] not in seen_comments:
            seen_comments.add(comment['comment'])
            unique_comments.append(comment['comment'])
    print(f'Total unique comments: {len(unique_comments)}')
    # print(unique_comments)
    return unique_comments

def open_comments(page,reel_index):
    time.sleep(1)
    # print('clicking the comment button...')
# Step 1: Get all visible comment buttons on page by SVG label
    comment_buttons = page.locator('svg[aria-label="Comment"]').locator('..')  # parent div with click handler

    # Step 2: Print how many buttons are visible
    print(f"Total comment buttons found: {comment_buttons.count()}")

    # Step 3: Click the one matching the reel_index
    # print(f"Clicking comment button for reel index {reel_index}")
    comment_buttons.nth(reel_index).click()

def extract_comments(page, max_comments=10):
    time.sleep(2)
    # print("⏳ Extracting comments using XPath...")
    # Wait for comment section using your XPath
    comment_section = page.locator('xpath=/html/body/div[1]/div/div/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div/div[1]/div/div[2]')
    comment_section.wait_for(timeout=5000)
    print("✅ Comment section found via XPath")

    html = comment_section.inner_html()
    comments = extract_from_html(html)
    page.keyboard.press('Escape')

    return comments