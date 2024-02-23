import sys
import requests
import re
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build


if len(sys.argv) < 2:
    print('Você deve fornecer o webContentLink como argumento.')
    sys.exit(1)

web_content_link = sys.argv[1]


with open('/home/node/python/n8nDockerImage/credentials.json') as json_file:
    credentials_info = json.load(json_file)


folder_id = '1lPmyhEQ_tIc5dGgYyqeePqNNhzu6gqqJ'  


def download_google_drive_file(web_content_link):
   
    match = re.search(r'id=([a-zA-Z0-9_-]+)', web_content_link)

    if not match:
        print("ID do arquivo não encontrado na URL.")
        return None
    else:
        file_id = match.group(1)
        print("ID do arquivo:", file_id)

   
    credentials_file = '/home/node/python/n8nDockerImage/credentials.json'

    try:
        credentials = service_account.Credentials.from_service_account_file(
            credentials_file,
            scopes=['https://www.googleapis.com/auth/drive.file']
        )
    except Exception as e:
        print("Erro ao carregar credenciais:", str(e))
        return None

    drive_service = build('drive', 'v3', credentials=credentials)

   
    request = drive_service.files().get_media(fileId=file_id)
    file_contents = request.execute()

    return file_contents



def transcrever_audio(file_contents):
    
    url_whisper = 'http://whisper:5000/whisper'  # Substitua pela URL correta do serviço Whisper
    response = requests.post(url_whisper, data={'file_contents': file_contents})

    if response.status_code == 200:
        
        transcription = response.json().get('transcription', '')

       
        nome_arquivo_srt = 'transcricao.srt'
        with open(nome_arquivo_srt, 'w') as arquivo_srt:
            arquivo_srt.write(transcription)

        return nome_arquivo_srt
    else:
        print('Erro na solicitação ao serviço Whisper:', response.status_code)
        return None
    

def upload_para_google_drive(nome_arquivo_srt, folder_id):
    credentials = service_account.Credentials.from_service_account_file(
        credentials_info, ['https://www.googleapis.com/auth/drive.file']
    )

    drive_service = build('drive', 'v3', credentials=credentials)

    file_metadata = {
        'name': nome_arquivo_srt,
        'parents': [folder_id],
    }

    media = drive_service.files().create(
        body=file_metadata,
        media_body=nome_arquivo_srt,
    ).execute()

    print('Arquivo transcrito enviado para o Google Drive. ID do arquivo:', media.get('id'))
 
file_contents = download_google_drive_file(web_content_link)

if file_contents:
    
    nome_arquivo_srt = transcrever_audio(file_contents)

    if nome_arquivo_srt:
        
        upload_para_google_drive(nome_arquivo_srt)
