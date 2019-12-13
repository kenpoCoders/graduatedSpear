import random

def goodPick( oldCard, newCard, HoL ):
  faces = [ "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace" ]
  pickedHigher = False
  if ( HoL == "h" ):
    print ("You picked higher.")
    pickedHigher = True
  elif ( HoL == "l" ):
    print ("You picked lower.")
  if faces.index( oldCard[0] ) < faces.index( newCard[0] ):
    ## High Card
    if pickedHigher:
      return True
    else:
      return False
  elif faces.index( oldCard[0] ) > faces.index( newCard[0] ):
    ## Low Card
    if not pickedHigher:
      return True
    else:
      return False
  else:
    ## Tie
    print ("Tie")
    return True
  

def shuffle_deck( deck_of_cards ):
  shuffled_deck = []
  while len(deck_of_cards) > 0:
    card = random.choice( deck_of_cards )
    card_index = deck_of_cards.index( card )
    shuffled_deck.append( deck_of_cards.pop( card_index ) )
  return shuffled_deck
 
if __name__ == "__main__":

  faces = [ "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king", "ace" ]
  suits = [ "diamonds", "spades", "hearts", "clubs" ]

  deck_of_cards = []

  for suit in suits:
    for face in faces:
      deck_of_cards.append( (face,suit) )

  deck_of_cards = shuffle_deck( deck_of_cards )

  last_card = 0
  new_card = 1

  for i in range(4):
    print ( "Last Card is ", deck_of_cards[last_card] )
    HoL = input("Type h for higher and l for lower. ")
    print ( "New Card is ", deck_of_cards[new_card] )
    if not goodPick( deck_of_cards[last_card], deck_of_cards[new_card], HoL ):
      print ("You Lose! Bye.")
      break
    elif ( i == 3 ):
      print ("Good job. You win!")
    else:
      print ("Good Job. Keep going")
    last_card = new_card
    new_card += 1
