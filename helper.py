import requests
import json


def build_instruction(User, num_responses):
    """
    Builds the instruction string for Gemini based on User profile information,
    handling empty attributes gracefully.
    """
    instruction = f"You are {User.name if User.name else 'a person'} that is having a conversation. "

    # this one is debatable for sure
    if User.gender:
        instruction += f"Your gender is {User.gender}. " 

    # Age and Hobbies
    if User.age and User.hobbies:
        instruction += f"You are {User.age} years old and enjoy {User.hobbies} hobbies. "
    elif User.age:
        instruction += f"You are {User.age} years old. "
    elif User.hobbies:
        instruction += f"You enjoy {User.hobbies} hobbies. " 

    # Occupation
    if User.occupation:
        instruction += f"Your occupation is {User.occupation}. "

    # OTHER POTENTIAL FIELDS
    
    # Location 

    # Educational Background

    # Preferred Tone

    # Goal for using the app

    # Relationship status ???

    instruction += (
    "Only talk about these attributes if you are certain they are relevant to the conversation. "
    f"You will generate {num_responses} feasible responses to the conversation. "
    "Do not include any additional text describing each response, just the list of responses. "
    "Return the responses as semicolon-separated values, with no newline characters or \\n."
    )

    return instruction

def gemini_request(User, instruction, APIKEY):
    headers = {
        'Content-Type': 'application/json',
    }
    prompt = "Return a list of phrases that can be used in response to the conversational input using this JSON schema:\n                  {type: object, properties: { phrase: {type: string}}}"
    user = {"role":"user", "parts":[{ "text": prompt}]}

    # Add current prompt to the users conversation list, then generate contents
    User.conversation.append[user]
    contents = User.conversation

    data = {"system_instruction": {"parts": { "text": instruction}}, "contents": contents, "generationConfig": {"response_mime_type": "application/json",}}

    response = requests.post(
        f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent?key={APIKEY}',
        headers=headers,
        data=json.dumps(data),
    )

    dictionary = response.json()

    model_responses = json.loads(dictionary['candidates'][0]['content']['parts'][0]['text'])

    return model_responses


