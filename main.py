import vk_api
import random
from vk_api.longpoll import VkLongPoll, VkEventType

def main():

    with open('quotes.txt', encoding='utf8') as f:
        quotes = f.readlines()
    quotes = [s[0:s.find('©')] for s in quotes]

    with open('pass.txt', encoding='utf-8') as f:
        passes = f.readlines()

    vk_session = vk_api.VkApi(passes[0], passes[1], app_id=2685278)
    vk = vk_session.get_api()

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me and event.from_user:
                vk.messages.send(user_id=event.user_id, message=quotes[random.randint(0, len(quotes) - 1)], random_id=random.randint(0, 999999999999999))


if __name__ == '__main__':
    main()