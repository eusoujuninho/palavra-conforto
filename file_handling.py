import os
from pydub import AudioSegment
from pydub.playback import play
from datetime import datetime

def concatenate_audio(audio_chunks):
    # Concatena uma lista de áudios em um único áudio
    combined_audio = AudioSegment.empty()
    for audio_chunk in audio_chunks:
        combined_audio += audio_chunk
    return combined_audio


def save_file(audio_binary, directory="audios"):
    # Salva o áudio binário em um arquivo no diretório especificado
    os.makedirs(directory, exist_ok=True)
    filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".mp3"
    filepath = os.path.join(directory, filename)
    with open(filepath, 'wb') as f:
        f.write(audio_binary)
    return filename
