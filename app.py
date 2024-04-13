from flask import Flask
import google.generativeai as genai

app = Flask(__name__)

@app.route('/test')
def test():
    return 'Hello, World!'

@app.errorhandler(404)
def page_not_found(error):
    return '404 Not Found', 404

#make token request to Gemini and return next copilot
@app.route('/copilot')
def copilot(user_input, input_path):
  model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
  new_up = genai.upload_file(path=input_path)
  prompt_final = f"Finish the following after '...': {user_input}..."
  response_final = model.generate_content([new_up, prompt_final])
  result_string = (response_final.text).replace(f'...{user_input}', "")
  result_string = (response_final.text).replace(f'... {user_input}', "")
  return result_string

if __name__ == '__main__':
    app.run(debug=True)

