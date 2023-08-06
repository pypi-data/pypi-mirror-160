#check if there are any mp3 in frames_dir
import os
# def check_mp3_file():
#     mp3_file_exists=False
#     for file in os.listdir(frames_dir):
#         if file.endswith(".mp3"):
#             mp3_file_exists=True
#             break
#     return mp3_file_exists
# mp3_name=""
# music_credits=""

# if check_mp3_file():
#     for file in os.listdir(frames_dir):
#         if file.endswith(".mp3"):
#             mp3_name=file
#             break
#     music_credits_filename=mp3_name.replace('.mp3','')+"_credits.txt"
#     with open(frames_dir+'/'+music_credits_filename) as f:
#         music_credits=f.read()
# else:
#     !pip install selenium
#     !apt-get update # to update ubuntu to correctly run apt install
#     !apt install chromium-chromedriver
#     !pip3 install  pyvirtualdisplay selenium webdriver_manager  > /dev/null
#     !cp /usr/lib/chromium-browser/chromedriver /usr/bin
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

ccmixter_search_url_or_keyword="instrumental"
if 'http://dig.ccmixter.org' not in ccmixter_search_url_or_keyword:
    ccmixter_search_url_or_keyword="http://dig.ccmixter.org/search?searchp="+ccmixter_search_url_or_keyword

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument("window-size=1400,1600")
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver',chrome_options=options)

driver.get(ccmixter_search_url_or_keyword)
original_html = driver.page_source
time.sleep(2)
#print("original_html", original_html)
number_of_songs_at_page=str(original_html).split('1 - ')[1].split(' of ')[0]
print ("number_of_songs_at_page", number_of_songs_at_page)
x=str(original_html).split('1 - '+number_of_songs_at_page+' of ')[1].split('</div><label')
number_of_songs = x[0].replace(',','')
#print("number_of_songs", number_of_songs)
url_with_all_songs=ccmixter_search_url_or_keyword.replace('search?',"search?limit="+number_of_songs+"&")
#url_with_all_songs="http://dig.ccmixter.org/search?limit="+number_of_songs+"&searchp=instrumental"
#new_url="http://dig.ccmixter.org/search?limit=10&searchp=instrumental"
#print("url_with_all_songs", url_with_all_songs)

driver.get(url_with_all_songs)
all_songs_html = driver.page_source
time.sleep(10)
y=str(all_songs_html).split('<a class="upload-link song-title" href="/files/')
song_list = []
for i in range(1,len(y)): #use split to get all song names
    song_list.append(y[i].split('</a> <a class="people-link artist-name light-color" ')[0].split('/')[1].split('">')[0])
random_song=random.sample(song_list,1)
print("random_song: ", random_song)
random_song_id = random_song[0].split('"')[0]


#button_element = driver.find_element_by_xpath("//button[@class='btn btn-warning  btn-lg' and @data-reactid='.0.1.6.0.2.0.0.1.$"+random_song_id+".2.0']")

button_element = driver.find_element(by=By.XPATH, value="//button[@class='btn btn-warning  btn-lg' and @data-reactid='.0.1.6.0.2.0.0.1.$"+random_song_id+".2.0']")
WebDriverWait(driver,10).until(EC.element_to_be_clickable(button_element)).click()
driver.switch_to.active_element
time.sleep(2)
html_of_song_popup = driver.page_source
time.sleep(12)
#open text file
text_file = open("data.txt", "w", encoding="utf-8")

#write string to file
text_file.write(html_of_song_popup)



#close file
text_file.close()
music_credits=str(html_of_song_popup).split('textarea readonly')[1].split('">')[1].split('</textarea>')[0]
print(music_credits)

#try putting the current code onto our pıp and see ıf we can download a song by usıng the pıp
#make a funcion in our code that takes an input search="instrumental"


mp3_url = 'http://ccmixter.org/' + str(html_of_song_popup).split('.mp3" download=""')[0].split('http://ccmixter.org/')[1] + '.mp3'
print(mp3_url)
mp3_name = "None"
if 'content' in mp3_url:
    mp3_name = mp3_url.split('http://ccmixter.org/content/')[1].replace('/','_')
elif 'contests' in mp3_url:
    mp3_name = mp3_url.split('http://ccmixter.org/contests/')[1].replace('/','_')
with open(mp3_name.split('.mp3')[0]+"_credits.txt", "w") as text_file:
    text_file.write(music_credits)
    
import os
import requests
full_save_path = os.path.join(os.getcwd())
base_path = os.path.dirname(full_save_path)
if not os.path.isdir(base_path):
    os.makedirs(base_path)

r = requests.get(mp3_url, headers={'referer': 'http://ccmixter.org/'})
if r.ok:
    with open(mp3_name, 'wb') as f:
        f.write(r.content)
else:
    r.raise_for_status()

