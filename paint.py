import pygame
import sys

pygame.init()

Screen_w, Screen_h = 800, 600
screen = pygame.display.set_mode((Screen_w, Screen_h))
pygame.display.set_caption("Paint")

canvas = pygame.Surface(screen.get_size())


clock = pygame.time.Clock()

black = (0, 0, 0)
white = (255, 255, 255)
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), black]
current_color = black
tool = "brush"
radius = 5

canvas.fill(white)

font = pygame.font.SysFont(None, 24)
buttons = {
    "Brush": pygame.Rect(10, 10, 80, 30),
    "Eraser": pygame.Rect(100, 10, 80, 30),
    "Rect": pygame.Rect(190, 10, 80, 30),
    "Circle": pygame.Rect(280, 10, 80, 30)
}

color_buttons = [
    pygame.Rect(400 + i*40, 10, 30, 30) for i in range(len(colors))
]

drawing = False
start_pos = None

def draw_buttons():
    for name, rect in buttons.items():
        pygame.draw.rect(screen, (200, 200, 200), rect)
        text = font.render(name, True, black)
        screen.blit(text, (rect.x + 5, rect.y + 5))

    for i, rect in enumerate(color_buttons):
        pygame.draw.rect(screen, colors[i], rect)

def handle_tool_buttons(pos):
    global tool
    for name, rect in buttons.items():
        if rect.collidepoint(pos):
            tool = name.lower()

def handle_color_buttons(pos):
    global current_color
    for i, rect in enumerate(color_buttons):
        if rect.collidepoint(pos):
            current_color = colors[i]

running = True
while running:
    screen.fill((220, 220, 220))
    screen.blit(canvas, (0, 0))

    draw_buttons()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                handle_tool_buttons(event.pos)
                handle_color_buttons(event.pos)
                if event.pos[1] > 50:
                    drawing = True
                    start_pos = event.pos
                    if tool == "brush":
                        pygame.draw.circle(canvas, current_color, event.pos, radius)
                    elif tool == "eraser":
                        pygame.draw.circle(canvas, white, event.pos, radius)
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                end_pos = event.pos
                if tool == "rect":
                    rect = pygame.Rect(start_pos, (end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]))
                    pygame.draw.rect(canvas, current_color, rect, 2)
                elif tool == "circle":
                    center = start_pos
                    radius_circle = int(((end_pos[0] - center[0]) ** 2 + (end_pos[1] - center[1]) ** 2) ** 0.5)
                    pygame.draw.circle(canvas, current_color, center, radius_circle, 2)
                drawing = False
                start_pos = None

        elif event.type == pygame.MOUSEMOTION and drawing:
            if tool == "brush":
                pygame.draw.circle(canvas, current_color, event.pos, radius)
            elif tool == "eraser":
                pygame.draw.circle(canvas, white, event.pos, radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
