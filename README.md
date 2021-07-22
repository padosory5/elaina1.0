# elaina1.0
Elaina is a personal voice assitant bot with an avatar. 
It has functions to help people in their daily lives.

# API
Google supports **Speech-To-Text** for everyone. Therefore, it can read out the voice and transform it to a text.
and that text will be sent to speak function.
With the support from **Naver Clova Premium Voice** product it is able to read out the texts that are being generated.


    def speak(audio_string):
        encText = urllib.parse.quote(audio_string)
        data = "speaker=nbora&volume=0&speed=0&pitch=1&format=mp3&text=" + encText
        url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
        request = urllib.request.Request(url)
        request.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
        request.add_header("X-NCP-APIGW-API-KEY", client_secret)
        response = urllib.request.urlopen(request, data=data.encode('UTF-8'))
        rescode = response.getcode()
        if(rescode == 200):
            print(audio_string)
            response_body = response.read()
            with open('1111.mp3', 'wb') as f:
                f.write(response_body)
            playsound.playsound("1111.mp3")
            os.remove("1111.mp3")
        else:
            print("Error Code:" + rescode)

more infomration about this API can be explained in here https://api.ncloud-docs.com/docs/en/ai-naver-clovavoice-ttspremium


#Functions

- File generate, add_content, type
- searching through google
- playing music
- alarm
- schedule
- remote control (ex : Air conditioning, television, curtains)
- time, date, weather
- message response

:heavy_check_mark: : operating :x: : not operating

There will be further updates on the fucntion.

