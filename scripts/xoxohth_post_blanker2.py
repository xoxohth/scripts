import requests
import time
import random
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def xo_spider(xoLogin,xoPass,moniker,startIndex,threadCount):
    #log in to xo
    headers = {
        'Host': 'xoxohth.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'http://xoxohth.com/login.php?forum_id=2&pft=1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Connection': 'keep-alive',
        'Cookie': 'sc_is_visitor_unique=rx1599464.1554253828.3611741D3EBD4F369E9B9FCF83F394E1.1.1.1.1.1.1.1.1.1; thegmp=626269310; lastsess=1558144575; PHPSESSID=t66n3v3sgfbh7bc51cuvqenfr5',
        'Upgrade-Insecure-Requests': '1'
    }
    
    login_data = {
        'ref_page'  :	'main.php?forum_id=2',
        'username'  :	str(xoLogin),
        'password'  :	str(xoPass),
        'Submit'    :	'Sign+In'
    }
    
    with requests.Session() as s:
        url = 'http://xoxohth.com/login.php?forum_id=2&pft=1'
        s.post(url, data=login_data, headers=headers)
        
        #find any editable entries
        editList = []
        max_range = startIndex + threadCount
        while startIndex <= max_range:
            url2 = 'http://xoxohth.com/thread.php?thread_id=' + str(startIndex) + '&mc=2&forum_id=2'
            source_code = s.get(url2)
            plain_text = source_code.text
            soup = BeautifulSoup(plain_text)
            for p in soup.findAll('table'):
                if str(p).find('law school admissions discussion</a> board in the world') < 0:
                    if str(p).find('<b>Author:</b> ' + str(moniker)) > 0:
                        for img in p.findAll('img'):
                            if str(img).find('alt=\"Edit Your Message\"') > 0:
                                for img2 in p.findAll('img'):
                                    if str(img2).find('alt=\"Favorite\"') > 0:
                                        message_id = img2.get('name')
                                        if message_id not in editList:
                                            editList.append(message_id)
                                            
                                            # go to the edit page for each entry
                                            editUrl = 'http://xoxohth.com/post.php?message_id=' + str(message_id) + '&thread_id=' + str(startIndex) + '&forum_id=2'
                                            editPage = s.get(editUrl)
                                            editText = editPage.text
                                            editSoup = BeautifulSoup(editText)
                                            print(editUrl)
                                            print(" ")
                                            for editForm in editSoup.findAll('form'):
                                                options = webdriver.ChromeOptions()
                                                options.add_argument("headless")
                                                
                                                driver = webdriver.Chrome(ChromeDriverManager().install(),
                                                                          options=options)
                                                driver.get(editUrl)
                                                
                                                usernameSub = driver.find_element_by_name('username')
                                                usernameSub.send_keys(xoLogin)
                                                
                                                passSub = driver.find_element_by_name('password')
                                                passSub.send_keys(xoPass)
                                                
                                                btnSub = driver.find_element_by_name('Submit')
                                                btnSub.click()
                                                
                                                text_area = driver.find_element_by_name('message')
                                                text_area.clear()
                                                #text_area.send_keys("TEST.")
                                                
                                                submitBtn = driver.find_element_by_name('btnOk')
                                                submitBtn.click()
                                                
                                                driver.close()
                                                
                                                #make traffic look natural
                                                time.sleep(random.randint(1, 10))
            startIndex += 1

#enter your xo login account as the first argument
#enter your xo password as the second argument
#enter your moniker as the third argument (too lazy to make it work for complex things)
#enter the starting thread id (randomly click on one and get the id from the url)
#enter how many threads from the start you would like to go through
#running this consecutvively will log in/log out, so running twice would run fine first time, log you out second time (wouldnt work)
#STARTING_THREAD_ID should be an int
#ENDING_INDEX should be an int

xo_spider('YOUR_LOGIN_HERE', 'YOUR_PASSWORD_HERE', 'YOUR_MONIKER_HERE', STARTING_THREAD_ID, ENDING_INDEX)
