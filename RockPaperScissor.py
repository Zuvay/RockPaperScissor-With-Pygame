import pygame
import random
import sys
import sqlite3

#Screen
WIDTH, HEIGHT = 800,600
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("RockPaperScissor Game")


#Color
WHITE = (255,255,255)
BLACK = (0,0,0)

OPTIONS = ["Rock","Paper","Scissor"]


#for images
PLAYER_IMAGES = {"Rock":pygame.image.load("img/rock.png"),
                "Paper":pygame.image.load("img/paper.png"),
                "Scissor":pygame.image.load("img/scissors.png")}
COMPUTER_IMAGES = {"Rock":pygame.image.load("img/rock.png"),
                "Paper":pygame.image.load("img/paper.png"),
                "Scissor":pygame.image.load("img/scissors.png")}

# SQLite connection
conn = sqlite3.connect('streaks.db')
# Create cursor
cursor = conn.cursor()
# Create a table if not exist
cursor.execute('''CREATE TABLE IF NOT EXISTS streak (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    current_streak INTEGER
                )''')
#insert the current streak
def update_streak(current_streak):
    cursor.execute('''INSERT INTO streak (current_streak) VALUES (?)''', (current_streak,))
    conn.commit()

def get_highest_score():
    # Veritabanındaki en yüksek skoru al
    cursor.execute('''SELECT MAX(current_streak) FROM streak''')
    highest_score = cursor.fetchone()[0]
    return highest_score
highest_score = get_highest_score()

def draw_opening_screen():
    WIN.fill(WHITE)
    
    font = pygame.font.SysFont(None, 36)
    welcome_text = font.render("Welcome", True, BLACK)
    welcome_text_rect = welcome_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    WIN.blit(welcome_text, welcome_text_rect)

    instruction_text = font.render("Press 'r(rock)', 's(scissor)' or 'p(paper)' to start & Press ESC to exit", True, BLACK)
    instruction_text_rect = instruction_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
    WIN.blit(instruction_text, instruction_text_rect)

    pygame.display.update()

#Determine winner
def determine_winner(player_choice, computer_choice):
    if player_choice == computer_choice:
        return "Draw"
    elif (player_choice == "Rock" and computer_choice == "Scissor") or \
         (player_choice == "Paper" and computer_choice == "Rock") or \
         (player_choice == "Scissor" and computer_choice == "Paper"):
        return "Player win"
    else:
        return "Computer win"
        
#Update Screen
def draw(player_choice, computer_choice, winner,current_streak):
    WIN.fill(WHITE) #Screen covered with white
    player_img = PLAYER_IMAGES[player_choice]
    computer_img = COMPUTER_IMAGES[computer_choice]
    WIN.blit(player_img,(100,200)) #placed image
    WIN.blit(computer_img,(500,200)) #placed computer's image

    font = pygame.font.SysFont(None,50) #Default font and 50px font size
    text = font.render(winner,True,BLACK)

    pygame.font.SysFont(None,50) #Default font and 50px font size
    text = font.render(winner,True,BLACK)
    WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT - 100))

    # Player text
    player_text = font.render("Player", True, BLACK)
    player_text_rect = player_text.get_rect(center=(100 + player_img.get_width() // 2, 200 + player_img.get_height() + 10))
    WIN.blit(player_text, player_text_rect)

    # computer text
    computer_text = font.render("Computer", True, BLACK)
    computer_text_rect = computer_text.get_rect(center=(500 + computer_img.get_width() // 2, 200 + computer_img.get_height() + 10))
    WIN.blit(computer_text, computer_text_rect)

    streak_text = font.render(f"Streak: {current_streak}", True, BLACK)
    WIN.blit(streak_text, (20, 20))

    score_text = font.render(f"Highest Score: {highest_score}", True, BLACK)
    WIN.blit(score_text, (20, 50))

    pygame.display.update() #update screen


def main():
    pygame.init()
    clock = pygame.time.Clock() 
    draw_opening_screen()
    current_streak = 0
    running = True
    while running:
        for event in pygame.event.get(): #This line initiates a loop to retrieve events from the Pygame event queue. Checks mouse and keyboards
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()


            if event.type == pygame.KEYDOWN: #when you use keyboard game progresses
                if event.key == pygame.K_ESCAPE: #when you press ESC button the game stop
                    running = False
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_r:
                    player_choice = "Rock"
                elif event.key == pygame.K_p:
                    player_choice = "Paper"
                elif event.key == pygame.K_s:
                    player_choice = "Scissor"

                computer_choice = random.choice(OPTIONS)
                winner = determine_winner(player_choice, computer_choice)
                if winner == "Player win":
                    current_streak += 1
                else:
                    update_streak(current_streak)
                    current_streak = 0
                draw(player_choice, computer_choice, winner, current_streak)
                
        clock.tick(60)

if __name__ == "__main__":
    main()