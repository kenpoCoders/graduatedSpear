import sys


def checkInstallation(rv):
    currentVersion = sys.version_info
    if currentVersion[0] == rv[0] and currentVersion[1] >= rv[1]:
        pass
    else:
        sys.stderr.write( "[%s] - Error: Your Python interpreter must be %d.%d or greater (within major version %d)\n" % (sys.argv[0], rv[0], rv[1], rv[0]) )
        sys.exit(-1)
    return 0

checkInstallation((3,0))

import random
import tkinter
import tkinter.messagebox
import tkinter.simpledialog
import time

def playGame():
  #print ("Roll Dice")
  global gameon
  global tstart
  global tend
  rollDice()
  if checkForWin():
    tend = time.time()
    gameon = False
    gtime = tend - tstart
    topTen = readInTopTen()
    topTen[ gtime ] = "TEST"
    topTenTimes = sorted(topTen.keys())
    ti = topTenTimes.index( gtime )
    if ti < 10:
      name = getName()
      topTen[ gtime ] = name
      writeTopTen( topTen )
    topTenMsg = "--- Top Ten Times ---\n"
    nt = len( topTenTimes )
    for i in range(nt):
      tm = topTenTimes[i]
      tm_str = "%.3f" % tm
      topTenMsg += str(i+1) + ": " + topTen[tm] + ", " + tm_str + " seconds\n"
      if i == 9:
        break
    tkinter.messagebox.showinfo(title="Result",message=( "Fivezi!!!!\n" +
                                                         "You won in " + str(gtime) + " seconds.\n" +
                                                         topTenMsg +
                                                         "Play Again" ) )
    resetHold()
    resetDice()

def getName():
  n = tkinter.simpledialog.askstring("Fivezi: Player Name","You are in the top ten.\nPlease enter your name:")
  n = n.replace(","," ")
  if n == None or n == "":
    n = "Fred"
  return n

def readInTopTen():
  f = open("./FiveziTopTen.txt",'r')
  lines = f.readlines()
  f.close()
  n = len(lines)
  topTen = {}
  if n < 10:
    print ("ERROR: Bad Top Ten File.")
    return topTen
  for i in range(10):
    ( name, time ) = lines[i].split(",")
    topTen[ float(time) ] = name
  return topTen

def writeTopTen(topTen):
  f = open("./FiveziTopTen.txt",'w')
  keys = sorted(topTen.keys())
  for i in range(10):
    k = keys[i]
    f.write( topTen[k] + ", " + str(k) + "\n" )
  f.close()

def checkForWin():
  myDiceVals = diceValue[:]
  myDiceVals.sort()
  if myDiceVals[0] == 0:
    return False
  if myDiceVals[0] == myDiceVals[-1]:
    return True
  return False

def dicePicFile( num ):
  colors = ["black","green","darkGreen"]
  rColor = random.choice(colors)
  fileName = "./dice/" + str(num) + "_" + rColor + ".png"
  return fileName

def resetDice():
  for slot in range(nDice):
    diceValue[ slot ] = 0
    diceFile = dicePicFile( 0 )
    diceImage = tkinter.PhotoImage(file=diceFile)
    diceLabel[slot].configure( image = diceImage )
    diceLabel[slot].image = diceImage
  root.update()

def resetHold():
  for i in range(nDice):
    diceRollButtons[i].deselect()

def rollDice():
  global gameon
  global tstart
  if not gameon:
    gameon = True
    tstart = time.time()
  for slot in range(nDice):
    ##print (diceRoll[slot].get())
    if diceRoll[slot].get() == "roll":
      diceValue[ slot ] = random.randint(1,6);
      diceFile = dicePicFile( diceValue[slot] )
      diceImage = tkinter.PhotoImage(file=diceFile)
      diceLabel[slot].configure( image = diceImage )
      diceLabel[slot].image = diceImage
  root.update()
  
def diceHoldFunk():
  ## Place holder
  return

def dice0():
  if diceRoll[0].get() == "roll":
    diceRollButtons[0].select()
  else:
    diceRollButtons[0].deselect()

def dice1():
  if diceRoll[1].get() == "roll":
    diceRollButtons[1].select()
  else:
    diceRollButtons[1].deselect()

def dice2():
  if diceRoll[2].get() == "roll":
    diceRollButtons[2].select()
  else:
    diceRollButtons[2].deselect()

def dice3():
  if diceRoll[3].get() == "roll":
    diceRollButtons[3].select()
  else:
    diceRollButtons[3].deselect()

def dice4():
  if diceRoll[4].get() == "roll":
    diceRollButtons[4].select()
  else:
    diceRollButtons[4].deselect()

if __name__ == "__main__":
  
  root = tkinter.Tk()

  global tstart
  global tend
  global gameon
  gameon = False

  root.title("Fivezi")
  root.geometry("+200+200")

  diceLabel = []
  diceValue = []
  diceRoll = []
  diceRollButtons = []

  nDice = 5
  diceFuncs = [ dice0, dice1, dice2, dice3, dice4 ]
  for i in range(nDice):
    diceValue.append( 0 )
    diceLabel.append( tkinter.Button( command=diceFuncs[i]) )
    diceLabel[-1].grid(row=0,column=i)
  resetDice()

  for i in range(nDice):
    diceRoll.append( tkinter.StringVar() )
    diceRollButtons.append( tkinter.Checkbutton(root,text="Hold", variable=diceRoll[-1],
                                 onvalue="hold", offvalue="roll", command=diceHoldFunk ) )
    diceRollButtons[-1].deselect()
    diceRollButtons[-1].grid(row=1,column=i)

  playB = tkinter.Button(text="Roll",command=playGame)
  playB.grid(row=0,column=nDice)
  root.update()

  root.mainloop()
