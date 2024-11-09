from openai import OpenAI
def speechToText(audio_filepath):
  client=OpenAI(api_key='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'#这里需要替换为你的账户API KEY
    )

  audio_file= open(audio_filepath, "rb")
  transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
  )
  audio_file.close()
  print(transcription.text)
  return transcription.text