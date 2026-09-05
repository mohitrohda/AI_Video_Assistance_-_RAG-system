from utils.audio_processor import process_input
from core.transcriber import transcribe_all

source = input("Enter a YouTube URL or local audio file path: ")

chunks = process_input(source)

transcription = transcribe_all(chunks, translate=False)

print("Final Transcription:")
print(transcription)