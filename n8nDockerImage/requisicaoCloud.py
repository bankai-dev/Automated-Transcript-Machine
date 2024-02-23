import requests
import os


file_name = os.getenv("ITEM_NAME")
file_content = os.getenv("ITEM_BINARY")

url = 'http://whisper:5000/whisper'  


files = {'file': (file_name, file_content, 'application/octet-stream')}

response = requests.post(url, files=files)

if response.status_code == 200:
   
    data = response.json()
    print(data)

    
    with open('/path/para/salvar/transcricao.srt', 'w', encoding='utf-8') as srt_file:
        srt_file.write(data["transcribed_text"])

else:
    print('Erro na solicitação HTTP:', response.status_code)
