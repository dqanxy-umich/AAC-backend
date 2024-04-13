def build_instruction(user, num_responses):
    """
    Builds the instruction string for Gemini based on user profile information,
    handling empty attributes gracefully.
    """
    instruction = f"You are {user['name'] if user['name'] else 'a person'} that is having a conversation. "

    # this one is debatable for sure
    if user['gender']:
        instruction += f"Your gender is {user['gender']}. " 

    # Age and Hobbies
    if user['age'] and user['hobbies']:
        instruction += f"You are {user['age']} years old and enjoy {user['hobbies']} hobbies. "
    elif user['age']:
        instruction += f"You are {user['age']} years old. "
    elif user['hobbies']:
        instruction += f"You enjoy {user['hobbies']} hobbies. " 

    # Occupation
    if user['occupation']:
        instruction += f"Your occupation is {user['occupation']}. "

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