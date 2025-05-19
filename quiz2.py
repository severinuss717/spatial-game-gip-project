import os
import time
import pygame as pg
import sys

# Initialize pygame
pg.init()

# Create the screen
screen = pg.display.set_mode((1000, 800))
pg.display.set_caption("Geospatial Quiz")
icon = pg.image.load('joystick.png')
pg.display.set_icon(icon)

font = pg.font.SysFont(None, 36)
button_font = pg.font.SysFont(None, 40)

def draw_button(text, x, y, w, h, color, hover_color):
    mouse = pg.mouse.get_pos()
    click = pg.mouse.get_pressed()
    rect = pg.Rect(x, y, w, h)
    hovered = rect.collidepoint(mouse)
    pg.draw.rect(screen, hover_color if hovered else color, rect)
    text_surface = button_font.render(text, True, (255, 255, 255))
    screen.blit(text_surface, (x + 20, y + 10))
    return hovered and click[0]

def run_quiz():
    questions = [
        ("What best describes levelling?", ["determining two points.", "determining height differences between two points on the earth", "Calculating Height ", "Flight Heihg and photo scale"], 1),
        ("What is not required to calclate photo scale", ["Level", "Flying height", "Height above sea level", "Focal length"], 0),
        ("Which coordinate system is most common in GIS?", ["Polar", "Cartesian", "Geographic", "Temporal"], 2),
        ("What is remote sensing?", ["acquiring data from a distance", "acquiring data on a distance", "calculating data", "Creating distance data"], 0),
        ("Which of these is not an instrument used in levelling?", ["level", "Staff", "Tripod", "Camera"], 3),
        ("for levelling calculations one should have?", ["Intermediate sight", "Fore sight", "Back sight", "All of the above"], 3),
        ("When levelling always start with?", ["Fore sight", "Intermediate sight", "Back sight", "Turning point"], 2),
        ("Which is not part of flight planning?", ["Determining flight area", "Determining flight height", "Determining the number of photographs required", "None of the above"], 3),
        ("Which is not required for fligh height calculation ?", ["Height above sea level", "Photos scale", "Bar scale", "For length"], 2),
        ("You have a photoscale of 1:1000 and focal length of 0.35m and height above sea level of 400m determine the flight height H?", ["750m", "1.75m", "7500m", "200m"], 1)
    ]

    current_q = 0
    score = 0

    def draw_question(q_index):
        screen.fill((30, 30, 60))
        question, options, _ = questions[q_index]
        question_surface = font.render(f"Q{q_index + 1}: {question}", True, (255, 255, 255))
        screen.blit(question_surface, (50, 50))
        for i, opt in enumerate(options):
            opt_surface = font.render(f"{i + 1}. {opt}", True, (200, 200, 0))
            screen.blit(opt_surface, (70, 120 + i * 50))
        instruction = font.render("Press 1, 2, 3 or 4 to answer.", True, (180, 180, 180))
        screen.blit(instruction, (50, 350))
        pg.display.update()

    answering = True
    while answering:
        draw_question(current_q)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key in [pg.K_1, pg.K_KP1]:
                    selected = 0
                elif event.key in [pg.K_2, pg.K_KP2]:
                    selected = 1
                elif event.key in [pg.K_3, pg.K_KP3]:
                    selected = 2
                elif event.key in [pg.K_4, pg.K_KP4]:
                    selected = 3
                else:
                    continue

                _, _, correct_index = questions[current_q]
                if selected == correct_index:
                    score += 1
                current_q += 1
                if current_q >= len(questions):
                    answering = False
                time.sleep(0.3)

    show_result(score)

def show_result(score):
    showing_result = True
    while showing_result:
        screen.fill((0, 0, 0))
        result_text = f"You scored {score}/10!"
        screen.blit(font.render(result_text, True, (255, 255, 255)), (400, 250))

        if score >= 5:
            screen.blit(font.render("Great job! Click below to continue to next level.", True, (0, 255, 0)), (200, 300))
            if draw_button("Next Level", 400, 400, 200, 60, (0, 128, 0), (0, 200, 0)):
                pg.quit()
                os.system("python level_2.py")  # Replace with actual file
        else:
            screen.blit(font.render("You failed. Click to retry the quiz.", True, (255, 0, 0)), (280, 300))
            if draw_button("Retry", 400, 400, 200, 60, (128, 0, 0), (200, 0, 0)):
                pg.quit()
                restart_game()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        pg.display.update()

def restart_game():
    os.execl(sys.executable, sys.executable, *sys.argv)

# Run the quiz immediately when this script is run
run_quiz()


