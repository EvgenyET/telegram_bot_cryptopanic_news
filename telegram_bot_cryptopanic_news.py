import os
import requests
import deepl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

'''забираем данные из cryptopanic:'''

response = requests.get(os.environ["CRYPTOPANIC_API_URL"])

'''вывод стркутуры json:'''

# print(json.dumps(response.json(), sort_keys=True, indent=4))

'''вывод ключевых элементов построчно из json (плюсами убираем пробелы , а '\n' - перенос строки'''

def f():
   for item in response.json()['results']:
        print(item['published_at'],'\n'+item['title'],'\n('+item['url']+')\n')
   return()


'''вывод отдельных значений json в переменные:'''

d=response.json()['results'][5]['title']
i=response.json()['results'][5]['url']
h=response.json()['results'][5]['source']['title']


'''задаём опции для chromedriver:'''

options = Options()
# options.add_argument("--headless")
# options.headless = True
options.headless = False

'''запускаем chromedriver:'''

driver = webdriver.Chrome(executable_path=os.path.join(os.path.dirname(__file__), "chromedriver.exe"), options=options)
driver.get(i)

'''парсим данные по классу и записываем в переменную:'''

element = driver.find_elements(By.CLASS_NAME, "description-body")

for e in element:
    print(e.text)

g = e.text

driver.quit()


'''Работа с API DeepL:'''

auth_key = os.environ['DEEPL_AUTH_KEY']
translator = deepl.Translator(auth_key)

result = translator.translate_text(g, target_lang="RU")
result2 = translator.translate_text(d, target_lang="RU")

print(result.text)
print(result2.text)

'''работаем с API Telebot:'''

api_token = os.environ['TELEGRAM_BOT_TOKEN']

requests.get('https://api.telegram.org/bot{}/sendMessage'.format(api_token), params=dict(
   chat_id=os.environ["TELEGRAM_CHAT_ID"],
   text='_Источник:_  '+'_'+h+'_'+'\n'+'\n'+'*'+result2.text+'*'+'\n'+'\n'+result.text+'\n'+'\n'+'('+i+')', parse_mode = "Markdown"))
