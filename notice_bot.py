import logging
import asyncio
import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import Message
import time

#CONST
URL = 'https://cse.kangwon.ac.kr/cse/community/undergraduate-notice.do'
TOKEN = '6236290538:AAER9AbelyQ6mrsL02SBbbZICAPtlQKUmgA'
BASE_URL = 'https://cse.kangwon.ac.kr/cse/community/undergraduate-notice.do'
CHAT_ID = '6190720715'
CHAT_ID1 = '5719645582'

# 봇 생성
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
logging.basicConfig(level=logging.INFO)


# 이전 공지사항 정보를 저장하는 변수
previous_notices = set()

# 학교 공지사항 스크래핑 함수
def get_school_notices():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    notice_titles = soup.find(attrs ={'class':'b-title-box b-notice'})
    notices = []

    title = notice_titles.a.get('title')
    href = BASE_URL + notice_titles.a.get('href')
    notices.append((title, href))
    print(notices)
    
    return set(notices)

# 알림 전송 함수
async def send_notification(new_notices):
    if new_notices:
        response = "새로운 공지사항이 있습니다:\n"
        for idx, (title, href) in enumerate(new_notices, 1):
            response += f"{idx}. {title}\n{href}\n"
        await bot.send_message(chat_id=CHAT_ID, text=response)
        await bot.send_message(chat_id=CHAT_ID1, text=response)


async def periodic_notices():
    global previous_notices
    while True:
        await asyncio.sleep(10)  # 1분마다 공지사항을 스크래핑합니다.
        current_notices = get_school_notices()
        new_notices = current_notices - previous_notices

        if new_notices:
            await send_notification(new_notices)
        previous_notices = current_notices
        
        
# 봇 시작
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(dp.start_polling())
    loop.create_task(periodic_notices())
    loop.run_forever()