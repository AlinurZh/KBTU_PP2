import pygame


def main():
    pygame.init()
    screen = pygame.display.set_mode((700, 500))
    clock = pygame.time.Clock()

    radius = 15
    mode = 'draw'
    points = []
    start_pos = None
    drawings = []

    current_color = (0, 0, 255)
    colors = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 255, 0),
        (0, 255, 255),
        (255, 165, 0)
    ]

    WHITE = (255, 255, 255)

    buttons = [
        ("Draw", 'draw', 10),
        ("Rect", 'rect', 100),
        ("Circle", 'circle', 190),
        ("Eraser", 'eraser', 280),
        ("Square", 'square', 370),
        ("rTriangle", 'rtriangle', 460),
        ("eTriangle", 'etriangle', 550),
        ("Rhombus", 'rhombus', 640)
    ]

    while True:
        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_held:
                    return
                if event.key == pygame.K_F4 and alt_held:
                    return
                if event.key == pygame.K_ESCAPE:
                    return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Проверяем, нажал ли пользователь на кнопку инструмента
                    for (label, btn_mode, bx) in buttons:
                        btn_rect = pygame.Rect(bx, 445, 80, 30)
                        if btn_rect.collidepoint(event.pos):
                            mode = btn_mode
                            break

                    # Проверяем, выбрал ли пользователь новый цвет
                    for i, color in enumerate(colors):
                        color_rect = pygame.Rect(490 + i * 35, 0, 30, 30)
                        if color_rect.collidepoint(event.pos):
                            current_color = color
                            break

                    start_pos = event.pos
                    points = []

                elif event.button == 3:
                    radius = max(1, radius - 1)

            if event.type == pygame.MOUSEMOTION:
                if event.buttons[0]:
                    if mode == 'draw':
                        points.append(event.pos)

                        if len(points) >= 2:
                            drawings.append(('line', current_color, points[-2], points[-1], radius))

                    elif mode == 'eraser':
                        drawings.append(('eraser', WHITE, event.pos, radius * 2))

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and start_pos:
                    if mode == 'rect':
                        x = min(start_pos[0], event.pos[0])
                        y = min(start_pos[1], event.pos[1])
                        w = abs(event.pos[0] - start_pos[0])
                        h = abs(event.pos[1] - start_pos[1])

                        drawings.append(('rect', current_color, (x, y, w, h)))

                    elif mode == 'circle':
                        dx = event.pos[0] - start_pos[0]
                        dy = event.pos[1] - start_pos[1]
                        r = int((dx ** 2 + dy ** 2) ** 0.5)

                        drawings.append(('circle', current_color, start_pos, r))

                    elif mode == 'square':
                        x = min(start_pos[0], event.pos[0])
                        y = min(start_pos[1], event.pos[1])
                        w = h = min(
                            abs(event.pos[0] - start_pos[0]),
                            abs(event.pos[1] - start_pos[1])
                        )

                        drawings.append(('square', current_color, (x, y, w, h)))

                    elif mode == 'etriangle':
                        drawings.append(('etriangle', current_color, [
                            start_pos,
                            event.pos,
                            (
                                (start_pos[0] + event.pos[0]) // 2,
                                start_pos[1] + int(abs(event.pos[0] - start_pos[0]) * 0.866)
                            )
                        ]))

                    elif mode == 'rhombus':
                        x = (start_pos[0] + event.pos[0]) // 2
                        y = (start_pos[1] + event.pos[1]) // 2

                        top = (x, start_pos[1])
                        right = (event.pos[0], y)
                        bottom = (x, event.pos[1])
                        left = (start_pos[0], y)

                        drawings.append(('rhombus', current_color, [top, right, bottom, left]))

                    elif mode == 'rtriangle':
                        drawings.append(('rtriangle', current_color, [
                            start_pos,
                            (start_pos[0], event.pos[1]),
                            event.pos
                        ]))

                    start_pos = None
                    points = []

        screen.fill(WHITE)

        # Каждый кадр заново рисуем все фигуры, которые были сохранены раньше
        for drawing in drawings:
            if drawing[0] == 'line':
                drawLineBetween(screen, 0, drawing[2], drawing[3], drawing[4], drawing[1])

            elif drawing[0] == 'rect':
                pygame.draw.rect(screen, drawing[1], drawing[2], 2)

            elif drawing[0] == 'square':
                pygame.draw.rect(screen, drawing[1], drawing[2], 2)

            elif drawing[0] == 'etriangle':
                pygame.draw.polygon(screen, drawing[1], drawing[2], 2)

            elif drawing[0] == 'circle':
                pygame.draw.circle(screen, drawing[1], drawing[2], drawing[3], 2)

            elif drawing[0] == 'eraser':
                pygame.draw.circle(screen, drawing[1], drawing[2], drawing[3])

            elif drawing[0] == 'rhombus':
                pygame.draw.polygon(screen, drawing[1], drawing[2], 2)

            elif drawing[0] == 'rtriangle':
                pygame.draw.polygon(screen, drawing[1], drawing[2], 2)

        # Предпросмотр фигуры, пока мышка еще не отпущена
        if start_pos and mode == 'rect':
            x = min(start_pos[0], mouse_pos[0])
            y = min(start_pos[1], mouse_pos[1])
            w = abs(mouse_pos[0] - start_pos[0])
            h = abs(mouse_pos[1] - start_pos[1])

            pygame.draw.rect(screen, current_color, (x, y, w, h), 2)

        elif start_pos and mode == 'circle':
            dx = mouse_pos[0] - start_pos[0]
            dy = mouse_pos[1] - start_pos[1]
            r = int((dx ** 2 + dy ** 2) ** 0.5)

            pygame.draw.circle(screen, current_color, start_pos, r, 2)

        elif start_pos and mode == 'square':
            x = min(start_pos[0], mouse_pos[0])
            y = min(start_pos[1], mouse_pos[1])
            w = h = min(
                abs(mouse_pos[0] - start_pos[0]),
                abs(mouse_pos[1] - start_pos[1])
            )

            pygame.draw.rect(screen, current_color, (x, y, w, h), 2)

        elif start_pos and mode == 'etriangle':
            pygame.draw.polygon(screen, current_color, [
                start_pos,
                mouse_pos,
                (
                    (start_pos[0] + mouse_pos[0]) // 2,
                    start_pos[1] + int(abs(mouse_pos[0] - start_pos[0]) * 0.866)
                )
            ], 2)

        elif start_pos and mode == 'rhombus':
            x = (start_pos[0] + mouse_pos[0]) // 2
            y = (start_pos[1] + mouse_pos[1]) // 2

            top = (x, start_pos[1])
            right = (mouse_pos[0], y)
            bottom = (x, mouse_pos[1])
            left = (start_pos[0], y)

            pygame.draw.polygon(screen, current_color, [top, right, bottom, left], 2)

        elif start_pos and mode == 'rtriangle':
            pygame.draw.polygon(screen, current_color, [
                start_pos,
                (start_pos[0], mouse_pos[1]),
                mouse_pos
            ], 2)

        pygame.draw.rect(screen, (50, 50, 50), (0, 440, 700, 60))
        pygame.draw.rect(screen, (50, 50, 50), (480, 0, 225, 50))

        for (label, btn_mode, bx) in buttons:
            if mode == btn_mode:
                color = (150, 150, 150)
            else:
                color = (100, 100, 100)

            pygame.draw.rect(screen, color, (bx, 445, 80, 30))

            txt = pygame.font.SysFont("Verdana", 12).render(label, True, (0, 0, 0))
            screen.blit(txt, (bx + 5, 452))

        for i, color in enumerate(colors):
            pygame.draw.rect(screen, color, (490 + i * 35, 0, 30, 30))

            if color == current_color:
                pygame.draw.rect(screen, (0, 0, 0), (490 + i * 35, 0, 30, 30), 2)

        pygame.display.flip()
        clock.tick(60)


def drawLineBetween(screen, index, start, end, width, current_color):
    # Так линия получается плавнее, потому что между двумя точками рисуются маленькие круги
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    iterations = max(abs(dx), abs(dy))

    if iterations == 0:
        return

    for i in range(iterations):
        progress = 1.0 * i / iterations
        aprogress = 1 - progress

        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])

        pygame.draw.circle(screen, current_color, (x, y), width)


main()