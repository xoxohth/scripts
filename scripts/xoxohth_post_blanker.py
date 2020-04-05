from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

my_threads = []
browser = webdriver.Chrome()
browser.get('https://xoxohth.com/login.php?forum_id=2&pft=1')
user = browser.find_element_by_name('username')
user.send_keys('your_username_here')
pwd = browser.find_element_by_name('password')
pwd.send_keys('your_password_here')
submit_btn = browser.find_element_by_name('Submit')
submit_btn.click()
browser.get('https://xoxohth.com/main.php?forum_id=2&show=posted')
links = browser.find_elements_by_tag_name('a')[18::2]
for link in links:
    my_threads.append(link.get_attribute('href'))
for thread in my_threads:
    my_poasts = []
    browser.get(thread)
    posts = browser.find_elements_by_tag_name('a')
for post in posts:
    if 'post.php?message_id' in str(post.get_attribute('href')):
        edit_link = post.get_attribute('href')
        my_poasts.append(edit_link)
        for p in my_poasts:
            try:
                print(p)
                browser.get(p)
                textarea = browser.find_element_by_tag_name('textarea')
                textarea.clear()
                btn_ok = browser.find_element_by_name('btnOk')
                btn_ok.click()
                time.sleep(4)
            except:
                print('error',p)
            time.sleep(2)
