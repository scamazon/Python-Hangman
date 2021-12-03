import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showwarning, askyesno
import turtle
import re
import string
import functools
import json
import random


class Hangman(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.title('Hangman')
        
        self.data = {
            'word': tk.StringVar(),
            'hidden_word': tk.StringVar(),
            'difficulty': tk.StringVar()
        }
        
        self.style = ttk.Style()
        self.style.configure('big.TLabel', font=('Arial', 18, 'bold'))
        self.style.configure('medium.TLabel', font=('Sergoe UI', 12))
        self.style.configure('letter.TButton', width=3)

        container = tk.Frame(self)
        container.grid(row=0, column=0)

        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Menu, WordSelect, Game):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky='nsew')


        self.show_frame('Menu')

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        if page_name == 'WordSelect': frame.word_entry.focus()
        frame.grid()
        frame.focus_set()
        for frame_ in self.frames.values():
            if frame != frame_: frame_.grid_forget()
        self.geometry("")
        frame.tkraise()
    
    def get_page(self, page_name):
        return self.frames[page_name]
    
    def make_hidden_word(self):
        hidden_word = ''
        word = self.data['word'].get()
        for index, letter in enumerate(word):
            if index < len(word) - 1:
                if letter.isalpha():
                    hidden_letter = '_ '
                else:
                    hidden_letter = f'{letter} '
            else:
                hidden_letter = '_' if letter.isalpha() else letter

            hidden_word += hidden_letter
        
        self.data['hidden_word'].set(hidden_word)
        
    def start_game(self):
        game = self.get_page('Game')
        difficulty = self.data['difficulty'].get()
        if difficulty == 'Hard':
            game.draw_base()
            game.draw_stand()
            game.draw_beam()
            game.hangman_screen.update()
        wrong_guess_limit = len(game.difficulties[difficulty])
        game.guess_label_text.set(f'Wrong guesses left: {wrong_guess_limit}')
        self.show_frame('Game')


class Menu(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.word_list = json.loads(open('wordlist.json').read())
        
        self.columnconfigure(0, weight=1)

        self.title_label = ttk.Label(self, text="Hangman", style="big.TLabel")
        self.random_word_button = ttk.Button(self, text='Random word', command=self.random_word)
        self.custom_word_button = ttk.Button(self, text='Custom word', command=lambda: self.controller.show_frame('WordSelect'))
        self.difficulty_menu = ttk.OptionMenu(self, self.controller.data['difficulty'], 'Easy', *('Easy', 'Medium', 'Hard'))
        
        self.title_label.grid(row=0, padx=50, pady=(5,20))
        self.random_word_button.grid(row=1, padx=5, pady=5)
        self.custom_word_button.grid(row=2, padx=5, pady=(5,20))
        self.difficulty_menu.grid(row=3, padx=5, pady=5)
    
    def random_word(self):
        word = random.choice(self.word_list).upper()
        self.controller.data['word'].set(word)
        self.controller.start_game()
        self.controller.make_hidden_word()


class WordSelect(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.word_entry_label = ttk.Label(self, text='Enter a word:')
        self.word_entry = ttk.Entry(self)
        self.word_submit_button = ttk.Button(self, text='Ok', command=self.validate_word)
        self.word_cancel_button = ttk.Button(self, text='Cancel', command=exit)

        self.word_entry_label.grid(row=0, column=0, columnspan=2, padx=5, pady=(5,0), sticky='w')
        self.word_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=(0,5), sticky='we')
        self.word_submit_button.grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.word_cancel_button.grid(row=2, column=1, padx=5, pady=5, sticky='w')
        
        self.word_entry.bind('<Return>', lambda x: self.validate_word())
        
    def validate_word(self):
        word = self.word_entry.get()
        word = word.upper().strip()
        word = re.sub('\s+', ' ', word)
        word_valid = re.sub('[^a-zA-Z]', '', word).isalpha() and '_' not in word
        if not word_valid:
            showwarning('Warning', 'Invalid word')
            self.word_entry.focus()
        else:
            self.controller.data['word'].set(word)
            
            self.word_entry.delete(0,'end')
            self.controller.make_hidden_word()
            self.controller.start_game()
            

class Game(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.wrong_guesses = 0
        self.drawing = False
        self.difficulties = {}
        
        self.difficulties['Hard'] = [self.draw_rope,
                                     self.draw_head, 
                                     self.draw_body, 
                                     self.draw_left_arm,
                                     self.draw_right_arm,
                                     self.draw_left_leg,
                                     self.draw_right_leg]
        self.difficulties['Medium'] = [self.draw_base,
                                       self.draw_stand,
                                       self.draw_beam] + self.difficulties['Hard']
        self.difficulties['Easy'] = self.difficulties['Medium'] + [self.draw_eyes,
                                                                   self.draw_nose,
                                                                   self.draw_mouth]
        
        
        self.guess_label_text = tk.StringVar()
        
        self.canvas = tk.Canvas(self)
        self.hangman_screen = turtle.TurtleScreen(self.canvas)
        self.draw = turtle.RawTurtle(self.hangman_screen)
        
        self.guess_label = ttk.Label(self, textvariable=self.guess_label_text, style='medium.TLabel')
        self.word_label = ttk.Label(self, textvariable=self.controller.data['hidden_word'], style='big.TLabel')       
        self.letters_frame = ttk.Labelframe(self) 
        
        self.canvas.grid(row=0, padx=5, pady=5)
        self.guess_label.grid(row=1, padx=5, pady=5)
        self.word_label.grid(row=2, padx=5, pady=5)
        self.letters_frame.grid(row=3, padx=5, pady=5)       
        
        self.button_list = []
        for index, letter in enumerate(string.ascii_uppercase):
            row = int((index)/13)
            column = index if index < 13 else index - 13
            letter_button = ttk.Button(self.letters_frame, text=letter, command=functools.partial(self.guess, letter), style='letter.TButton')
            letter_button.grid(row=row, column=column, padx=5, pady=5)
            self.button_list.append(letter_button)

            eval_letter = lambda x: (lambda p: self.guess(x))
            self.bind(letter.lower(), eval_letter(letter))
        
        self.draw.hideturtle()
        self.draw.speed('fast')
        self.draw.width(3)
        self.hangman_screen.tracer(False)
    
          
    def guess(self, letter):
        index = string.ascii_uppercase.index(letter)
        button_state = self.button_list[index]['state']
        
        word = self.controller.data['word'].get()
        hidden_word = self.controller.data['hidden_word'].get()
        
        if str(button_state) != 'disabled':
            self.button_list[index]['state'] = 'disabled'
            
            if letter in word:
                for index, word_letter in enumerate(word):
                    if letter == word_letter:
                        hidden_word = hidden_word[:index*2] + letter + hidden_word[(index*2)+1:]
                self.controller.data['hidden_word'].set(hidden_word)
                if '_' not in hidden_word:
                    play_again = askyesno('You Win!', f'You win! Play again?')
                    self.restart() if play_again else exit()
            else:
                draw_list = self.difficulties[self.controller.data['difficulty'].get()]
                draw_list[self.wrong_guesses]()
                self.hangman_screen.update()
                self.wrong_guesses += 1
                self.guess_label_text.set(f'Wrong guesses left: {len(draw_list) - self.wrong_guesses}')
                if self.wrong_guesses >= len(draw_list):
                    play_again = askyesno('You Lose!', f'You lose! The word was: {word}. Play again?')
                    self.restart() if play_again else exit()
     
    def restart(self):
        for button in self.button_list:
            button['state'] = 'enabled'
        self.controller.show_frame('Menu')
        self.wrong_guesses = 0
        self.guess_label_text.set(f'Wrong guesses left: {7 - self.wrong_guesses}')
        self.draw.clear()
    
    def draw_base(self):
        self.draw.penup()
        self.draw.goto(-100, -100)
        self.draw.pendown()
        self.draw.setheading(0)
        self.draw.forward(200)
        
    def draw_stand(self):
        self.draw.penup()
        self.draw.goto(-60, -100)
        self.draw.pendown()
        self.draw.setheading(90)
        self.draw.forward(200)
        
    def draw_beam(self):
        self.draw.setheading(0)
        self.draw.forward(120)
        
    def draw_rope(self):
        self.draw.penup()
        self.draw.goto(0, 100)
        self.draw.setheading(270)
        self.draw.pendown()
        self.draw.forward(30)
    
    def draw_head(self):
        self.draw.setheading(0)
        self.draw.circle(-20)
        
    def draw_body(self):
        self.draw.penup()
        self.draw.goto(0, 30)
        self.draw.setheading(270)
        self.draw.pendown()
        self.draw.forward(60)
        
    def draw_left_arm(self):
        self.draw.penup()
        self.draw.goto(0, 20)
        self.draw.setheading(240)
        self.draw.pendown()
        self.draw.forward(35)
    
    def draw_right_arm(self):
        self.draw.penup()
        self.draw.goto(0, 20)
        self.draw.setheading(300)
        self.draw.pendown()
        self.draw.forward(35)
    
    def draw_left_leg(self):
        self.draw.penup()
        self.draw.goto(0, -30)
        self.draw.setheading(240)
        self.draw.pendown()
        self.draw.forward(40)
        
    def draw_right_leg(self):
        self.draw.penup()
        self.draw.goto(0, -30)
        self.draw.setheading(300)
        self.draw.pendown()
        self.draw.forward(40)
    
    def draw_eyes(self):
        self.draw.penup()
        self.draw.goto(-8, 55)
        self.draw.dot()
        self.draw.goto(8, 55)
        self.draw.dot()
    
    def draw_nose(self):
        self.draw.penup()
        self.draw.goto(0, 52)
        self.draw.setheading(240)
        self.draw.pendown()
        self.draw.forward(7)
        self.draw.setheading(0)
        self.draw.forward(5)
        
    def draw_mouth(self):
        self.draw.penup()
        self.draw.goto(5, 35)
        self.draw.setheading(90)
        self.draw.pendown()
        self.draw.circle(5, 180)
        
                        

if __name__ == '__main__':
    app = Hangman()
    app.mainloop()