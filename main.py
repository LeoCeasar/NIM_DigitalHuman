from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import logging
import os
import time
import grpc
import numpy as np
from threading import Thread
import azure.cognitiveservices.speech as speechsdk
import openai
from openai import OpenAI
#import audio2face_pb2
#import audio2face_pb2_grpc
# import soundfile

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Serve static files
# app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/audio", StaticFiles(directory="audio"), name="audio")


# Configure logging
logging.basicConfig(level=logging.INFO)

class TextItem(BaseModel):
    text: str

audio_data_list = []

def speech_synthesizer_synthesizing_cb(evt: speechsdk.SessionEventArgs):
    audio_data_list.append(evt.result.audio_data)

def azure_tts_api(txtdata):
    speech_config = speechsdk.SpeechConfig(subscription="00628ffd22984799aef224f772897a18", region="eastasia")
    speech_config.set_property(property_id=speechsdk.PropertyId.SpeechServiceResponse_RequestSentenceBoundary, value='true')
    audio_config = speechsdk.audio.AudioOutputConfig(filename='./audio/output.wav')
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    speech_synthesizer.synthesizing.connect(speech_synthesizer_synthesizing_cb)
    
    speech_synthesis_voice_name = 'zh-CN-XiaoxiaoNeural'
    ssmlstr = """<speak version='1.0' xml:lang='zh-CN' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts'>
        <voice name='{}'>"""+f"""
            <mstts:viseme type='redlips_front'/>
            {txtdata}
        </voice>
    </speak>"""
    ssml = ssmlstr.format(speech_synthesis_voice_name)
    speech_synthesis_result = speech_synthesizer.speak_ssml_async(ssml).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("SynthesizingAudioCompleted result")
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")


def startspeaking(words):
    global audio_data_list
    audio_data_list = []
    t1 = Thread(target=azure_tts_api, args=[words])
    #t2 = Thread(target=push_audio_track_stream)
    t1.start()
    #t2.start()
    t1.join()
    #t2.join()


async def call_nvidia_nim2(text:str):
    client = OpenAI(
        base_url = "https://integrate.api.nvidia.com/v1",
        api_key = "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"
    )

    completion = client.chat.completions.create(
        model="meta/llama3-70b-instruct",
        messages=[{"role":"user","content":text}],
        temperature=0.5,
        top_p=1,
        max_tokens=1024,
        stream=True
    )
    res = ""
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            res = res+chunk.choices[0].delta.content
            print(chunk.choices[0].delta.content, end="")

    return res

@app.post("/answer")
async def get_answer(item: TextItem):
    answer = await call_nvidia_nim2(item.text)
    azure_tts_api(item.text)
    return JSONResponse(content={"answer": answer})


@app.post("/synthesize")
async def synthesize(item: TextItem):
    global audio_data_list
    audio_data_list = []
    # azure_tts_api(item.text)
    # return JSONResponse(content={"audio_url": "./audio/output.wav"})
    audio_url = 'http://localhost:8000/audio/output.wav'
    return JSONResponse(content={"audio_url": audio_url})

@app.get("/audio/{filename}")
async def get_audio(filename: str):
    # file_path = f"./{filename}"
    file_path = f"./audio/{filename}"
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=filename)
    else:
        raise HTTPException(status_code=404, detail="File not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
