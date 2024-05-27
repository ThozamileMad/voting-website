import hashlib
import string
import random

class User:
    def __init__(self, name, surname, id_number):
        self.name = name
        self.surname = surname
        self.id_number = id_number
        
class User_vote_information:
    def __init__(self, user , party):
        self.user = user
        self.party = party

class VoteBlock:
    def __init__(self, previous_blockhash, user_vote_information):
        self.previous_blockhash = previous_blockhash
        self.user_vote_information = user_vote_information
        
   
        self.current_block_data = str(user_vote_information) + str(previous_blockhash)
        self.current_block_hash = hashlib.sha256(self.current_block_data.encode()).hexdigest()

    def encryption_algorithm(self, user_vote_information):
        
        un_characters = string.punctuation + string.digits + " " + string.ascii_letters
        en_characters = list(un_characters)

        char_key = en_characters.copy()
        random.shuffle(char_key)
    
        cypher_text = " "
        
        encryption_code_key = random.randint(100)
    
        for single_charater in user_data:
            index = en_characters.index(single_charater)
        
            cypher_text += char_key[index]
        
        user_data = cypher_text
        return user_data