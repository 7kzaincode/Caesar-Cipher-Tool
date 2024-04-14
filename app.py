from flask import Flask, render_template, request

import nltk
nltk.download('words')
from nltk.corpus import words
english_words = set(words.words())
app = Flask(__name__)

def shift(char, key, alphabet):
    original_case = char.isupper()
    char = char.upper()
    if char in alphabet:
        num = alphabet[char]
        shifted_num = (num + key - 1) % 26 + 1
        for letter, value in alphabet.items():
            if value == shifted_num:
                if not original_case:
                    letter = letter.lower()
                return letter
    else:
        return char
def caesar(key, plaintext):
    alphabet = {
        'A': 1, 'B': 2,
        'C': 3, 'D': 4,
        'E': 5, 'F': 6,
        'G': 7, 'H': 8,
        'I': 9, 'J': 10,
        'K': 11, 'L': 12,
        'M': 13, 'N': 14,
        'O': 15, 'P': 16,
        'Q': 17, 'R': 18,
        'S': 19, 'T': 20,
        'U': 21, 'V': 22,
        'W': 23, 'X': 24,
        'Y': 25, 'Z': 26
    }
    shifted_text = ""
    for letter in plaintext:
        shifted_text += shift(letter, key, alphabet)
    return shifted_text
def decrypt_caesar_cipher(text, shift):
    decrypted_text = ""
    for char in text:
        if char.isalpha():
            shift_amount = shift % 26
            if char.islower():
                decrypted_text += chr((ord(char) - shift_amount - 97) % 26 + 97)
            else:
                decrypted_text += chr((ord(char) - shift_amount - 65) % 26 + 65)
        else:
            decrypted_text += char
    return decrypted_text
def decrypt(text):
    possible_texts = []
    for shift in range(1, 27):
        decrypted_text = decrypt_caesar_cipher(text, shift)
        if is_english(decrypted_text):
            possible_texts.append((shift, decrypted_text))
    return possible_texts
def is_english(text):
    text_words = text.split()
    count = sum(1 for word in text_words if word.lower() in english_words)
    return count > 0

"""encrypted_message = caesar(12, input("Enter Word: "))
print(encrypted_message)

decrypted_results = decrypt(encrypted_message)

for result in decrypted_results:
    print(f"Shift {result[0]}: {result[1]}")
"""


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'encrypt' in request.form:
            plaintext = request.form['plaintext']
            shift = int(request.form['shift'])
            encrypted_message = caesar(shift, plaintext)
            return render_template('index.html', encrypted_message=encrypted_message)
        elif 'decrypt' in request.form:
            ciphertext = request.form['ciphertext']
            decrypted_results = decrypt(ciphertext)
            return render_template('index.html', decrypted_results=decrypted_results)
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)