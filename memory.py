#This is an implementation of the card game 'Memory' usign simplegui
import simplegui
import random

#initialize globals
list_1 = range(0,8)
list_2 = range(0,8)
concat = list_1 + list_2 #concatenation of two lists (card numbers)
exposed = [False for i in range(16)] #tracks if card is exposed
state = 0
flip_1 = 0
flip_2 = 0
click = 0
nums = range(0,800,50) #increments pixels by 50 so ranges can be made in the next list comprehension
list = [range(i,i+50) for i in nums] #makes a list of range positions corresponding to horizontal pixels to track where on the canvas a click has taken place
match = True #initializes the match indicator
turn = 0

# helper function to initialize globals
def new_game():
    '''event handler to restart the game'''
    
    random.shuffle(concat) #reshuffles the deck
    global state
    global turn
    global exposed
    turn = 0 #resets the turn counter
    state = 0 #resets the counter that tracks how many clicks there are in each turn
    exposed = [False for i in range(16)] #tracks if card is exposed
  

    
def mouseclick(pos):
    '''event handler called every time the mouse is clicked, includes the game logic'''
    
    global state
    global flip_1, flip_2
    global click
    global match
    global turn
    click += 1 #increments to track the number of clicks
    for idx,element in enumerate(list):
        if pos[0] in list[idx] and exposed[idx] is False: #compares the mouse positon to the ranges that correspond to card positions and whether or not that card has been exposed
            exposed[idx] = True #reveals the card corresponding to the area of the frame clicked
            if state == 0:
                state = 1
                flip_1 = idx #tracks index of first card flipped
            elif state == 1: #when state = 1, a turn has ended (two subsequent card flips)
                state = 2
                turn += 1 #iterates to track the turn
                flip_2 = idx #tracks index of second card flipped
                if concat[flip_1] != concat[flip_2]: #determines whether two subsequent card flips are a match
                    match = False #if not, sets global variable match to False
                else:  #if they are a match...
                    match = True #...sets global to True
            else: #if state == 2 (e.g., end of a turn)
                if match is False and click % 2 == 1: #if there is no match and the # of clicks is odd (minus the first click)
                    exposed[flip_1] = False #flips non-matched revealed cards back over
                    exposed[flip_2] = False
                flip_1 = idx #tracks the index of the first card flipped in the next turn
                state = 1 #resets global state variable

                            
# cards are logically 50x100 pixels in size    
def draw(canvas):
    '''event handler to draw on the canvas (updates 60x/sec)'''
    
    j = 0
    global turn
    label.set_text("Turns = " + str(turn)) #updates the turn counter label
    for idx,card in enumerate(concat):
        if exposed[idx] is True: #if the card is exposed...
            canvas.draw_text(str(card),[12+(50 * idx),70], 50, 'White') #draw the number underneath
            j += 50 #incrementing j
        else: #if card is not exposed...
            canvas.draw_polygon([[0+j,0],[50+j,0],[50+j,100],[0+j,100]], 2, 'Black','Green') #draw a green rectangle
            j += 50 #incrementing j to move the drawing of the cards horizontally by increments

# creating frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = ")


# registering event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# getting things rolling
new_game()
frame.start()