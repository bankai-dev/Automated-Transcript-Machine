import sys
import requests

# Verifica se houve um arquivo anexado
if len(sys.argv) < 2:
    print('Você deve fornecer o caminho do arquivo como argumento.')
    sys.exit(1)

# Pega o caminho do arquivo
file_path = sys.argv[1]

url = 'http://whisper:5000/whisper'  

# Lê o conteúdo do arquivo 
with open(file_path, 'rb') as file:
    file_content = file.read()

# Cria um dicionário com informações sobre o arquivo
files = {'file': (file_path, file_content, 'application/octet-stream')}

response = requests.post(url, files=files)

if response.status_code == 200:
    
    data = response.json()
    print(data)
else:
    print('Erro na solicitação HTTP:', response.status_code)
    print(response)
