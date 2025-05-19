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
        ("Which of this is not a component of Geospatial science?", ["GIS", "Remote sensing", "Pancreas", "GPS"], 2),
        ("Which actictivity is part of GIS?", ["Running", "Dancing", "Throwing", "Data Collection"], 3),
        ("Which is not a presentation of vector data?", ["Point", "Image", "Line", "Polygon"], 1),
        ("What does GIS stand for?", ["Geospatial Imaging System", "Geographic Information System", "Geology Index Survey", "Global Infrastructure Setup"], 1),
        ("Select the application of GIS?", ["Agriculture", "Sweaping", "cattle herding", "balancing the equation"], 0),
        ("Raster Data is presented by?", ["Rows amd columns", "Polygons", "lines", "Parallel lines"], 0),
        ("Which of these is NOT a common GIS software?", ["ArcGIS", "QGIS", "AutoCAD", "ArcMap"], 2),
        ("How many types of maps do we have?", ["1", "5", "3", "2"], 2),
        ("What is not an element of map?", ["North arrow", "QuickBird", "Map scale", "legend"], 1),
        ("under what does a map fall in Geospatial science?", ["Data collection", "Data analysis", "Data presentation", "Data interpretation"], 2)
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


