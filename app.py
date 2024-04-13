from flask import Flask
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


APIKEY = "AIzaSyAXxUj2bE3FXnWy4OegQUXibwCAKVhSvXA"
genai.configure(api_key=APIKEY)

app = Flask(__name__)

@app.route('/test')
def test():
    return 'Hello, World!'

@app.errorhandler(404)
def page_not_found(error):
    return '404 Not Found', 404

@app.route('/copilot')
def copilot():
  user_input = "I agree! Let's"
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
def predict_face_mood():
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
@app.route('/suggest-responses')
def suggest_responses():
    # Example User instance
    user = User("Jean", 20, "Male", ['soccer', 'coding', 'poker'], 'student')
    #  'audio/sample_turn2.wav'#
    audio_path = get_recording()
    new_file = genai.upload_file(path=audio_path)
    file_uri = new_file.uri

    # build instruction based on user data
    instruction = helper.build_instruction(user, 10)
    
    # generate HTTP request, retrieve model response
    responses = helper.gemini_request(User, instruction, file_uri, APIKEY)

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



