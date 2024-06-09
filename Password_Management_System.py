'''
-> Microsoft Policy for Creating strong passwords

Password security starts with creating a strong password. A strong password is:

- At least 12 characters long but 14 or more is better. - Done

- A combination of uppercase letters, lowercase letters, numbers, and symbols. - Done

- Not a word that can be found in a dictionary or the name of a person, character, product, or organization.

- Significantly different from your previous passwords.

- Easy for you to remember but difficult for others to guess. Consider using a memorable phrase like "6MonkeysRLooking^".
'''

# Libraries
import re
import string
import secrets
from flask import Flask, request

app = Flask(__name__)

password = "Sample@12345"

def checking_password_security(password):
    haslowercase_letter = True
    hasuppercase_letter = True
    hasnumber = True

    # Upper and Lower case Logic
    for letter in password:
        if letter.isupper():
            hasuppercase_letter = False
        if letter.islower():
            haslowercase_letter = False

    # Numbers and Special Chars Logic
    expression = "\d"
    hasnumber = bool(re.search(expression, password))
    expression_for_specialchars = '[^A-Za-z0-9\s]'
    hasspecial_chars = bool(re.search(expression_for_specialchars, password))

    # Main Program Conditions
    if len(password) <= 12:
        return "Your password do not have a length of 12. Please make sure to atleast use 12 characters long password."
    elif hasuppercase_letter:
        return "Your password do not have upper case letter."
    elif haslowercase_letter:
        return "Your password do not have lower case."
    elif hasnumber==False:
        return "Your password do not have a number."
    elif hasspecial_chars==False:
        return "Your password do not have special characters."
    else:
        return False


# Generating secure password using Secrets
def random_password_generator(length):
    policy = string.ascii_uppercase + string.ascii_lowercase + string.digits + string.punctuation

    password1 = ''
    password2 = ''
    password3 = ''
    for i in range(16):
        password1 += secrets.choice(policy)
        password2 += secrets.choice(policy)
        password3 += secrets.choice(policy)
        
    final_password = ''
    for i in range(14):
        final_password += secrets.choice(password1 + password2 + password3)
    
    return final_password

@app.route('/api/secure_password_generator', methods=['GET'])
def secure_password_generator():
    
    validating_password = True
    while validating_password:
        rand_pass = random_password_generator(14)
        validating_password = checking_password_security(rand_pass)
    return {'message': rand_pass}

@app.route('/api/secure_password_checker', methods=['POST'])
def secure_password_checker():
    data = request.json
    password = data.get("password")
    reply = checking_password_security(password)
    if reply == False:
        return {'message': 'Your Password is Secure.'}
    else:
        return {'message': reply}

if __name__ == '__main__':
    app.run(debug=True)
