import requests
from bs4 import BeautifulSoup
import telegram
import asyncio
import time

URL = 'https://cse.kangwon.ac.kr/cse/index.do'
BASE_URL = 'https://cse.kangwon.ac.kr'
TOKEN = ''
CHAT_ID = ''
CHAT_ID1 = ''

# 이전에 발송한 공지사항 저장을 위한 변수
previous_notices = set()

# 텔레그램 봇 설정
bot = telegram.Bot(token=TOKEN)

response = requests.get(URL)
soup = BeautifulSoup(response.text, 'html.parser')
notices_craw = soup.select_one(".main-notice-box.temp02 .mini-date") #해당 위치로 가 공지 업로드 날짜 받아오기
notice = notices_craw.text 
print(notice)
today = time.strftime('%Y.%m.%d')

if notice == today:  #todo notice 랑 현재 날짜 비교해서 참이면 아래 코드 실행 f면 종료
    # 선택한 요소의 상위 클래스에 제목이랑 href가 있어 .main-notice-box.temp02를 찾습니다.
    parent_class = notices_craw.parent
    element = parent_class.select_one('a')
    
    if element:
        title = element.text
        href = element.get('href')
        message = f"새로운 공지사항이 있습니다:\n{title}\n{BASE_URL + href}"
        print('message', message)
        
        async def send_message_async():
            await bot.send_message(chat_id=CHAT_ID, text=message)
            await bot.send_message(chat_id=CHAT_ID1, text=message)

        # asyncio를 사용하여 비동기로 실행
        asyncio.run(send_message_async())
        
else:
    print("오늘 새로운 공지는 없습니다.")
