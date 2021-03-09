import vk_api
import random
import time
from vk_api.longpoll import VkLongPoll, VkEventType

def captcha_handler(captcha):
    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()

    return captcha.try_again(key)

def main():

    with open('quotes.txt', encoding='utf8') as f:
        quotes = f.readlines()
    quotes = [s[0:s.find('©')].rstrip() for s in quotes]

    with open('pass.txt', encoding='utf-8') as f:
        passes = f.readlines()

    vk_session = vk_api.VkApi(passes[0], passes[1], app_id=2685278, captcha_handler=captcha_handler)
    vk = vk_session.get_api()

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    longpoll = VkLongPoll(vk_session)
    chatid = 1

    '''
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me and event.from_chat:
                if event.text == '!DetectChat':
                    print(event.chat_id)
                vk.messages.send(chat_id=chatid, message=quotes[random.randint(0, len(quotes) - 1)], random_id=random.randint(0, 999999999999999))
    '''

    while True:
        vk.messages.send(chat_id=chatid, message=quotes[random.randint(0, len(quotes) - 1)], random_id=random.randint(0, 999999999999999))
        time.sleep(random.randint(1200, 12000));


if __name__ == '__main__':
    main()