import vk_api
import random
import time
import requests
import json
import os
from pydub import AudioSegment
from vk_api.longpoll import VkLongPoll, VkEventType


def captcha_handler(captcha):
    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()

    return captcha.try_again(key)


class VkController:
    def __init__(self, chat_ids):
        with open('pass.txt', encoding='utf-8') as f:
            passes = f.readlines()

        self.vk_session = vk_api.VkApi(passes[0], passes[1], app_id=2685278, captcha_handler=captcha_handler, scope="audio,docs,messages")
        self.vk_session.auth()
        self.vk = self.vk_session.get_api()

        with open('quotes.txt', encoding='utf8') as f:
            quotes = f.readlines()
        self.quotes = [s[0:s.find('©')].rstrip() for s in quotes]

        self.chat_ids = chat_ids

    def send_random_quotes(self):
        for chat_id in self.chat_ids:
            self.vk.messages.send(chat_id=chat_id, message=self.quotes[random.randint(0, len(self.quotes) - 1)], random_id=random.randint(0, 999999999999999))
            time.sleep(random.randint(5, 10))

    def send_random_voicelines(self):
        audio_message_url = self.vk_session.method('docs.getUploadServer', {'type': 'audio_message'})['upload_url']
        export_filename = 'NaziVoicesToUpload.ogg'

        for chat_id in self.chat_ids:
            audio = AudioSegment.from_file('NaziVoices' + str(random.randint(1, 16)) + '.ogg', format='ogg')
            audio_length = len(audio)
            part_length = random.randint(20000, 40000)
            part_start = random.randint(0, audio_length - part_length)
            part_end = part_start + part_length

            audio_final = audio[part_start:part_end]
            audio_final.export(export_filename, format='ogg')

            files = [('file', (export_filename, open(export_filename, 'rb')))]
            uploaded_url = requests.post(audio_message_url, files=files).text
            response = json.loads(uploaded_url)['file']
            uploaded_response = self.vk_session.method('docs.save', {'file': response})
            file_id = uploaded_response['audio_message']['id']
            owner_id = uploaded_response['audio_message']['owner_id']

            document = 'doc%s_%s' % (str(owner_id), str(file_id))
            self.vk.messages.send(chat_id=chat_id, random_id=random.randint(0, 999999999999999), message='', attachment=document)
            time.sleep(random.randint(5, 10))


def main():
    vk = VkController([5])
    vk.send_random_voicelines()

'''
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me and event.from_user:
                if event.text == '!Voice':
                    print('Sending voice message...')
                    send_voice_message(vk, vk_session, event.user_id, 'TestVoiceMsg.mp3')
'''


if __name__ == '__main__':
    main()
