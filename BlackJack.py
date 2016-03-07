# Mini-project #6 - Blackjack

import simplegui
import random

WH = [600, 600]

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://i.imgur.com/MfGvt7J.png?1?6968?dl=1")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
color = "White"

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}
dc = ""
pc = ""

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class
class Hand:
    def __init__(self):
        self.cards = []
        #self.is_dealer = is_dealer

    def __str__(self):
        hmsg = "Hand:"
        for card in self.cards:
            hmsg = hmsg + " " + str(card)
        return hmsg

    def add_card(self, card):
        self.cards.append(card)

    def get_value(self):
        A = []
        cards_sum = int()
        for card in self.cards:
            cards_sum += VALUES[card.get_rank()]
            if card.get_rank() == "A":
                A.append(True)
            else:
                A.append(False)
#        print A, cards_sum
        if (A[0] or A[1]) and (cards_sum + 10 <= 21):
            return cards_sum + 10
        if (A[0] or A[1]) and (cards_sum + 10 > 21):
            return cards_sum
        elif (A[0] and A[1] and A[2] in A) and (A[0] or A[1] or A[2]) and (cards_sum + 10 <= 21):
            return cards_sum + 10
        elif (A[0] and A[1] and A[2] and A[3] in A) and (cards_sum + 10 <= 21):
            return cards_sum + 10
        else:
            return cards_sum
        
    def draw(self, canvas, pos):
        next_card = int()
        for card in self.cards:
            if in_play and next_card == int() and pos[1] == 250:
                canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,[pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
            else:
                card.draw(canvas, [pos[0] + next_card * CARD_SIZE[0] * 0.5, pos[1] + next_card * CARD_SIZE[1] * 0.1])
            next_card += 1

# define deck class 
class Deck:
    def __init__(self):
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        self.used = int()
        random.shuffle(self.cards)

    def deal_card(self):
        self.used -= 1
        return self.cards[self.used]
    
    def __str__(self):
        dmsg = "Deck:"
        for card in self.cards:
            dmsg = dmsg + " " + str(card)
        return dmsg

#define event handlers for buttons
def deal():
    global outcome, in_play, score, color, dc, pc
    player_cards.cards = []
    dealer_cards.cards = []
    d.shuffle()
    player_cards.add_card(d.deal_card())
    player_cards.add_card(d.deal_card())
    dealer_cards.add_card(d.deal_card())
    dealer_cards.add_card(d.deal_card())
    dc = ""
    pc = ""
    if in_play:
        color = "Black"
        outcome = "You loose. Wanna new deal?"
        score -= 1
    in_play = True
    color = "White"
    outcome = "Choose: hit or stand"

def hit():
    global outcome, score, in_play, color, dc, pc
    if in_play:
        player_cards.add_card(d.deal_card())
        if player_cards.get_value() <= 21:
            color = "White"
            outcome = "Choose: hit or stand"
        else:
            color = "Black"
            outcome = "Busted! You loose. New deal?"
            score -= 1
            in_play = False
            dc = dealer_cards.get_value()
            pc = player_cards.get_value()
       
def stand():
    global outcome, score, in_play, color, dc, pc
    if in_play:
        in_play = False
        if player_cards.get_value() <= 21:
            while dealer_cards.get_value() < 17:
                dealer_cards.add_card(d.deal_card())
            if dealer_cards.get_value() > 21:
                color = "#6fcd4a"
                outcome = "Dealer busts! You win. New deal?"
                score += 1
            elif dealer_cards.get_value() == 21:
                color = "Black"
                outcome = "Busted! You loose. New deal?"
                score -= 1
            elif player_cards.get_value() > dealer_cards.get_value():
                color = "#6fcd4a"
                outcome = "Dealer busts! You win. New deal?"
                score += 1
            elif player_cards.get_value() <= dealer_cards.get_value():
                color = "Black"
                outcome = "Busted! You loose. New deal?"
                score -= 1
        elif player_cards.get_value() > 21:
            color = "Black"
            outcome = "Busted! You loose. New deal?"
    dc = dealer_cards.get_value()
    pc = player_cards.get_value()
    # Check cards and game status
#    print player_cards.get_value(), dealer_cards.get_value()
#    if color == "Black":
#        print "A shameful DEFEAT!"
#        print
#    else:
#        print "A glorious VICTORY!"
#        print

# draw handler    
def draw(canvas):
    canvas.draw_text("BlackJack", [100, 100], 60, "White")
    canvas.draw_text("Game score: " + str(score), [100, 130], 16, "White")
    canvas.draw_text(outcome, [100, 160], 20, color)
    canvas.draw_text("Dealer: " + str(dc), [100, 240], 20, "White")
    dealer_cards.draw(canvas, [100, 250])
    canvas.draw_text("Your cards: " + str(pc), [100, 420], 20, "White")
    player_cards.draw(canvas, [100, 430])

player_cards = Hand()
dealer_cards = Hand()
d = Deck()

# initialization frame
frame = simplegui.create_frame("Blackjack", WH[0], WH[1])
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()