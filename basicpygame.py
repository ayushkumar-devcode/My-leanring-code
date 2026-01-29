import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
BOARD_SIZE = 10
CELL_SIZE = 60
BOARD_WIDTH = BOARD_SIZE * CELL_SIZE
BOARD_HEIGHT = BOARD_SIZE * CELL_SIZE
SCREEN_WIDTH = BOARD_WIDTH + 200
SCREEN_HEIGHT = BOARD_HEIGHT
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snakes & Ladders with Portals")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 18)

class Player:
    def __init__(self, color, start_pos=0):
        self.pos = start_pos
        self.color = color

def draw_board(screen):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            x = col * CELL_SIZE
            y = row * CELL_SIZE if row % 2 == 0 else (BOARD_SIZE - 1 - col) * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
            
            # Number label (boustrophedon numbering)
            num = row * 10 + col + 1 if row % 2 == 0 else row * 10 + (9 - col) + 1
            text = small_font.render(str(num), True, BLACK)
            screen.blit(text, (x + 25, y + 20))

def generate_portals(num_portals=5):
    portals = {}
    used = set()
    while len(portals) < num_portals:
        start = random.randint(1, 99)
        if start in used:
            continue
        end = random.randint(1, 100)
        if end == 100 or end in used or end == start:
            continue
        portals[start] = end
        used.add(start)
        used.add(end)
    return portals

# Fixed snakes and ladders
snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

# Portals override snakes/ladders if conflict
portals = generate_portals()

def get_final_pos(pos):
    # Check portals first
    if pos in portals:
        return portals[pos]
    # Then snakes/ladders
    if pos in snakes:
        return snakes[pos]
    if pos in ladders:
        return ladders[pos]
    return pos

def pos_to_coords(pos):
    if pos == 0:
        return (10 * CELL_SIZE // 2, BOARD_HEIGHT - 50)
    pos -= 1
    row = pos // 10
    col = pos % 10
    if row % 2 == 0:
        x = col * CELL_SIZE + CELL_SIZE // 2
    else:
        x = (9 - col) * CELL_SIZE + CELL_SIZE // 2
    y = row * CELL_SIZE + CELL_SIZE // 2
    return (x, y)

def draw_player(screen, player):
    x, y = pos_to_coords(player.pos)
    pygame.draw.circle(screen, player.color, (x, y), 20)

def draw_dice(screen, roll):
    dice_rect = pygame.Rect(BOARD_WIDTH + 20, 100, 120, 120)
    pygame.draw.rect(screen, WHITE, dice_rect)
    pygame.draw.rect(screen, BLACK, dice_rect, 3)
    dots = [
        ((40,40), (80,80)),  # 1
        ((40,40), (80,80)),  # 2 -> adjust
    ]
    # Simplified dice dots for 1-6
    dot_positions = {
        1: [(60,60)],
        2: [(30,30), (90,90)],
        3: [(30,30), (60,60), (90,90)],
        4: [(30,30), (30,90), (90,30), (90,90)],
        5: [(30,30), (30,90), (60,60), (90,30), (90,90)],
        6: [(30,30), (30,60), (30,90), (90,30), (90,60), (90,90)]
    }
    for dx, dy in dot_positions.get(roll, []):
        pygame.draw.circle(screen, BLACK, (BOARD_WIDTH + dx, 120 + dy), 8)

def draw_portals(screen, portals):
    for start, end in portals.items():
        sx, sy = pos_to_coords(start)
        ex, ey = pos_to_coords(end)
        pygame.draw.line(screen, PURPLE, (sx, sy), (ex, ey), 5)
        pygame.draw.circle(screen, PURPLE, (sx, sy), 15)

# Game setup
player = Player(RED, 0)
dice_roll = 0
rolling = False
message = "Click dice or SPACE to roll!"

running = True
while running:
    screen.fill((200, 200, 255))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                rolling = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if BOARD_WIDTH + 20 <= mx <= BOARD_WIDTH + 140 and 100 <= my <= 220:
                rolling = True
    
    if rolling:
        dice_roll = random.randint(1, 6)
        new_pos = min(100, player.pos + dice_roll)
        player.pos = get_final_pos(new_pos)
        rolling = False
        if player.pos == 100:
            message = "You Win! 🎉"
        else:
            message = f"Rolled {dice_roll}! New position: {player.pos}"
    
    # Draw everything
    draw_board(screen)
    draw_portals(screen, portals)
    draw_player(screen, player)
    draw_dice(screen, dice_roll)
    
    # UI text
    score_text = font.render(f"Position: {player.pos}", True, BLACK)
    screen.blit(score_text, (BOARD_WIDTH + 20, 250))
    msg_text = font.render(message, True, BLUE)
    screen.blit(msg_text, (BOARD_WIDTH + 20, 300))
    
    # Instructions
    inst_text = small_font.render("SPACE or click dice to roll", True, BLACK)
    screen.blit(inst_text, (BOARD_WIDTH + 20, 50))
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()