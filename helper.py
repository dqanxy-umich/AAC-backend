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