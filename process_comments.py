from bs4 import BeautifulSoup

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
    print(unique_comments)
    return unique_comments

# with open('html.html', 'r', encoding='utf-8') as file:
#     data = file.read()

# comments = extract_comments(data)
# # print(comments)
# comments_no_duplicate = []
# for comment in comments:
#     # print(f"Username: {comment['username']}")
#     print(f"Comment: {comment['comment']}")
#     if comment['comment'] not in comments_no_duplicate:
#         comments_no_duplicate.append(comment['comment'])
#     # print(f"Time: {comment['time']['absolute']} ({comment['time']['relative']})")
#     # print(f"Likes: {comment['likes']}")
#     # print("-" * 40)
#     # print(comment['comment'])


# print(f'Total unique comments: {len(comments_no_duplicate)}')
# print(comments_no_duplicate)