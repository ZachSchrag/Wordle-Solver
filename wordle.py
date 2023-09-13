# list of valid words is stored in "words.txt"
import tkinter as tk # GUI
import random # used for testing

    
# highlight button/textbox when focused
#   have to use ttk buttons, but lose some attributes. Need to check documentation. Otherwise, have to bind it :/
# highlighting background is def possible with frame.configure and label["background"]

# automatically tabing over something with a yellow warning ; did not catch error entirely
# enable strict check while on green letters with warning properly prompted, no focus is left from yellow entry so warning does not go away
# create __enable(Green)Warning methods and clean validateGreenInput up
# fix yellow frame positioning


class App(tk.Tk):
    
  def __init__(self):
    super().__init__()
    self.__configWindow__()
    self.__configRowCol__()

    # directions label
    tk.Label(self, text = "Enter the placed letters, unplaced letters, and invalid letters and press \"Solve\"!", 
                          font = ("" , 12, "bold")).grid(column = 0, row = 0, padx = 115, pady = 25, sticky = tk.S)
    
    # placed letters widgets
    tk.Label(self, text="Placed Letters",
             font = ("", 11, "bold")).grid(column = 0, row = 1, sticky = tk.S)
    self.greenFrame = self.__createGreenLetterFrame__()
    self.greenFrame.grid(column = 0, row = 2)
    self.greenFrame.winfo_children()[0].focus() # init window focus
    self.greenWarnings = self.__createGreenWarnings__()
    self.greenWarnings.grid(column = 0, row = 3, sticky = tk.N)

    # unplaced letters widgets
    tk.Label(self, text="Unplaced Letters", 
             font = ("", 11, "bold")).grid(column = 0, row = 4, sticky = tk.S)
    self.yellowFrame = self.__createYellowLetterFrame__()
    self.yellowFrame.grid(column = 0, row = 5, sticky = tk.S)
    self.yellowChecksWarningsFrame = self.__createYellowChecksWarnings__()
    self.yellowChecksWarningsFrame.grid(column = 0, row = 6, pady = 5, sticky = tk.N)

    # invalid letters widgets
    self.greyFrame = self.__createGreyLetterFrame__()
    self.greyFrame.grid(column = 0, row = 7, sticky = tk.N)

    # buttons
    self.solveButton = tk.Button(self, text = "Solve", width = 10, font = ("", 10, "bold"), relief = "solid", command = self.__onSolve__)
    self.solveButton.grid(column = 0, row = 8, padx = 100)
    self.clearButton = tk.Button(self, text = "Clear", width = 10, font = ("", 10, "bold"), relief = "solid", command = self.__onClear__)
    self.clearButton.grid(column = 0, row = 9, padx = 100, sticky = tk.N)


  def __configWindow__(self):
      self.title('Wordle Solver')
      self.attributes('-alpha', True)
      self.geometry('1400x1050')
      self.resizable(False, False)
      #self.configure(bg = "Salmon")


  def __configRowCol__(self):
    self.rowconfigure(0, weight = 2) # directions label
    self.rowconfigure(1, weight = 1) # green letters label
    self.rowconfigure(2, weight = 1) # green warning labels
    self.rowconfigure(3, weight = 1) # green letters frame
    self.rowconfigure(4, weight = 1) # yellow letters label
    self.rowconfigure(5, weight = 1) # yellow letters frame
    self.rowconfigure(6, weight = 1) # yellow letter checkboxes (strict check, multi letters) + warning labels
    self.rowconfigure(7, weight = 2) # invalid letter label, frame, warnings
    self.rowconfigure(8, weight = 1) # solve button
    self.rowconfigure(9, weight = 1) # clear button
      

  # *** PLACED LETTERS METHODS ***
  def __createGreenLetterFrame__(self):
      frame = tk.Frame(self)
      self.greenLetters = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
    
      tk.Entry(frame, width = 4, justify = "center", background = "lime", font = ("", 18, "bold"),
               relief = "solid", textvariable = self.greenLetters[0]).grid(column = 0, row = 1, padx = 3, sticky = tk.S) 
      tk.Entry(frame, width = 4, justify = "center", background = "lime", font = ("", 18, "bold"), 
               relief = "solid", textvariable = self.greenLetters[1]).grid(column = 1, row = 1, sticky = tk.E)  
      tk.Entry(frame, width = 4, justify = "center", background = "lime", font = ("", 18, "bold"),
               relief = "solid",textvariable = self.greenLetters[2]).grid(column = 2, row = 1, padx = 3, sticky = tk.S)
      tk.Entry(frame, width = 4, justify = "center", background = "lime", font = ("", 18, "bold"),
               relief = "solid",textvariable = self.greenLetters[3]).grid(column = 3, row = 1, sticky = tk.W)
      tk.Entry(frame, width = 4, justify = "center", background = "lime", font = ("", 18, "bold"),
               relief = "solid",textvariable = self.greenLetters[4]).grid(column = 4, row = 1, padx = 3, sticky = tk.S)

      # not using bind_class because there are different validations for each frame of input
      for i, entry in enumerate(frame.winfo_children()):
          entry.bind("<Key>", lambda e, d = self.greenLetters[i], i = i: self.__validateGreenInput__(e, d, i), add ="+")
          entry.bind("<FocusOut>", self.__removeGreenWarnings__, add = "+")
         
      return frame
  
  def __createGreenWarnings__(self):
      frame = tk.Frame(self)
      self.greenIncludedInvalid = tk.Label(frame, text = "(!) <key> is included in invalid letters (!)", font = ("", 9, "bold"), fg="red")
      self.greenIncludedValid = tk.Label(frame, text = "(!) <key> is included in unplaced letters in the same position with strict check (!)",
                                         font = ("", 9, "bold"), fg="red")
      return frame
  
  def __validateGreenInput__(self, event, data, i):
      print(event)
      key = event.char.upper()
      ret = self.__validateGenericInput__(event.keysym, key) # generic validation which all entries must satisfy

      if ret == 0: # passed, complete green specific 
          if key in self.greyLetters.get():
              self.__enableGreenInvalidWarning__(key)
          elif self.strictYellowCheck.get() == "1" and key in self.yellowLetters[i].get():
              self.__enableGreenValidWarning__(key)
          else:
              self.__removeGreenWarnings__()
              self.__removeYellowWarnings__() # if placed and unplaced letters collide and user enables strict mode while adding to placed letters, label sticks
              event.widget.delete(0)
              data.set(key)
              self.__goNextEntry__(i)
          return "break" # want all input to automatically go to captial letters without delay so we manually ignore the event
      elif ret == 1:
          self.__removeYellowWarnings__() # if placed and unplaced letters collide and user enables strict mode while adding to placed letters, label sticks
          self.__goNextEntry__(i, event.keysym)
          pass
      else:
          return ret # returns either None to allow key to come through or "break" to stop processing 
      
  def __removeGreenWarnings__(self, e = None):
      self.greenIncludedInvalid.grid_remove()
      self.greenIncludedValid.grid_remove()

  def __enableGreenInvalidWarning__(self, key):
      self.greenIncludedValid.grid_remove()
      self.greenIncludedInvalid["text"] = "(!) " + key + " is included in invalid letters (!)"
      self.greenIncludedInvalid.grid(column = 0, row = 0, sticky = tk.N)

  def __enableGreenValidWarning__(self, key):
      self.greenIncludedInvalid.grid_remove()
      self.greenIncludedValid["text"] = "(!) " + key + " is included in unplaced letters in the same position with strict check (!)"
      self.greenIncludedValid.grid(column = 0, row = 0, sticky = tk.N)
      
      
  # *** UNPLACED LETTERS METHODS ***
  def __createYellowLetterFrame__(self):
      frame = tk.Frame(self)
      self.yellowLetters = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
      
      tk.Entry(frame, width = 4, justify = "center", background = "yellow", font = ("", 18, "bold"), 
               relief = "solid", textvariable = self.yellowLetters[0]).grid(column = 0, row = 1, padx = 3, sticky = tk.S)
      tk.Entry(frame, width = 4, justify = "center", background = "yellow", font = ("", 18, "bold"),
               relief = "solid", textvariable = self.yellowLetters[1]).grid(column = 1, row = 1, sticky = tk.SE)  
      tk.Entry(frame, width = 4, justify = "center", background = "yellow", font = ("", 18, "bold"),
               relief = "solid", textvariable = self.yellowLetters[2]).grid(column = 3, row = 1, padx = 3, sticky = tk.S)
      tk.Entry(frame, width = 4, justify = "center", background = "yellow", font = ("", 18, "bold"),
               relief = "solid", textvariable = self.yellowLetters[3]).grid(column = 4, row = 1, sticky = tk.W)
      tk.Entry(frame, width = 4, justify = "center", background = "yellow", font = ("", 18, "bold"),
               relief = "solid", textvariable = self.yellowLetters[4]).grid(column = 5, row = 1, padx = 3, sticky = tk.S)

      # not using bind_class because there are different validations for each frame of input
      for i, entry in enumerate(frame.winfo_children()):
          entry.bind("<Key>", lambda e, d = self.yellowLetters[i], i = i: self.__validateYellowInput__(e, d, i), add = "+")
          entry.bind("<FocusOut>", self.__removeYellowWarnings__, add = "+")

      return frame
  
  def __createYellowChecksWarnings__(self):
      frame = tk.Frame(self)

      self.strictYellowCheck = tk.StringVar()
      tk.Checkbutton(frame, text = "Strict check (considers position of letter)", variable = self.strictYellowCheck, font = ("", 8, "bold"),
                     offvalue = "", fg = "red", command = lambda e = self.strictYellowCheck: self.__updateCheckBoxColor__(e, 0)
                     ).grid(column = 0, row = 0, sticky = tk.N)
      
      self.multipleYellowCheck = tk.StringVar()
      tk.Checkbutton(frame, text = "Allow multiple letters per entry", variable = self.multipleYellowCheck, font = ("", 8, "bold"),
                     offvalue = "", fg = "red", command = lambda e = self.multipleYellowCheck: self.__updateCheckBoxColor__(e, 1)
                     ).grid(column = 0, row = 1, sticky = tk.N)
      
      self.strictCollision = tk.Label(frame, text = "(!) Collision of placed and unplaced letters is not allowed in strict mode (!)",
                                    font = ("", 8, "bold"), fg = "red")
      self.yellowIncludedInvalid = tk.Label(frame, text = "(!) <key> is included in invalid letters (!)", font = ("", 8, "bold"), fg = "red")
      self.yellowIncludedInside = tk.Label(frame, text = "(!) <key> already included in this entry (!)", font = ("", 8, "bold"), fg = "red")

      return frame

  def __validateYellowInput__(self, event, data, i):
      key = event.char.upper()
      ret = self.__validateGenericInput__(event.keysym, key) # generic validation which all entries must satisfy
      allowMulti = self.multipleYellowCheck.get()
      strictMode = self.strictYellowCheck.get()
      print(event)

      if ret == 0: # passed, complete yellow specific validation
          if key in self.greyLetters.get(): # key already in invalid list
              self.__enableYellowInvalidWarning__(key)
          elif strictMode == "1" and self.greenLetters[i].get() == key: # key already in placed letters with strict mode enabled
              self.__enableYellowCollisonWarning__()
          elif allowMulti == "1" and key in self.yellowLetters[i].get(): # key already in focused entry
              self.__enableYellowInsideWarning__(key)
          elif allowMulti == "1": # multi enabled, add to list
              index = event.widget.index(tk.INSERT)
              event.widget.insert(index, key)
              self.__removeYellowWarnings__()
          else: # wipe current data and place last key typed
              event.widget.delete(0)
              data.set(key)
              self.__goNextEntry__(i + 5)
              self.__removeYellowWarnings__()
          return "break"
      elif ret == 1:
          self.__goNextEntry__(i + 5, event.keysym)
          pass
      else:
          return ret # returns either None to allow key to come through or "break" to stop processing 
  
  def __updateCheckBoxColor__(self, data, i):
      box = self.yellowChecksWarningsFrame.winfo_children()[i]
      if data.get() != "1":
           if i == 1:
               # disabled multiLetter box, reset all yellow letter inputs to their last character
               for x in self.yellowLetters:
                   if len(x.get()) > 1:
                       x.set(x.get()[-1])
           box["fg"] = "red"
      else:
           if i == 0: # enabled strictCheck box, ensure green letters and yellow letters do not collide
               collison = False
               for j in range(5):
                   green = self.greenLetters[j].get()
                   yellow = self.yellowLetters[j]
                   if green != "" and green in yellow.get(): # collision
                       yellow.set(yellow.get().replace(green, ""))
                       collison = True
               if collison:
                   self.__enableYellowCollisonWarning__()
           box["fg"] = "#129304"      

  def __removeYellowWarnings__(self, e = None):
      self.strictCollision.grid_remove()
      self.yellowIncludedInside.grid_remove()
      self.yellowIncludedInvalid.grid_remove()
      # self.yellowChecksWarningsFrame.winfo_children()[0].grid(column = 0, row = 0)
      # self.yellowChecksWarningsFrame.winfo_children()[1].grid(column = 0, row = 1)

  def __enableYellowCollisonWarning__(self):
      self.yellowIncludedInvalid.grid_remove()
      self.yellowIncludedInside.grid_remove()
      self.strictCollision.grid(column = 0, row = 0)
      self.__moveYellowChecks__()

  def __enableYellowInvalidWarning__(self, key):
      self.strictCollision.grid_remove()
      self.yellowIncludedInside.grid_remove()
      self.yellowIncludedInvalid["text"] = "(!) " + key + " is included in invalid letters (!)"
      self.yellowIncludedInvalid.grid(column = 0, row = 0)
      self.__moveYellowChecks__()

  def __enableYellowInsideWarning__(self, key):
      self.yellowIncludedInvalid.grid_remove()
      self.strictCollision.grid_remove()
      self.yellowIncludedInside["text"] = "(!) " + key + " already included in this entry (!)"
      self.yellowIncludedInside.grid(column = 0, row = 0)
      self.__moveYellowChecks__()

  def __moveYellowChecks__(self):
      self.yellowChecksWarningsFrame.winfo_children()[0].grid(column = 0, row = 1) # strict mode
      self.yellowChecksWarningsFrame.winfo_children()[1].grid(column = 0, row = 2) # multi letter mode
      
      
  # *** INVALID LETTERS METHODS ***
  def __createGreyLetterFrame__(self):
      frame = tk.Frame(self)
      self.greyLetters = tk.StringVar()
      
      tk.Label(frame, text="Invalid Letters", justify = "center",
               font = ("", 11, "bold")).grid(column = 0, row = 0, pady = 5)
      entry = tk.Entry(frame, justify = "center", background = "lightgrey", relief = "solid",
               textvariable = self.greyLetters, width = 24, font = ("", 16, "bold"))
      entry.grid(column = 0, row = 1)

      # labels for indicating that a letter known to be in the word was placed in "invalid letters"
      self.greyIncludedAbove = tk.Label(frame, text="(!) <key> is included above (!)", font = ("", 9, "bold"), fg="red")
      self.greyIncludedInside = tk.Label(frame, text="(!) <key> is already included in invalid letters (!)", font = ("", 9, "bold"), fg="red")

      entry.bind("<Key>", self.__validateGreyInput__)
      entry.bind("<FocusOut>", self.__removeGreyWarnings__, add="+")
      return frame

  def __validateGreyInput__(self, event):
      key = event.char.upper()
      ret = self.__validateGenericInput__(event.keysym, key) # generic validation which all entries must satisfy
    
      if ret == 0: # passed, complete grey specific validation
          data = self.greyLetters.get()
          if (key in data): # attempted insert is already in list of invalid letters
              self.__enableGreyInsideWarning__(key)
          elif (key in [x.get() for x in self.greenLetters] or key in [y.get() for y in self.yellowLetters]):
              self.__enableGreyAboveWarning__(key)
          else:
            event.widget.insert(len(data), key)
            event.widget.icursor(len(data) + 1)
            self.__removeGreyWarnings__()
          return "break"
      elif ret == 1:
          self.__goNextEntry__(10, event.keysym)
      else:
          self.__removeGreyWarnings__()
          return ret
          
  def __removeGreyWarnings__(self, e = None):
      self.greyIncludedAbove.grid_remove()
      self.greyIncludedInside.grid_remove()

  def __enableGreyInsideWarning__(self, key):
      self.greyIncludedInside["text"] = "(!) " + key + " is already included in invalid letters (!)"
      self.greyIncludedInside.grid(column = 0, row = 5, sticky = tk.S)
      self.greyIncludedAbove.grid_remove()

  def __enableGreyAboveWarning__(self, key):
      self.greyIncludedAbove["text"] = "(!) " + key + " is already included above (!)"
      self.greyIncludedAbove.grid(column=0, row = 5, sticky = tk.N)
      self.greyIncludedInside.grid_remove()
      
      
  # helper methods
  def __validateGenericInput__(self, keysym, key):
      if self.__isSpecialKey__(keysym): # enter, delete, escape
          return
      elif keysym in ["Left", "Right", "Up", "Down"] or key == "\x08": # special case entry changing keys
          return 1
      elif key in "\t": # keys intended to have their assumed purpose (tab, shift, caps)
          return
      elif not (key >= "A" and key <= "Z"): # keys which produced output that isn't a letter
          return "break"
      return 0 # valid key pressed
  
  def  __isSpecialKey__(self, key):
      # a bind_all was failing to produce this result so we instead check on generic input checks 
      if key == "Return":
          self.__onSolve__()
      elif key == "Delete":
          self.__onClear__()
      elif key == "Escape":
          self.destroy()
      return key == "Return" or key == "Delete" or key == "Escape"
  
  def __onSolve__(self):
      for x in self.greenLetters:
          print(x.get())
      self.geometry("1920x1080")

  def __onClear__(self):
      for x, y in zip(self.greenLetters, self.yellowLetters):
          x.set("")
          y.set("")
      self.greyLetters.set("")
      self.__removeYellowWarnings__()
      self.__removeGreenWarnings__()
      self.__removeGreyWarnings__()
      self.greenFrame.winfo_children()[0].focus()
      self.geometry("1400x1050")
            
  def __goNextEntry__(self, i, keysym = ""):
      if i < 5: # green frame
          if keysym == "Down":
              self.yellowFrame.winfo_children()[i].focus()
          elif keysym == "Left" and i > 0:
              self.greenFrame.winfo_children()[i - 1].focus()
          elif i == 4:
              self.yellowFrame.winfo_children()[0].focus()
          else:
              self.greenFrame.winfo_children()[i + 1].focus()

      elif i < 10: # yellow frame
          # indexs for strict check. if at index 0 and press left key go prev entry, index len() w/ right key go next entry
          if keysym == "Up":
              self.greenFrame.winfo_children()[i - 5].focus()
          elif keysym == "Down":
              self.greyFrame.winfo_children()[1].focus()
          elif self.multipleYellowCheck.get() != "1":
            if keysym == "Left":
                if i == 5:
                    self.greenFrame.winfo_children()[4].focus()
                else:
                    self.yellowFrame.winfo_children()[i - 6].focus()
            else:
                print(i)
                self.yellowFrame.winfo_children()[i - 4].focus()

      else: # grey frame
          index = self.greyFrame.winfo_children()[1].index(tk.INSERT)
          if keysym == "Up":
              if index > 4:
                  index = 4
              self.yellowFrame.winfo_children()[index].focus()
          elif keysym == "Left":
              if index == 0:
                  self.yellowFrame.winfo_children()[4].focus()


'''
def read_input(words):
    green_letters = {}
    yellow_letters = [[], [], [], [], []]

    letters = open("example.txt", "r").readlines()
    green = letters[0].strip("\n").split(",")
    yellow = letters[1].strip("\n").split(",")    
    grey_letters = letters[2].strip().split(",")

    for let in green:
        if (len(let) < 2):
            continue
        green_letters[let[0]] = int(let[2])
    
    for let in yellow:
        if (len(let) < 2):
            continue
        yellow_letters[int(let[2])].append(let[0])
    
    return green_letters, yellow_letters, grey_letters
    

    
def guess(possible_words):
    # list of the letters sorted by frequency
    freq = {'e': 0, 't':1, 'a':2, 'o':3, 'n':4, 'i':5, 'h':6, 's':7, 'r':8, 'l':9, 'd':10, 'u':11, 'c':12,
            'm':13, 'w':14, 'y':15, 'f':16, 'g':17, 'p':18, 'b':19, 'v':20, 'k':21, 'j':22, 'x':23, 'q':24, 'z':25}
    
    ret = []
    scores = []
    # assign each word a "score" which is defined as the sum of the freq of each letters
    # the score of a single letter is given by its corresponding key:value pair (e.g., e is 0 and z is 25)
    # the word with the least score includes the most frequently used characters and will be used as the next guess
    for word in possible_words:
        score = 0
        for c in word:
            score += freq[c]
        scores.append(score)
    
    # print(scores)

    return possible_words[scores.index(min(scores))]
    

    ''
    SORTS ALL GUESSES BY FREQ. CURRENTLY ONLY RETURN ONE GUESS

    for i in range(len(scores)):
        index = scores.index(min(scores))
        ret.append(possible_words[index])
        scores[index] = 125 # won't ever have a word with freq this high so set it to not include it on the next iteration
        
    return ret
    '''
        

def read_words():
    ret = []
    for entry in open("valid_words.txt", "r"):
        ret.append(entry.strip("\n"))
    return ret
    


class Game():

    def __init__(self, valid_words):
        self.words = valid_words
        self.solution = random.choice(valid_words)
        self.grey_letters = []
        self.yellow_letters = [[], [], [], [], []]
        self.green_letters = {}
        self.guesses = 0

    def makeGuess(self, guess):
        # updates the state after making the guess passed as guess

        # updates internal collections 
        self.__readGuess__(guess)

        # updates internal words array to only include possible solutions given green, yellow, and grey letters
        self.words = self.__getPossibleWords__(self.words, self.green_letters, self.yellow_letters, self.grey_letters)
        self.guesses += 1

    def __readGuess__(self, guess):
        # compares guess against solution to update green, yellow, and grey letters collections

        for i in range(5):
            # green letter check
            if self.solution[i] == guess[i]:
                self.green_letters[guess[i]] = i
            
            # yellow letter check
            elif guess[i] in self.solution:
                if not (guess[i] in self.yellow_letters[i]):
                    self.yellow_letters[i].append(guess[i])

            # grey letter
            else:
                if not (guess[i] in self.grey_letters):
                    self.grey_letters.append(guess[i])
    
    def __getPossibleWords__(self, words, green_letters, yellow_letters, grey_letters):
        ret = []
        
        for word in words:
            valid = True
            
            for let in grey_letters:
                # candidate word contains a letter it cannot have
                if word.find(let) != -1:
                    valid = False
                    break
                
            if not valid:
                continue
            
            for let in green_letters:
                if word[green_letters[let]] != let:
                    # candidate word does not have a green letter in correct index
                    valid = False
                    break
            
            if not valid:
                continue
            
            for i in range(4):
                for let in yellow_letters[i]:
                    if let == word[i]:
                        # candidate word contains a yellow letter at specificed location
                        # or candidate word does not contain the yellow letter anywhere else
                        valid = False
                        break
            
            if not valid:
                continue
            
            ret.append(word)
        
        return ret

    def getNextGuess(self):
        # list of the letters sorted by frequency
        freq = {'e': 0, 't':1, 'a':2, 'o':3, 'n':4, 'i':5, 'h':6, 's':7, 'r':8, 'l':9, 'd':10, 'u':11, 'c':12,
                'm':13, 'w':14, 'y':15, 'f':16, 'g':17, 'p':18, 'b':19, 'v':20, 'k':21, 'j':22, 'x':23, 'q':24, 'z':25}

        scores = []
        # assign each word a "score" which is defined as the sum of the freq of each letters
        # the score of a single letter is given by its corresponding key:value pair (e.g., e is 0 and z is 25)
        # the word with the least score includes the most frequently used characters and will be used as the next guess
        for word in self.words:
            score = 0
            for c in word:
                score += freq[c]
            scores.append(score)
        

        # return self.words[scores.index(min(scores))] can compute index and min at the same time if manual:
        index = 0
        min = 200
        for i in range(len(scores)):
            if scores[i] < min:
                min = scores[i]
                index = i
        
        return self.words[index]


            

def create_game_window():
      app = App()
      app.mainloop()
      return app

def main():
    create_game_window()
    
      

if __name__ == "__main__":
    main()
    
    '''
    FOR ALL POSSIBLE GUESSES 

    words = []
    for entry in open("words.txt", "r"):
        words.append(entry.strip("\n"))
        
    green_letters, yellow_letters, grey_letters = read_input(words)
    possible_words = get_possible_words(words, green_letters, yellow_letters, grey_letters)
    guesses = sort_by_freq(possible_words)
    
    print(possible_words)
    print(guesses)
    print("\nonly valid words\n")

    green_letters, yellow_letters, grey_letters = read_input(valid_words)
    possible_words = get_possible_words(valid_words, green_letters, yellow_letters, grey_letters)
    guesses = guess(possible_words)

    valid_words = read_words()
    guesses = [0, 0, 0, 0, 0, 0, 0]
    failures = []

    for i in range(100):
        game = Game(valid_words)
        game.makeGuess(random.choice(game.words))
        while(game.guesses < 6):
            guess = game.getNextGuess()
            game.makeGuess(guess)
            if (guess == game.solution):
                break

        if guess != game.solution:
            guesses[6] += 1
            failures.append( [game.solution, guess] )
        else:
            guesses[game.guesses - 1] += 1
    
    print(guesses)
    print(failures)

    game = Game(valid_words)
    game.solution = "sworn"
    game.makeGuess("troop")
    while game.guesses < 6:
        guess = game.getNextGuess()
        game.makeGuess(guess)
        if (guess == game.solution):
            break
    print(game.guesses)
    print(guess)
    print(game.grey_letters)
    '''


    
    
        
                
                
    