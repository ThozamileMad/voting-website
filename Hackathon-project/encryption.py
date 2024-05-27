import random
import string

        
def encryption_algorithm(user_data):
    un_characters = string.punctuation + string.digits + " " + string.ascii_letters
    en_characters = list(un_characters)

    char_key = en_characters.copy()
    random.shuffle(char_key)
    
    cypher_text = " "
    main_key = 6
    
    for single_charater in user_data:
        index = en_characters.index(single_charater)
        
        cypher_text += char_key[index]
        
    user_data = cypher_text
    return user_data

name = "John"
print(encryption_algorithm(name))     


