import copy
import random 
import pygame

pygame.init()
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
one_deck = 4 * cards
decks = 4 
game_deck = copy.deepcopy(one_deck * decks) 
WIDTH = 600 
HEIGHT = 700
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Pygame Blackjack')
fps = 60 
timer = pygame.time.Clock()
font = pygame.font.Font(None, 44)
small_font = pygame.font.Font(None, 30)
active = False

# W/L or push 

records = [0, 0, 0]
user_score = 0  
dealer_score = 0 
initial_deal = False
my_hand = []
dealer_hand = []
outcome = 0 
reveal_dealer = False #remember this has to be false 
hand_active = False 
outcome = 0
add_score = False
results = ['Busted','You win', 'dealer win', 'push']

def deal_cards(current_hand, current_deck):
    # Fixing the index issue
    card = random.randint(0, len(current_deck) - 1)  
    current_hand.append(current_deck[card])  # Adds card to hand 
    current_deck.pop(card)  # Remove the card from the deck so no dupes
    return current_hand, current_deck

def calc_score(hand):  # sees how many aces u get 
    hand_score = 0 
    aces_count = hand.count('A')
    
    for i in range(len(hand)):
        for j in range(8):  # we are getting first 8 of cards
            if hand[i] == cards[j]:
                hand_score += int(hand[i])  # turns them into integars  
        
        # Adds 10 for face cards and '10'
        if hand[i] in ['10', 'J', 'Q', 'K']:
            hand_score += 10 
        
        # Ace starts by adding 11
        elif hand[i] == 'A':  
            hand_score += 11

    # Check if aces need to be reduced to 11 to 1 to get best chance of winnnig
    if hand_score > 21 and aces_count > 0:
        for i in range(aces_count):
            if hand_score > 21:
                hand_score -= 10  # Each ace - 10 score if over 21 
    
    return hand_score

# Game condition and buttons  
def draw_game(act, record, result):
    button_list = []
    
    # shows deal hand as the only option
    if not act: 
        deal = pygame.draw.rect(screen, 'white', [150, 20, 200, 80], 0, 5)  # deal
        pygame.draw.rect(screen, 'green', [150, 20, 200, 80], 3, 5)
        deal_text = font.render('DEAL HAND', True, 'black')
        screen.blit(deal_text, (165, 40))
        button_list.append(deal)
        
    
    else: 
        hit = pygame.draw.rect(screen, 'white', [0, 500, 290, 80], 0, 5)  #hit
        pygame.draw.rect(screen, 'green', [0, 500, 290, 80], 3, 5)
        hit_text = font.render('HIT', True, 'black')  
        screen.blit(hit_text, (55, 530))  
        button_list.append(hit)
        
        stand = pygame.draw.rect(screen, 'white', [300, 500, 290, 80], 0, 5)   #stand
        pygame.draw.rect(screen, 'green', [300, 500, 290, 80], 3, 5)
        stand_text = font.render('STAND', True, 'black')  
        screen.blit(stand_text, (355, 530))  
        button_list.append(stand)

        score_text = small_font.render(f'Wins: {record[0]}    Losses: {record[1]}   Draws: {record[2]}', True, 'white')
        screen.blit(score_text, (15, 640))
    
    # displays result
    if result != 0: 
        result_text = font.render(results[result], True, 'white')  # Display the results
        screen.blit(result_text, (15, 25))  # Place the result in the top-left corner
        deal = pygame.draw.rect(screen, 'white', [150, 220, 200, 80], 3, 5)  
        pygame.draw.rect(screen, 'black', [150, 220, 200, 80], 3, 5)
        deal_text = font.render('NEW HAND', True, 'black')
        screen.blit(deal_text, (160, 240))
        button_list.append(deal)
    
    return button_list

def draw_scores(player, dealer):
    screen.blit(font.render(f'score[{player}]', True, 'white'), (40, 200)) 
    if reveal_dealer:
        screen.blit(font.render(f'score[{dealer}]', True, 'white'), (400, 200)) 

def draw_cards(player, dealer, reveal):
    for i in range(len(player)):
        x_offset = 10 + (60 * i)  # horizontal spacing 
        pygame.draw.rect(screen, 'white', [x_offset, 300, 100, 150], 0, 5)  # Smaller card rectangle
        pygame.draw.rect(screen, 'black', [x_offset, 300, 100, 150], 5, 5)  # Card border
        screen.blit(font.render(player[i], True, 'black'), (x_offset + 15, 320))  # Value on top of the card
        screen.blit(font.render(player[i], True, 'black'), (x_offset + 15, 390))  # Value on bottom of the card

    for i in range(len(dealer)):
        dx_offset = 350+ (60 * i)  #spacing for card
        pygame.draw.rect(screen, 'white', [dx_offset, 300, 100, 150], 0, 5)  # Smaller card rectangle
        if i != 0 or reveal:
         screen.blit(font.render(dealer[i], True, 'black'), (dx_offset + 15, 320))  # Value on top of the card
         screen.blit(font.render(dealer[i], True, 'black'), (dx_offset + 15, 390))  # Value on bottom of the card
        else:
            screen.blit(font.render('???', True, 'black'), (dx_offset + 15, 320))  # Value on top of the card
            screen.blit(font.render('???', True, 'black'), (dx_offset + 15, 390))  # Value on bottom of the card
        pygame.draw.rect(screen, 'red', [dx_offset, 300, 100, 150], 5, 5)  # Card border

def check_endgame(hand_act, deal_score, play_score, result, totals, add):
    if not hand_act and deal_score >= 17:
        if play_score > 21:
            result = 1  # Busted
        elif dealer_score > 21:
            result = 2  # You win
        elif play_score > dealer_score:
            result = 2  # You win
        elif play_score < dealer_score:
            result = 3  # Dealer wins
        else:
            result = 4  # Push (draw)
        
        if add: 
            if result == 1 or result == 3:
                totals[1] += 1  # Loss or dealer win
            elif result == 2:
                totals[0] += 1  # Player win
            else:
                totals[2] += 1  # Draw
            add = False 
    return result, totals, add

run = True 
while run:
    timer.tick(fps)
    screen.fill('blue')
    
    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
            print(my_hand, dealer_hand)
        initial_deal = False

    if active:
       user_score = calc_score(my_hand)
       draw_cards(my_hand, dealer_hand, reveal_dealer)
       if reveal_dealer: 
           dealer_score = calc_score(dealer_hand)
           if dealer_score < 17: 
               dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
           
       draw_scores(user_score, dealer_score)
       
    outcome, records, add_score = check_endgame(hand_active, dealer_score, user_score, outcome, records, add_score)

    buttons = draw_game(active, records, outcome) 
    
    # clicks and buttons 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            run = False 
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos 
            if not active:
                if buttons[0].collidepoint(mouse_pos): 
                    active = True 
                    hand_active = True 
                    initial_deal = True 
                    reveal_dealer = False 
                    my_hand = [] 
                    dealer_hand = [] 
                    outcome = 0 
                    add_score = True 
            else:
                if buttons[0].collidepoint(mouse_pos) and hand_active:
                    my_hand, game_deck = deal_cards(my_hand, game_deck)
                    user_score = calc_score(my_hand)
                    if user_score > 21: 
                        reveal_dealer = True 
                        hand_active = False 
                if buttons[1].collidepoint(mouse_pos) and hand_active:
                    reveal_dealer = True
                    hand_active = False 
                if len(buttons) > 2: 
                    if buttons[2].collidepoint(mouse_pos) and not hand_active: 
                        active = False 

    pygame.display.flip() 

pygame.quit()

