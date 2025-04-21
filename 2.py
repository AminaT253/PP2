import pygame
import random
import sys
import psycopg2

# === Подключение к БД ===
conn = psycopg2.connect(
    host="localhost",
    database="suppliers",
    user="postgres",
    password="21071994",
    port="5432"
)
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        level INT DEFAULT 1
    )
""")
cur.execute("""
    CREATE TABLE IF NOT EXISTS user_score (
        username TEXT PRIMARY KEY,
        score INT DEFAULT 0
    )
""")
conn.commit()

username = input("Введите имя пользователя: ")
cur.execute("SELECT * FROM users WHERE username = %s", (username,))
if cur.fetchone() is None:
    cur.execute("INSERT INTO users VALUES (%s, 1)", (username,))
    cur.execute("INSERT INTO user_score VALUES (%s, 0)", (username,))
    level, score = 1, 0
    conn.commit()
    print("Пользователь добавлен.")
else:
    cur.execute("SELECT level FROM users WHERE username = %s", (username,))
    level = cur.fetchone()[0]
    cur.execute("SELECT score FROM user_score WHERE username = %s", (username,))
    score = cur.fetchone()[0]
    print(f"Добро пожаловать обратно, {username}! Уровень: {level} Очки: {score}")

pygame.init()

Screen_w, Screen_h = 600, 400
Cell_size = 20
screen = pygame.display.set_mode((Screen_w, Screen_h))
pygame.display.set_caption("Snake Game")
Clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 19)

Blue = (0, 0, 255)
Red = (255, 0, 0)
Yellow = (255, 255, 0)
Orange = (255, 165, 0)
Green = (0, 255, 0)
Black = (0, 0, 0)
White = (255, 255, 255)

Font = pygame.font.SysFont("Verdana", 25)

def draw_walls():
    pygame.draw.rect(screen, Blue, (0, 0, Screen_w, Cell_size))
    pygame.draw.rect(screen, Blue, (0, Screen_h - Cell_size, Screen_w, Cell_size))
    pygame.draw.rect(screen, Blue, (0, 0, Cell_size, Screen_h))
    pygame.draw.rect(screen, Blue, (Screen_w - Cell_size, 0, Cell_size, Screen_h))

class Food():
    def __init__(self, snake, speed):
        self.value = random.choice([1, 3, 5])
        self.color = {1: Yellow, 3: Orange, 5: Red}[self.value]
        self.position = self.generate_position(snake)
        self.timer = 5 * speed

    def generate_position(self, snake):
        while True:
            x = random.randint(1, (Screen_w - Cell_size * 2) // Cell_size) * Cell_size
            y = random.randint(1, (Screen_h - Cell_size * 2) // Cell_size) * Cell_size
            if (x, y) not in snake:
                return (x, y)

    def draw(self):
        pygame.draw.rect(screen, self.color, (*self.position, Cell_size, Cell_size))

    def update_timer(self):
        self.timer -= 1
        return self.timer <= 0

def pause_and_save(level, score):
    cur.execute("UPDATE users SET level = %s WHERE username = %s", (level, username))
    cur.execute("UPDATE user_score SET score = %s WHERE username = %s", (score, username))
    conn.commit()
    paused = True
    print("Пауза. Нажмите P для продолжения.")
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused = False
                print("Игра продолжается.")

def start_screen():
    screen.fill(White)
    title = Font.render("Snake Game", True, Blue)
    subtitle = font.render("Нажмите ENTER, чтобы начать", True, Black)
    screen.blit(title, (Screen_w // 2 - 100, Screen_h // 2 - 60))
    screen.blit(subtitle, (Screen_w // 2 - 150, Screen_h // 2))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  
                    waiting = False

def game():
    global level, score
    snake = [(Cell_size * 10, Cell_size * 10)]
    direction = (Cell_size, 0)
    speed = 2 + level * 2
    food = Food(snake, speed)

    while True:
        screen.fill(White)
        draw_walls()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pause_and_save(level, score)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, Cell_size):
                    direction = (0, -Cell_size)
                elif event.key == pygame.K_DOWN and direction != (0, -Cell_size):
                    direction = (0, Cell_size)
                elif event.key == pygame.K_LEFT and direction != (Cell_size, 0):
                    direction = (-Cell_size, 0)
                elif event.key == pygame.K_RIGHT and direction != (-Cell_size, 0):
                    direction = (Cell_size, 0)
                elif event.key == pygame.K_p:
                    pause_and_save(level, score)

        new_pos = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        if (new_pos in snake or 
            new_pos[0] < Cell_size or new_pos[0] >= Screen_w - Cell_size or 
            new_pos[1] < Cell_size or new_pos[1] >= Screen_h - Cell_size):
            text = Font.render("GAME OVER", True, Red)
            screen.blit(text, (180, 350))
            pygame.display.update()
            pygame.time.delay(1500)
            pause_and_save(level, score)
            pygame.quit()
            sys.exit()

        snake.insert(0, new_pos)

        if new_pos == food.position:
            score += food.value
            food = Food(snake, speed)
            if score >= level * 10:
                level += 1
                speed += 2
        else:
            snake.pop()

        if food.update_timer():
            food = None
        if food is None:
            food = Food(snake, speed)
        else:
            food.draw()

        for part in snake:
            pygame.draw.rect(screen, Green, (*part, Cell_size, Cell_size))

        score_text = font.render(f"Score: {score}", True, Black)
        level_text = font.render(f"Level: {level}", True, Black)

        screen.blit(score_text, (0, 0))
        screen.blit(level_text, (Screen_w - 120, 0))

        pygame.display.flip()
        Clock.tick(speed)

start_screen()
game()
