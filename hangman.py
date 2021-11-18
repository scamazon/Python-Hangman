from tkinter import *
from tkinter.ttk import *
from tkinter.simpledialog import askstring
from tkinter.messagebox import showwarning, showinfo
import re
import string

root = Tk()
root.withdraw()

def replacer(s, newstring, index, nofail=False):
    if not nofail and index not in range(len(s)):
        raise ValueError("index outside given string")

    if index < 0:
        return newstring + s
    if index > len(s):
        return s + newstring

    return s[:index] + newstring + s[index + 1:]

def guess(guess_letter):
    global hidden_word
    global wrong_guesses
    button = button_index[guess_letter.lower()]
    if button['state'] != 'disabled':
        button['state'] = 'disabled'
        if guess_letter in word:
            for index, letter in enumerate(word):
                if guess_letter == letter:
                    hidden_word = replacer(hidden_word, letter, index * 2)
                    hidden_word_label['text'] = hidden_word
        else:
            wrong_guesses += 1
            wrong_guesses_label['text'] = f'Wrong guesses left: {6 - wrong_guesses}'
        if wrong_guesses >= 6:
            showinfo('You Lose!', f'You lose! The word was: {word}')

word_valid = False

while not word_valid:
    word = askstring('Word', 'Enter a word:')
    if word == None:
        exit()
    word = word.upper().strip()
    word_valid = re.sub(' ', '', word).isalpha()
    if not word_valid:
        showwarning('Warning', 'Invalid word')


hidden_word = ''
wrong_guesses = 0

for index, letter in enumerate(word):
    if index < len(word) - 1 and letter != ' ':
        hidden_letter = '_ '
    elif letter == ' ':
        hidden_letter = '  '
    else:
        hidden_letter = '_'

    hidden_word += hidden_letter


Style().configure('TLabel', font=('Arial', 18, 'bold'))
Style().configure('small.TLabel', font=('Arial', 12))
Style().configure('TButton', width=2)

root.deiconify()

root.columnconfigure(0, weight=1)

wrong_guesses_label = Label(root, text=f'Wrong guesses left: {6 - wrong_guesses}', style='small.TLabel')
wrong_guesses_label.grid(row=0, column=0, padx=5, pady=5)

hidden_word_label = Label(root, text=hidden_word)
hidden_word_label.grid(row=1, column=0, padx=5, pady=5)

letters_labelframe = LabelFrame(root)
letters_labelframe.grid(row=2, column=0, padx=5, pady=5)

a_button = Button(letters_labelframe, text='A', command=lambda: guess('A'))
a_button.grid(row=0, column=0, padx=5, pady=5)

b_button = Button(letters_labelframe, text='B', command=lambda: guess('B'))
b_button.grid(row=0, column=1, padx=5, pady=5)

c_button = Button(letters_labelframe, text='C', command=lambda: guess('C'))
c_button.grid(row=0, column=2, padx=5, pady=5)

d_button = Button(letters_labelframe, text='D', command=lambda: guess('D'))
d_button.grid(row=0, column=3, padx=5, pady=5)

e_button = Button(letters_labelframe, text='E', command=lambda: guess('E'))
e_button.grid(row=0, column=4, padx=5, pady=5)

f_button = Button(letters_labelframe, text='F', command=lambda: guess('F'))
f_button.grid(row=0, column=5, padx=5, pady=5)

g_button = Button(letters_labelframe, text='G', command=lambda: guess('G'))
g_button.grid(row=0, column=6, padx=5, pady=5)

h_button = Button(letters_labelframe, text='H', command=lambda: guess('H'))
h_button.grid(row=0, column=7, padx=5, pady=5)

i_button = Button(letters_labelframe, text='I', command=lambda: guess('I'))
i_button.grid(row=0, column=8, padx=5, pady=5)

j_button = Button(letters_labelframe, text='J', command=lambda: guess('J'))
j_button.grid(row=0, column=9, padx=5, pady=5)

k_button = Button(letters_labelframe, text='K', command=lambda: guess('K'))
k_button.grid(row=0, column=10, padx=5, pady=5)

l_button = Button(letters_labelframe, text='L', command=lambda: guess('L'))
l_button.grid(row=0, column=11, padx=5, pady=5)

m_button = Button(letters_labelframe, text='M', command=lambda: guess('M'))
m_button.grid(row=0, column=12, padx=5, pady=5)

n_button = Button(letters_labelframe, text='N', command=lambda: guess('N'))
n_button.grid(row=1, column=0, padx=5, pady=5)

o_button = Button(letters_labelframe, text='O', command=lambda: guess('O'))
o_button.grid(row=1, column=1, padx=5, pady=5)

p_button = Button(letters_labelframe, text='P', command=lambda: guess('P'))
p_button.grid(row=1, column=2, padx=5, pady=5)

q_button = Button(letters_labelframe, text='Q', command=lambda: guess('Q'))
q_button.grid(row=1, column=3, padx=5, pady=5)

r_button = Button(letters_labelframe, text='R', command=lambda: guess('R'))
r_button.grid(row=1, column=4, padx=5, pady=5)

s_button = Button(letters_labelframe, text='S', command=lambda: guess('S'))
s_button.grid(row=1, column=5, padx=5, pady=5)

t_button = Button(letters_labelframe, text='T', command=lambda: guess('T'))
t_button.grid(row=1, column=6, padx=5, pady=5)

u_button = Button(letters_labelframe, text='U', command=lambda: guess('U'))
u_button.grid(row=1, column=7, padx=5, pady=5)

v_button = Button(letters_labelframe, text='V', command=lambda: guess('V'))
v_button.grid(row=1, column=8, padx=5, pady=5)

w_button = Button(letters_labelframe, text='W', command=lambda: guess('W'))
w_button.grid(row=1, column=9, padx=5, pady=5)

x_button = Button(letters_labelframe, text='X', command=lambda: guess('X'))
x_button.grid(row=1, column=10, padx=5, pady=5)

y_button = Button(letters_labelframe, text='Y', command=lambda: guess('Y'))
y_button.grid(row=1, column=11, padx=5, pady=5)

z_button = Button(letters_labelframe, text='Z', command=lambda: guess('Z'))
z_button.grid(row=1, column=12, padx=5, pady=5)

button_index = {
    'a' : a_button,
    'b' : b_button,
    'c' : c_button,
    'd' : d_button,
    'e' : e_button,
    'f' : f_button,
    'g' : g_button,
    'h' : h_button,
    'i' : i_button,
    'j' : j_button,
    'k' : k_button,
    'l' : l_button,
    'm' : m_button,
    'n' : n_button,
    'o' : o_button,
    'p' : p_button,
    'q' : q_button,
    'r' : r_button,
    's' : s_button,
    't' : t_button,
    'u' : u_button,
    'v' : v_button,
    'w' : w_button,
    'x' : x_button,
    'y' : y_button,
    'z' : z_button
}

for letter in list(string.ascii_lowercase):
    def make_lambda(x):
        return lambda event: guess(x)
    root.bind(letter, make_lambda(letter.upper()))

root.mainloop()