from flask import Flask, request
from user import User
import google.generativeai as genai
import threading
import pyaudio
import wave
import time
import cv2
import sys
import logging
import helper
import base64
from flask_cors import CORS, cross_origin

APIKEY = "AIzaSyAXxUj2bE3FXnWy4OegQUXibwCAKVhSvXA"
genai.configure(api_key=APIKEY)

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/test')
def test():
    return 'Hello, World!'

@app.errorhandler(404)
def page_not_found(error):
    return '404 Not Found', 404

@app.route('/copilot')
@cross_origin()
def copilot():
  user_input= request.args.get('input')
  input_path = get_recording()
  model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
  new_up = genai.upload_file(path=input_path)
  prompt_final = f"Finish the following after '...': {user_input}..."
  response_final = model.generate_content([new_up, prompt_final])
  result_string = (response_final.text).replace(f'...{user_input}', "")
  result_string = (response_final.text).replace(f'... {user_input}', "")
  return result_string

#make function to predict one word output/categorization
@app.route('/face-predict')
def face_predict():
  input_file = '/Users/sushritarakshit/Documents/GitHub/AAC-backend/images/frown.jpeg'
  model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
  new_up = genai.upload_file(path=input_file)
  prompt_final = "Describe the person's facial expression. Give one word response, not generic."
  response_final = model.generate_content([new_up, prompt_final], stream = False)
  print(response_final.text)
  return response_final.text

@app.route('/record')
def record():
    get_recording()
    return "Recording complete. File uploaded to Gemini."

#Returns the past few seconds of recording as a file that can be straight uploaded to gemini.
#May hang for a bit.
def get_recording():
    global record_flag
    global write_flag
    global kill_flag
    record_flag = True
    while not write_flag:
        if kill_flag:
            break
        pass
    write_flag = False
    record_flag = False
    return "output.wav"

record_flag = False
write_flag = False

def record_thread():
    global record_flag
    global write_flag
    global kill_flag
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = []

    while not kill_flag:
        while not record_flag:
            if kill_flag:
                break
            data = stream.read(CHUNK)
            frames.append(data)
        if kill_flag:
            break
        print("* done recording")

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames[-min(len(frames),int(RATE / CHUNK * RECORD_SECONDS)):]))
        wf.close()
        write_flag = True
        while write_flag:
            pass
    
    stream.stop_stream()
    stream.close()
    p.terminate()


    
#make function to predict one word output/categorization
@app.route('/video-predict')
def predict_face_mood_2():
  input_file = '/Users/sushritarakshit/Documents/GitHub/AAC-backend/frown.jpeg'


#render camera on spot
@app.route('/cam-capture')
def predict_face_vis():
  camera = cv2.VideoCapture(0)
  logging.info("Camera opened")
  time.sleep(1)
  ret, frame = camera.read()
  logging.info("grabbed frame")
  camera.release()
  logging.info("camera done")
  fshape = frame.shape
  fheight = fshape[0]
  fwidth = fshape[1]
  #fourcc = cv2.VideoWriter_fourcc(*'XVID')
  logging.info("made video file")
  #out = cv2.VideoWriter('output.avi',fourcc, 20.0, (fwidth,fheight))
  cv2.imwrite('captured_image.jpg', frame)
  logging.info("successdully written")


  model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
  new_up = genai.upload_file(path='/Users/sushritarakshit/Documents/GitHub/AAC-backend/captured_image.jpg')
  prompt_final = "Describe the person's facial expression. Give one word response, not generic."
  response_final = model.generate_content([new_up, prompt_final], stream = False)
  print(response_final.text)
  return response_final.text

# temporary route using python sdk, will switch to JSON using Curl
#integrate responses with user info
@app.route('/suggest-responses')
@cross_origin()
def suggest_responses():
    
    # Example User instance
    user = User("Sushrita", 32, "Female", ['soccer', 'coding', 'poker'], 'student')

        
    # prompt and instruction
    # prompt = f"Respond to the person speaking. Your response should pertain to a style matching the User's demographics: {user.name}, {user.age}, {user.gender}, {user.hobbies}, {user.occupation}."
   
    instruction = helper.build_instruction(user, 10)
    # generate HTTP request, retrieve model response
    # audio input 
    #audio_path = 'audio/sample_turn2.wav'# get_recording()
    #audio_file = genai.upload_file(path=audio_path)
    audio_file = get_recording() #-> just get the recording


    prompt = f"Respond to the person speaking. Your response should pertain to a style matching the User's demographics: {user.name}, {user.age}, {user.gender}, {user.hobbies}, {user.occupation}."
    instruction = helper.build_instruction(user, 10)

    model = genai.GenerativeModel(
        'models/gemini-1.5-pro-latest',
        system_instruction=instruction
    )

    response = model.generate_content([prompt, audio_file])
    logging.info("got response")
    responses = response.text.replace('\n', '').strip().split(";")
    logging.info("split response")

    return responses

@app.route('/full-context')
def gen_full_context():
    #get visuals
    opponent_mood = predict_face_vis()
    #opponent_mood = 'infurious'
    user = User("Sushrita", 32, "Female", ['soccer', 'coding', 'poker'], 'student')

    # audio input 
    #audio_path = 'audio/sample_turn2.wav'# get_recording()
    #audio_file = genai.upload_file(path=audio_path)
    audio_file = get_recording() #-> just get the recording


    prompt = f"Respond to the person speaking. Your response should pertain to a style matching the User's demographics: {user.name}, {user.age}, {user.gender}, {user.hobbies}, {user.occupation}. Also keep in mind the opposing speaker feels like this: {opponent_mood}"
    instruction = helper.build_instruction(user, 10)

    model = genai.GenerativeModel(
        'models/gemini-1.5-pro-latest',
        system_instruction=instruction
    )

    response = model.generate_content([prompt, audio_file])
    logging.info("got response")
    responses = response.text.replace('\n', '').strip().split(";")
    logging.info("split response")

    return responses



    


if __name__ == '__main__':
    global kill_flag
    kill_flag = False
    record_thread = threading.Thread(target=record_thread)
    record_thread.start()
    app.run(debug=True)
    try:
        while 1:
            time.sleep(.1)
    except:
        kill_flag = True
        print("Enabled kill flag.")
        record_thread.join()
        print("Threads killed.")
        exit(0)



