from flask import Flask, abort, request
from tempfile import NamedTemporaryFile
import whisper
import torch

#Testa se a placa de vídeo está disponível

torch.cuda.is_available()
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

model = whisper.load_model("base", device=DEVICE)

app = Flask(__name__)

@app.route("/")
def hello():
    return "Whisper Hello World"

@app.route('/whisper', methods=['POST'])
def manipula():
    if not request.files:
        abort(400)
    
    results = []
    
    for filename, manipula in request.files.items():
 
        temp = NamedTemporaryFile()
        
        manipula.save(temp)
        
        result = model.transcribe(temp.name)
       
        results.append({
            'filename': filename,
            'transcript': result['text'],
        })

    return {'results': results}