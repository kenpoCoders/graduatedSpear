import random
import tkinter
import tkinter.messagebox
import tkinter.simpledialog
import time

wins = 0
loses = 0
noMessage = False

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
  time.sleep(0.3)

def resetCards():
  cardFile = "./cards/card_back.png"
  cardImage = tkinter.PhotoImage(file=cardFile)
  for slot in range(nCards):
    cards[slot].configure( image = cardImage )
    cards[slot].image = cardImage
  root.update()
  time.sleep(0.3)

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
  time.sleep(0.3)
  
def playGame():
  global wins
  global loses
  resetCards()
  faces = [ "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace" ]
  suits = [ "diamonds", "spades", "hearts", "clubs" ]
  deck_of_cards = []
  for suit in suits:
    for face in faces:
      deck_of_cards.append( (face,suit) )
  deck_of_cards = shuffle_deck( deck_of_cards )
  last_card = 0
  new_card = 1
  revealCard( last_card, deck_of_cards[last_card] )
  msg = ""
  for i in range(4):
    HoL = tkinter.messagebox.askyesno(title="High or Low",message="Is the next card going to be higher?")
    revealCard( new_card, deck_of_cards[new_card] )
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

  winLabel = tkinter.Label(text= "Total Wins: 0" )
  winLabel.grid(row=1,column=nCards)

  loseLabel = tkinter.Label(text= "Total Loses: 0" )
  loseLabel.grid(row=2,column=nCards)

  playB = tkinter.Button(text="Play",command=playGame)
  playB.grid(row=3,column=nCards)

  root.mainloop()