from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import cos, sin


# Medidas da peca da imagem, usando o ponto vermelho como origem (0, 0).
SCALE = 6
OFFSET_X = 230
OFFSET_Y = 130


PIECE_POINTS = [
    (0, 0),
    (25, 0),
    (25, 15),
    (50, 0),
    (65, 0),
    (65, 30),
    (55, 30),
    (55, 45),
    (40, 45),
    (40, 60),
    (30, 60),
    (30, 45),
    (15, 60),
    (0, 60),
    (0, 40),
    (10, 40),
    (10, 25),
    (0, 25),
]


def to_screen(x, y):
    return int(OFFSET_X + x * SCALE), int(OFFSET_Y + y * SCALE)


def bresenham(x1, y1, x2, y2):
    x1, y1 = int(x1), int(y1)
    x2, y2 = int(x2), int(y2)
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    glBegin(GL_POINTS)
    while True:
        glVertex2i(x1, y1)
        if x1 == x2 and y1 == y2:
            break

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy
    glEnd()


def draw_line(x1, y1, x2, y2):
    sx1, sy1 = to_screen(x1, y1)
    sx2, sy2 = to_screen(x2, y2)
    bresenham(sx1, sy1, sx2, sy2)


def draw_circle(x, y, radius, fill=True):
    cx, cy = to_screen(x, y)
    r = int(radius * SCALE)

    if fill:
        glBegin(GL_TRIANGLE_FAN)
        glVertex2i(cx, cy)
        for i in range(41):
            angle = 2.0 * 3.14159265 * i / 40
            glVertex2f(cx + r * cos(angle), cy + r * sin(angle))
        glEnd()
        return

    glBegin(GL_LINE_LOOP)
    for i in range(40):
        angle = 2.0 * 3.14159265 * i / 40
        glVertex2f(cx + r * cos(angle), cy + r * sin(angle))
    glEnd()


def draw_text(text, x, y, scale=0.13, rotation=0):
    glPushMatrix()
    sx, sy = to_screen(x, y)
    glTranslatef(sx, sy, 0)
    glRotatef(rotation, 0, 0, 1)
    glScalef(scale, scale, scale)
    for char in text:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(char))
    glPopMatrix()


def draw_dimension_text(text, x, y, vertical=False):
    draw_text(text, x, y, scale=0.12, rotation=90 if vertical else 0)


def draw_arrow(x, y, direction):
    size = 1.8
    if direction == "left":
        draw_line(x, y, x + size, y + size * 0.65)
        draw_line(x, y, x + size, y - size * 0.65)
    elif direction == "right":
        draw_line(x, y, x - size, y + size * 0.65)
        draw_line(x, y, x - size, y - size * 0.65)
    elif direction == "up":
        draw_line(x, y, x - size * 0.65, y - size)
        draw_line(x, y, x + size * 0.65, y - size)
    elif direction == "down":
        draw_line(x, y, x - size * 0.65, y + size)
        draw_line(x, y, x + size * 0.65, y + size)


def horizontal_dimension(x1, x2, y, text, text_y_offset=1.5):
    draw_line(x1, y, x2, y)
    draw_arrow(x1, y, "right")
    draw_arrow(x2, y, "left")
    draw_dimension_text(text, (x1 + x2) / 2 - 2.6, y + text_y_offset)


def vertical_dimension(x, y1, y2, text, text_x_offset=-4.5):
    draw_line(x, y1, x, y2)
    draw_arrow(x, y1, "up")
    draw_arrow(x, y2, "down")
    draw_dimension_text(text, x + text_x_offset, (y1 + y2) / 2 - 2.2, vertical=True)


def draw_extension_lines():
    glColor3f(0.45, 0.45, 0.45)

    for x in (0, 15, 30, 40, 55, 65):
        draw_line(x, 60, x, 73)

    for x in (0, 25, 50, 65):
        draw_line(x, -6, x, 0)

    for y in (0, 25, 40, 60):
        draw_line(-10, y, 0, y)

    for y in (0, 30, 45, 60):
        draw_line(65, y, 78, y)

    draw_line(25, 0, 25, 18)
    draw_line(10, 25, 10, 34)
    draw_line(30, 45, 30, 62)
    draw_line(40, 45, 40, 62)


def draw_dimensions():
    glColor3f(0.0, 0.0, 0.0)

    horizontal_dimension(0, 15, 70, "15")
    horizontal_dimension(15, 30, 70, "15")
    horizontal_dimension(30, 40, 70, "10")
    horizontal_dimension(40, 55, 70, "15")
    horizontal_dimension(55, 65, 70, "10")

    horizontal_dimension(0, 25, -8, "25", text_y_offset=-5)
    horizontal_dimension(25, 50, -8, "25", text_y_offset=-5)
    horizontal_dimension(50, 65, -8, "15", text_y_offset=-5)

    horizontal_dimension(0, 10, 30, "10", text_y_offset=1.2)

    vertical_dimension(-9, 45, 60, "15")
    vertical_dimension(-9, 25, 45, "20")
    vertical_dimension(-9, 0, 25, "25")

    vertical_dimension(75, 45, 60, "15", text_x_offset=3)
    vertical_dimension(75, 30, 45, "15", text_x_offset=3)
    vertical_dimension(75, 0, 30, "30", text_x_offset=3)

    vertical_dimension(36, 45, 60, "15", text_x_offset=-2)
    vertical_dimension(20, 0, 15, "15", text_x_offset=-4)


def draw_piece_fill():
    glColor3f(0.98, 0.88, 0.68)

    screen_points = [to_screen(x, y) for x, y in PIECE_POINTS]
    min_y = min(y for _, y in screen_points)
    max_y = max(y for _, y in screen_points)

    glBegin(GL_LINES)
    for y in range(min_y, max_y + 1):
        intersections = []

        for index in range(len(screen_points)):
            x1, y1 = screen_points[index]
            x2, y2 = screen_points[(index + 1) % len(screen_points)]

            if y1 == y2:
                continue

            if min(y1, y2) <= y < max(y1, y2):
                x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                intersections.append(x)

        intersections.sort()
        for index in range(0, len(intersections), 2):
            if index + 1 < len(intersections):
                glVertex2i(round(intersections[index]), y)
                glVertex2i(round(intersections[index + 1]), y)
    glEnd()


def draw_piece_outline():
    glColor3f(0.0, 0.0, 0.0)
    for index in range(len(PIECE_POINTS)):
        x1, y1 = PIECE_POINTS[index]
        x2, y2 = PIECE_POINTS[(index + 1) % len(PIECE_POINTS)]
        draw_line(x1, y1, x2, y2)


def draw_origin_point():
    glColor3f(1.0, 0.0, 0.0)
    draw_circle(0, 0, 1.4)


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_piece_fill()
    draw_extension_lines()
    draw_dimensions()
    draw_piece_outline()
    draw_origin_point()
    glFlush()


def init():
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 600)
    glPointSize(2.0)


def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Peca cotada com Bresenham")
    init()
    glutDisplayFunc(display)
    glutMainLoop()


if __name__ == "__main__":
    main()
