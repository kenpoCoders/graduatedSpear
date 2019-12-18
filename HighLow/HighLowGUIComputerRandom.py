import random
import tkinter
import tkinter.messagebox
import tkinter.simpledialog
import time

wins = 0
loses = 0
noMessage = False

def getNumberTK(boxTitle,boxQuestion,defaultNum,minNum,maxNum):
  n = tkinter.simpledialog.askinteger(boxTitle,boxQuestion,
                                      minvalue=minNum,maxvalue=maxNum)
  if n == None:
    n = defaultNum
  return n

def goodPick( oldCard, newCard, pickedHigher ):
  faces = [ "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace" ]
  if faces.index( oldCard[0] ) < faces.index( newCard[0] ):
    if pickedHigher:
      return True
    else:
      return False
  elif faces.index( oldCard[0] ) > faces.index( newCard[0] ):
    if not pickedHigher:
      return True
    else:
      return False
  else:
    return True
  
def shuffle_deck( deck_of_cards ):
  shuffled_deck = []
  while len(deck_of_cards) > 0:
    card = random.choice( deck_of_cards )
    card_index = deck_of_cards.index( card )
    shuffled_deck.append( deck_of_cards.pop( card_index ) )
  return shuffled_deck

def revealCard(slot,card):
  cardFile = "./cards/" + card[0] + "_of_" + card[1] + ".png"
  cardImage = tkinter.PhotoImage(file=cardFile)
  cards[slot].configure( image = cardImage )
  cards[slot].image = cardImage
  root.update()
  ##time.sleep(0.3)

def resetCards():
  cardFile = "./cards/card_back.png"
  cardImage = tkinter.PhotoImage(file=cardFile)
  for slot in range(nCards):
    cards[slot].configure( image = cardImage )
    cards[slot].image = cardImage
  root.update()
  ##time.sleep(0.3)

def updateScore():
  global wins
  global loses
  winStr = "Total Wins: " + str(wins)
  loseStr = "Total Loses: " + str(loses)
  winLabel.configure( text = winStr )
  winLabel.text = winStr
  loseLabel.configure( text = loseStr )
  loseLabel.text = loseStr
  root.update()
  ##time.sleep(0.3)

def checkButtonClick():
  global noMessage
  if aiVar.get() == "computer":
    tkinter.messagebox.showinfo(title="Computer AI",message="You have chosen to let the computer play.")
    nPlays = getNumberTK("Number Computer Plays in a Row",
                         "How many times do you want the computer to play in a row?",
                         0,0,10000)
    root.update_idletasks()
    for i in range(nPlays):
      if i < (nPlays - 1):
        noMessage = True
      else:
        noMessage = False
      playGame()
      root.update()
      ##time.sleep(1)

def numCardsLessThanEqual( faceName, exposed_cards ):
  num = 0
  faces = [ "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace" ]
  for card in exposed_cards:
    if faces.index( card[0] ) <= faces.index( faceName ):
      num += 1
  return num

def numCardsGreaterThanEqual( faceName, exposed_cards ):
  num = 0
  faces = [ "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace" ]
  for card in exposed_cards:
    if faces.index( card[0] ) >= faces.index( faceName ):
      num += 1
  return num

def computerAI_pick( last_card, exposed_cards ):
  faces = [ "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace" ]
  if last_card[0] == "8":
    return random.choice( (True,False) )
  elif faces.index( last_card[0] ) <= faces.index( "8" ):
    return True
  else:
    return False

def computerAI_pick_random( faceName, exposed_cards ):
  return random.choice( (True,False) )
  
def playGame():
  global wins
  global loses
  global noMessage
  resetCards()
  faces = [ "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace" ]
  suits = [ "diamonds", "spades", "hearts", "clubs" ]
  deck_of_cards = []
  for suit in suits:
    for face in faces:
      deck_of_cards.append( (face,suit) )
  deck_of_cards = shuffle_deck( deck_of_cards )
  exposed_cards = []
  last_card = 0
  new_card = 1
  revealCard( last_card, deck_of_cards[last_card] )
  exposed_cards.append( deck_of_cards[last_card] )
  msg = ""
  for i in range(4):
    HoL = True
    if aiVar.get() == "computer":
      HoL = computerAI_pick_random( deck_of_cards[last_card][0], exposed_cards )
      ##print ("last card = ", last_card)
      ##print ("Picked High = ", HoL)
    else:
      HoL = tkinter.messagebox.askyesno(title="High or Low",message="Is the next card going to be higher?")
    if aiVar.get() != "computer":
      revealCard( new_card, deck_of_cards[new_card] )
    exposed_cards.append( deck_of_cards[new_card] )
    ##print ("Card is",deck_of_cards[new_card])
    if not goodPick( deck_of_cards[last_card], deck_of_cards[new_card], HoL ):
      msg = "You Lose!"
      loses += 1
      break
    elif ( i == 3 ):
      msg = "Good job. You win!"
      wins += 1
    last_card = new_card
    new_card += 1
  updateScore()
  if not noMessage:
    tkinter.messagebox.showinfo(title="Result",message=( msg + "\nPush Play to try again?"))

if __name__ == "__main__":

  root = tkinter.Tk()
  
  root.title("High or Low")
  root.geometry("+40+40")

  cards = []
  cardBackImage = tkinter.PhotoImage(file="./cards/card_back.png")
  nCards = 5
  for i in range(nCards):
    cards.append(tkinter.Label(image=cardBackImage))
    cards[-1].grid(row=0,column=i,rowspan=4)


  aiVar = tkinter.StringVar()
  aiButton = tkinter.Checkbutton(root,text="Let Computer Play", variable=aiVar,
                                 onvalue="computer", offvalue="user", command=checkButtonClick )
  aiButton.deselect()
  aiButton.grid(row=0,column=nCards)

  winLabel = tkinter.Label(text= "Total Wins: 0" )
  winLabel.grid(row=1,column=nCards)

  loseLabel = tkinter.Label(text= "Total Loses: 0" )
  loseLabel.grid(row=2,column=nCards)

  playB = tkinter.Button(text="Play",command=playGame)
  playB.grid(row=3,column=nCards)

  root.mainloop()
