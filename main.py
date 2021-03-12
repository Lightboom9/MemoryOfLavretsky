import vk_api
import random
import time
import requests
import json
import os
from pydub import AudioSegment
from vk_api.longpoll import VkLongPoll, VkEventType

#data-mp3


def captcha_handler(captcha):
    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()

    return captcha.try_again(key)


def send_voice_message(vk, vk_session, chat_id, audio_filename):
    audio_message_url = vk_session.method('docs.getUploadServer', {'type': 'audio_message'})['upload_url']
    files = [('file', (audio_filename, open(audio_filename, 'rb')))]
    uploaded_url = requests.post(audio_message_url, files=files).text
    response = json.loads(uploaded_url)['file']
    uploaded_response = vk_session.method('docs.save', {'file': response})
    file_id = uploaded_response['audio_message']['id']
    owner_id = uploaded_response['audio_message']['owner_id']

    document = 'doc%s_%s' % (str(owner_id), str(file_id))
    vk.messages.send(chat_id=chat_id, random_id=random.randint(0, 999999999999999), message='', attachment=document)


def send_random_voice_message(vk, vk_session, chat_id):
    audio = AudioSegment.from_file('NaziVoices' + str(random.randint(1, 16)) + '.ogg', format='ogg')

    audio_length = len(audio)
    part_length = random.randint(20000, 40000)
    part_start = random.randint(0, audio_length - part_length)
    part_end = part_start + part_length

    export_filename = 'NaziVoicesToUpload.ogg'
    audio_final = audio[part_start:part_end]
    audio_final.export(export_filename, format='ogg')

    send_voice_message(vk, vk_session, chat_id, export_filename)
    os.remove(export_filename)


def main():
    with open('quotes.txt', encoding='utf8') as f:
        quotes = f.readlines()
    quotes = [s[0:s.find('©')].rstrip() for s in quotes]

    with open('pass.txt', encoding='utf-8') as f:
        passes = f.readlines()

    vk_session = vk_api.VkApi(passes[0], passes[1], app_id=2685278, captcha_handler=captcha_handler, scope="audio,docs,messages")
    vk_session.auth()
    vk = vk_session.get_api()

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    chatid = 4
    chatid2 = 5

    send_random_voice_message(vk, vk_session, chatid)

'''
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me and event.from_user:
                if event.text == '!Voice':
                    print('Sending voice message...')
                    send_voice_message(vk, vk_session, event.user_id, 'TestVoiceMsg.mp3')
                    '''

'''
    while True:
        vk.messages.send(chat_id=chatid, message=quotes[random.randint(0, len(quotes) - 1)], random_id=random.randint(0, 999999999999999))
        time.sleep(random.randint(5, 15))
        vk.messages.send(chat_id=chatid2, message=quotes[random.randint(0, len(quotes) - 1)], random_id=random.randint(0, 999999999999999))
        time.sleep(random.randint(3600, 7200))
'''

if __name__ == '__main__':
    main()
