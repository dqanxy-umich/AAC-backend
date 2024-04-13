# Class for right now, can also make a JSON config
class User:
    conversation = []

    def __init__(self, name, age=None, gender=None, hobbies=None, occupation=None):
        self.name = name
        self.age = age
        self.gender = gender
        self.hobbies = hobbies
        self.occupation = occupation
        
    def end_conversation(self):
        self.conversation = []

