import pygame
import sys

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
TOOLBAR_HEIGHT = 60
CANVAS_HEIGHT = WINDOW_HEIGHT - TOOLBAR_HEIGHT

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
PINK = (255, 105, 180)
GRAY = (169, 169, 169)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (200, 200, 200)
TOOLBAR_BG = (40, 40, 40)
TOOLBAR_BORDER = (80, 80, 80)

TOOL_PENCIL = "pencil"
TOOL_RECTANGLE = "rectangle"
TOOL_CIRCLE = "circle"
TOOL_ERASER = "eraser"

class Button:
    """Represents a clickable button in the toolbar."""

    def __init__(self, x, y, width, height, color, label, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.label = label
        self.text_color = text_color
        self.is_active = False
        self.hover = False

    def draw(self, surface, font):
        """Draw the button on the given surface."""
        if self.is_active:
            pygame.draw.rect(surface, WHITE, self.rect.inflate(4, 4), border_radius=6)
        elif self.hover:
            pygame.draw.rect(surface, LIGHT_GRAY, self.rect.inflate(2, 2), border_radius=6)

        pygame.draw.rect(surface, self.color, self.rect, border_radius=5)

        text_surface = font.render(self.label, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def update_hover(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)

class ColorSwatch:
    """Represents a color selection swatch in the toolbar."""

    def __init__(self, x, y, size, color):
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color
        self.is_selected = False

    def draw(self, surface):
        """Draw the color swatch."""

        if self.is_selected:
            pygame.draw.rect(surface, WHITE, self.rect.inflate(6, 6), border_radius=4)

        pygame.draw.rect(surface, self.color, self.rect, border_radius=3)
        pygame.draw.rect(surface, DARK_GRAY, self.rect, 1, border_radius=3)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class PaintApp:
    """Main Paint Application class."""

    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Paint - Pygame")
        self.clock = pygame.time.Clock()

        self.font_small = pygame.font.SysFont("Arial", 13, bold=True)
        self.font_medium = pygame.font.SysFont("Arial", 15, bold=True)

        self.canvas = pygame.Surface((WINDOW_WIDTH, CANVAS_HEIGHT))
        self.canvas.fill(WHITE)

        self.current_tool = TOOL_PENCIL
        self.current_color = BLACK
        self.brush_size = 4
        self.drawing = False
        self.start_pos = None
        self.canvas_backup = None

        self._setup_toolbar()

    def _setup_toolbar(self):
        """Create all toolbar buttons and color swatches."""

        # ----- TOOL BUTTONS -----
        self.tool_buttons = [
            Button(10, 10, 80, 38, (70, 130, 180), "Pencil"),
            Button(100, 10, 90, 38, (60, 179, 113), "Rect"),
            Button(200, 10, 90, 38, (210, 105, 30), "Circle"),
            Button(300, 10, 80, 38, (169, 169, 169), "Eraser", BLACK),
        ]
        self.tool_buttons[0].is_active = True

        self.size_buttons = [
            Button(430, 10, 35, 38, DARK_GRAY, "S"),
            Button(470, 10, 35, 38, DARK_GRAY, "M"),
            Button(510, 10, 35, 38, DARK_GRAY, "L"),
        ]
        self.size_buttons[1].is_active = True

        self.brush_sizes = [2, 5, 10]
        self.brush_size = self.brush_sizes[1]

        # ----- CLEAR BUTTON -----
        self.clear_button = Button(555, 10, 70, 38, (200, 50, 50), "Clear")

        colors = [
            BLACK, WHITE, RED, GREEN, BLUE,
            YELLOW, ORANGE, PURPLE, CYAN, PINK, GRAY
        ]
        self.color_swatches = []
        swatch_x = 635          
        swatch_size = 24        
        gap = 3                 

        for i, color in enumerate(colors):
            col = i % 6
            row = i // 6
            x = swatch_x + col * (swatch_size + gap)
            y = 5 + row * (swatch_size + gap)
            swatch = ColorSwatch(x, y, swatch_size, color)
            if color == BLACK:
                swatch.is_selected = True
            self.color_swatches.append(swatch)

    def _select_tool(self, tool_name):
        self.current_tool = tool_name
        tool_map = {
            TOOL_PENCIL: 0,
            TOOL_RECTANGLE: 1,
            TOOL_CIRCLE: 2,
            TOOL_ERASER: 3
        }
        for i, btn in enumerate(self.tool_buttons):
            btn.is_active = (i == tool_map[tool_name])

    def _select_brush_size(self, index):
        self.brush_size = self.brush_sizes[index]
        for i, btn in enumerate(self.size_buttons):
            btn.is_active = (i == index)

    def _select_color(self, color):
        self.current_color = color
        for swatch in self.color_swatches:
            swatch.is_selected = (swatch.color == color)

    def _handle_events(self):
        mouse_pos = pygame.mouse.get_pos()

        for btn in self.tool_buttons + self.size_buttons:
            btn.update_hover(mouse_pos)
        self.clear_button.update_hover(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_down(mouse_pos, event.button)
            if event.type == pygame.MOUSEBUTTONUP:
                self._handle_mouse_up(mouse_pos, event.button)
            if event.type == pygame.MOUSEMOTION:
                self._handle_mouse_motion(mouse_pos)

    def _handle_keydown(self, key):
        if key == pygame.K_p:
            self._select_tool(TOOL_PENCIL)
        elif key == pygame.K_r:
            self._select_tool(TOOL_RECTANGLE)
        elif key == pygame.K_c:
            self._select_tool(TOOL_CIRCLE)
        elif key == pygame.K_e:
            self._select_tool(TOOL_ERASER)
        elif key == pygame.K_DELETE or key == pygame.K_BACKSPACE:
            self.canvas.fill(WHITE)

    def _handle_mouse_down(self, mouse_pos, button):
        if button != 1:
            return
        if mouse_pos[1] < TOOLBAR_HEIGHT:
            self._check_toolbar_click(mouse_pos)
            return

        canvas_pos = (mouse_pos[0], mouse_pos[1] - TOOLBAR_HEIGHT)
        self.drawing = True
        self.start_pos = canvas_pos

        if self.current_tool in (TOOL_RECTANGLE, TOOL_CIRCLE):
            self.canvas_backup = self.canvas.copy()

    def _handle_mouse_up(self, mouse_pos, button):
        if button != 1:
            return
        if self.drawing and self.start_pos:
            canvas_pos = (mouse_pos[0], mouse_pos[1] - TOOLBAR_HEIGHT)
            if self.current_tool == TOOL_RECTANGLE:
                self._draw_rectangle(self.start_pos, canvas_pos, final=True)
            elif self.current_tool == TOOL_CIRCLE:
                self._draw_circle(self.start_pos, canvas_pos, final=True)

        self.drawing = False
        self.start_pos = None
        self.canvas_backup = None

    def _handle_mouse_motion(self, mouse_pos):
        if not self.drawing:
            return
        if mouse_pos[1] < TOOLBAR_HEIGHT:
            return

        canvas_pos = (mouse_pos[0], mouse_pos[1] - TOOLBAR_HEIGHT)

        if self.current_tool == TOOL_PENCIL:
            if self.start_pos:
                pygame.draw.line(
                    self.canvas, self.current_color,
                    self.start_pos, canvas_pos, self.brush_size
                )
                pygame.draw.circle(
                    self.canvas, self.current_color,
                    canvas_pos, self.brush_size // 2
                )
            self.start_pos = canvas_pos

        elif self.current_tool == TOOL_ERASER:
            pygame.draw.circle(
                self.canvas, WHITE, canvas_pos, self.brush_size * 3
            )
            self.start_pos = canvas_pos

        elif self.current_tool == TOOL_RECTANGLE:
            self._draw_rectangle(self.start_pos, canvas_pos, final=False)

        elif self.current_tool == TOOL_CIRCLE:
            self._draw_circle(self.start_pos, canvas_pos, final=False)

    def _draw_rectangle(self, start, end, final=False):
        if not final and self.canvas_backup:
            self.canvas.blit(self.canvas_backup, (0, 0))

        x = min(start[0], end[0])
        y = min(start[1], end[1])
        width = abs(end[0] - start[0])
        height = abs(end[1] - start[1])

        rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.canvas, self.current_color, rect, self.brush_size)

    def _draw_circle(self, start, end, final=False):
        if not final and self.canvas_backup:
            self.canvas.blit(self.canvas_backup, (0, 0))

        cx, cy = start
        radius = int(((end[0] - cx) ** 2 + (end[1] - cy) ** 2) ** 0.5)

        if radius > 0:
            pygame.draw.circle(
                self.canvas, self.current_color,
                (cx, cy), radius, self.brush_size
            )

    def _check_toolbar_click(self, mouse_pos):
        tools = [TOOL_PENCIL, TOOL_RECTANGLE, TOOL_CIRCLE, TOOL_ERASER]
        for i, btn in enumerate(self.tool_buttons):
            if btn.is_clicked(mouse_pos):
                self._select_tool(tools[i])
                return

        for i, btn in enumerate(self.size_buttons):
            if btn.is_clicked(mouse_pos):
                self._select_brush_size(i)
                return

        if self.clear_button.is_clicked(mouse_pos):
            self.canvas.fill(WHITE)
            return

        for swatch in self.color_swatches:
            if swatch.is_clicked(mouse_pos):
                self._select_color(swatch.color)
                return

    def _draw_toolbar(self):
        """Draw the toolbar background and all UI elements."""
        toolbar_rect = pygame.Rect(0, 0, WINDOW_WIDTH, TOOLBAR_HEIGHT)
        pygame.draw.rect(self.screen, TOOLBAR_BG, toolbar_rect)
        pygame.draw.line(
            self.screen, TOOLBAR_BORDER,
            (0, TOOLBAR_HEIGHT - 1),
            (WINDOW_WIDTH, TOOLBAR_HEIGHT - 1), 2
        )

        # Draw tool buttons
        for btn in self.tool_buttons:
            btn.draw(self.screen, self.font_small)

        size_label = self.font_small.render("Size:", True, LIGHT_GRAY)
        self.screen.blit(size_label, (395, 23))

        # Draw size buttons
        for btn in self.size_buttons:
            btn.draw(self.screen, self.font_small)

        # Draw clear button
        self.clear_button.draw(self.screen, self.font_small)

        # Draw color swatches
        for swatch in self.color_swatches:
            swatch.draw(self.screen)

        # Draw keyboard shortcuts hint
        hint = self.font_small.render(
            "P=Pencil  R=Rect  C=Circle  E=Eraser  DEL=Clear",
            True, (120, 120, 120)
        )
        self.screen.blit(hint, (5, TOOLBAR_HEIGHT + 3))

    def run(self):
        """Main application loop."""
        while True:
            self._handle_events()

            self.screen.blit(self.canvas, (0, TOOLBAR_HEIGHT))
            self._draw_toolbar()

            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[1] > TOOLBAR_HEIGHT + 15:
                canvas_pos = (mouse_pos[0], mouse_pos[1])
                if self.current_tool == TOOL_ERASER:
                    pygame.draw.circle(
                        self.screen, GRAY, canvas_pos,
                        self.brush_size * 3, 1
                    )
                else:
                    pygame.draw.circle(
                        self.screen, self.current_color,
                        canvas_pos, max(2, self.brush_size // 2)
                    )

            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    app = PaintApp()
    app.run()