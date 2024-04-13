from flask import Flask
import google.generativeai as genai

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
  input_path = "sample_turn2.wav"
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
  input_file = '/Users/sushritarakshit/Documents/GitHub/AAC-backend/frown.jpeg'
  model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
  new_up = genai.upload_file(path=input_file)
  prompt_final = "Describe the person's facial expression. Give one word response, not generic."
  response_final = model.generate_content([new_up, prompt_final], stream = False)
  print(response_final.text)
  return response_final.text

#make function to predict one word output/categorization
@app.route('/video-predict')
def predict_face_mood():
  input_file = '/Users/sushritarakshit/Documents/GitHub/AAC-backend/frown.jpeg'
  model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
  new_up = genai.upload_file(path=input_file)
  prompt_final = "Describe the person's facial expression. Give one word response, not generic."
  response_final = model.generate_content([new_up, prompt_final], stream = False)
  print(response_final.text)
  return response_final.text

if __name__ == '__main__':
    app.run(debug=True)


