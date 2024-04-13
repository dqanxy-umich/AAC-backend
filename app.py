from flask import Flask
import google.generativeai as genai
import threading
import pyaudio
import wave
import time

app = Flask(__name__)

@app.route('/test')
def test():
    return 'Hello, World!'

@app.errorhandler(404)
def page_not_found(error):
    return '404 Not Found', 404

@app.route('/copilot')
def copilot(user_input, input_path):
  model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
  new_up = genai.upload_file(path=input_path)
  prompt_final = f"Finish the following after '...': {user_input}..."
  response_final = model.generate_content([new_up, prompt_final])
  result_string = (response_final.text).replace(f'...{user_input}', "")
  result_string = (response_final.text).replace(f'... {user_input}', "")
  return result_string

#make function to predict one word output/categorization
@app.route('/face-predict')
def predict_face_mood(input_file):
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
        record_thread.join()
        print("Threads killed.")
        exit(0)


