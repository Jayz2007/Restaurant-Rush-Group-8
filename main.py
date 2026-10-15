"""
RESTAURANT RUSH — GROUP 8
Polished, asset-free Pygame restaurant management game.
Python 3.10+ | pygame 2.5+
"""
import random
import sys
import pygame

pygame.init()
pygame.display.set_caption("Restaurant Rush | Group 8")

WIDTH, HEIGHT = 1100, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
FPS = 60

                                     
BG = (19, 25, 39)
PANEL = (30, 39, 58)
PANEL_LIGHT = (41, 53, 76)
CREAM = (250, 244, 230)
MUTED = (166, 180, 199)
ORANGE = (255, 166, 77)
GREEN = (83, 204, 143)
RED = (244, 100, 107)
BLUE = (103, 172, 255)
YELLOW = (255, 214, 102)
DARK = (15, 20, 31)
WHITE = (255, 255, 255)

FONT = pygame.font.SysFont("arial", 20)
SMALL = pygame.font.SysFont("arial", 15)
MEDIUM = pygame.font.SysFont("arial", 25, bold=True)
BIG = pygame.font.SysFont("arial", 48, bold=True)
TITLE = pygame.font.SysFont("arial", 58, bold=True)

                                                
TABLE_POSITIONS = [(78, 200), (78, 292), (78, 384), (78, 476)]

                                                                  
AVAILABLE_INGREDIENTS = {
    "bun", "patty", "cheese", "lettuce", "potato", "soda", "ice"
}

                                                               
RECIPES = {
    "Burger": {"bun": 1, "patty": 1, "cheese": 1, "lettuce": 1},
    "Fries": {"potato": 2},
    "Soda": {"soda": 1, "ice": 1},
    "Combo Meal": {"Burger": 1, "Fries": 1, "Soda": 1},
}
INGREDIENT_STOCK = {
    "bun": 10, "patty": 10, "cheese": 10, "lettuce": 10,
    "potato": 14, "soda": 12, "ice": 12
}
MENU = {
    "Burger": {"price": 30, "prep": 8, "emoji": "BURGER"},
    "Fries": {"price": 18, "prep": 5, "emoji": "FRIES"},
    "Soda": {"price": 12, "prep": 3, "emoji": "SODA"},
    "Combo Meal": {"price": 50, "prep": 12, "emoji": "COMBO"},
}

def bubble_sort_by_wait(items):
    """Bubble Sort: rank orders by longest waiting time first."""
    result = items[:]
    n = len(result)
    for end in range(n - 1, 0, -1):
        swapped = False
        for i in range(end):
            if result[i]["wait"] < result[i + 1]["wait"]:
                result[i], result[i + 1] = result[i + 1], result[i]
                swapped = True
        if not swapped:
            break
    return result


def insertion_sort_by_wait(items, new_item):
    """Insertion Sort: insert a new order into a list ranked by waiting time."""
    result = items[:]
    index = 0
    while index < len(result) and result[index]["wait"] >= new_item["wait"]:
        index += 1
    result.insert(index, new_item)
    return result


def selection_sort_by_prep(items):
    """Selection Sort: put the shortest-preparation order first."""
    result = items[:]
    for start in range(len(result)):
        best = start
        for i in range(start + 1, len(result)):
            if result[i]["prep"] < result[best]["prep"]:
                best = i
        result[start], result[best] = result[best], result[start]
    return result


def expand_recipe(recipe_name, multiplier=1):
    """
    Recursively expand nested recipes into base ingredients.
    Base case: a component is not a recipe name, so count the ingredient.
    """
    totals = {}
    recipe = RECIPES.get(recipe_name, {})
    for component, quantity in recipe.items():
        amount = quantity * multiplier
        if component in RECIPES:
            nested = expand_recipe(component, amount)
            for ingredient, count in nested.items():
                totals[ingredient] = totals.get(ingredient, 0) + count
        else:
            totals[component] = totals.get(component, 0) + amount
    return totals


def draw_text(surface, value, x, y, font=FONT, color=CREAM):
    surface.blit(font.render(str(value), True, color), (x, y))


def draw_center(surface, value, center, font=FONT, color=CREAM):
    surface.blit(font.render(str(value), True, color),
                 font.render(str(value), True, color).get_rect(center=center))


def rounded(surface, rect, color, radius=14, border=None, border_width=1):
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    if border:
        pygame.draw.rect(surface, border, rect, border_width, border_radius=radius)


def draw_button(surface, rect, label, color, enabled=True, small=False):
    rect = pygame.Rect(rect)
    fill = color if enabled else (65, 72, 86)
    rounded(surface, rect, fill, 10)
    font = SMALL if small else FONT
    rendered = font.render(label, True, WHITE if enabled else (150, 155, 165))
    surface.blit(rendered, rendered.get_rect(center=rect.center))


class RestaurantRush:
    def __init__(self):
        self.state = "menu"
        self.reset_game()
        self.state = "menu"

    def reset_game(self):
        self.orders = []
        self.selected_id = None
        self.next_id = 1
        self.remaining = 90.0
        self.spawn_elapsed = 0.0
        self.score = 0
        self.served = 0
        self.missed = 0
        self.satisfaction = 100
        self.stock = INGREDIENT_STOCK.copy()
        self.notice = "Select an order, prepare it, then serve it."
        self.notice_color = BLUE
        self.notice_time = 5.0
        self.sort_note = "Insertion Sort adds each new order by waiting time."
        self.state = "playing"
        self.spawn_order()

    def set_notice(self, message, color=BLUE):
        self.notice = message
        self.notice_color = color
        self.notice_time = 3.2

    def spawn_order(self):
        dish = random.choice(list(MENU.keys()))
        order = {
            "id": self.next_id,
            "dish": dish,
            "wait": 0.0,
            "prep": MENU[dish]["prep"],
            "prepared": False,
            "table": (self.next_id - 1) % len(TABLE_POSITIONS),
            "customer": random.choice(["Alex", "Sam", "Jamie", "Taylor", "Riley"]),
        }
        self.next_id += 1
        self.orders = insertion_sort_by_wait(self.orders, order)
        self.set_notice(f"New order #{order['id']}: {dish}!", GREEN)
        self.sort_note = "Insertion Sort inserted the new order into the wait-time list."

    def selected_order(self):
        for order in self.orders:
            if order["id"] == self.selected_id:
                return order
        return None

    def prepare_selected(self):
        order = self.selected_order()
        if not order:
            self.set_notice("Select an order card first.", YELLOW)
            return
        if order["prepared"]:
            self.set_notice("Already prepared! Serve the meal.", YELLOW)
            return
        if order["dish"] not in MENU:
            self.set_notice("That dish is not on the menu.", RED)
            return

        required = expand_recipe(order["dish"])
                                                                          
        missing = [ingredient for ingredient, amount in required.items()
                   if ingredient not in AVAILABLE_INGREDIENTS
                   or self.stock.get(ingredient, 0) < amount]
        if missing:
            self.set_notice("Not enough ingredients: " + ", ".join(missing), RED)
            return

        for ingredient, amount in required.items():
            self.stock[ingredient] -= amount
        order["prepared"] = True
        self.set_notice(f"{order['dish']} prepared for order #{order['id']}!", GREEN)

    def serve_selected(self):
        order = self.selected_order()
        if not order:
            self.set_notice("Select an order card first.", YELLOW)
            return
        if not order["prepared"]:
            self.set_notice("Prepare the meal before serving it.", YELLOW)
            return
                                              
        tip = max(0, int(12 - order["wait"] // 4))
        earned = MENU[order["dish"]]["price"] + tip
        self.score += earned
        self.served += 1
        self.satisfaction = min(100, self.satisfaction + 3)
        self.orders = [item for item in self.orders if item["id"] != order["id"]]
        self.selected_id = None
        self.set_notice(f"Served {order['dish']}! +{earned} points (includes tip).", GREEN)

    def sort_by_wait(self):
        self.orders = bubble_sort_by_wait(self.orders)
        self.set_notice("Bubble Sort ranked orders by longest waiting time.", BLUE)
        self.sort_note = "Bubble Sort compares adjacent orders and moves longest waits first."

    def choose_shortest_prep(self):
        if not self.orders:
            self.set_notice("There are no active orders.", YELLOW)
            return
        ranked = selection_sort_by_prep(self.orders)
        self.selected_id = ranked[0]["id"]
        self.set_notice(
            f"Selection Sort picked #{ranked[0]['id']} ({ranked[0]['dish']}), "
            f"shortest prep: {ranked[0]['prep']}s.", BLUE
        )
        self.sort_note = "Selection Sort selected the active order with the shortest prep time."

    def update(self, dt):
        if self.state != "playing":
            return
        self.remaining -= dt
        self.spawn_elapsed += dt
        if self.notice_time > 0:
            self.notice_time -= dt

                                                                                          
        for order in self.orders:
            order["wait"] += dt
        if self.spawn_elapsed >= 8.0:
            self.spawn_elapsed = 0.0
            if len(self.orders) < 6:
                self.spawn_order()
                                                 
        impatient = [o for o in self.orders if o["wait"] >= 28]
        for order in impatient:
            self.orders.remove(order)
            self.missed += 1
            self.satisfaction = max(0, self.satisfaction - 18)
            self.set_notice(f"Order #{order['id']} left unhappy!", RED)
            if self.selected_id == order["id"]:
                self.selected_id = None

        if self.remaining <= 0 or self.satisfaction <= 0:
            self.remaining = max(0, self.remaining)
            self.state = "over"

    def draw_header(self):
        rounded(SCREEN, (24, 18, WIDTH - 48, 94), PANEL, 20)
        draw_text(SCREEN, "RESTAURANT", 48, 31, SMALL, MUTED)
        draw_text(SCREEN, "RUSH", 48, 47, BIG, ORANGE)
        draw_text(SCREEN, "GROUP 8  •  SERVICE SHIFT", 230, 42, SMALL, MUTED)
                                              
        for rect, label, value, color in [
            ((560, 34, 145, 58), "SCORE", self.score, YELLOW),
            ((718, 34, 145, 58), "TIME LEFT", f"{int(self.remaining)}s", ORANGE),
            ((876, 34, 175, 58), "SATISFACTION", f"{self.satisfaction}%", GREEN if self.satisfaction > 35 else RED),
        ]:
            rounded(SCREEN, rect, PANEL_LIGHT, 12)
            draw_text(SCREEN, label, rect[0] + 12, rect[1] + 7, SMALL, MUTED)
            draw_text(SCREEN, value, rect[0] + 12, rect[1] + 27, MEDIUM, color)

    def draw_restaurant(self):
                            
        rounded(SCREEN, (24, 128, 282, 430), PANEL, 18)
        draw_text(SCREEN, "DINING ROOM", 44, 146, MEDIUM)
        draw_text(SCREEN, "Tables", 44, 178, SMALL, MUTED)
        for i, (x, y) in enumerate(TABLE_POSITIONS):
            occupied = any(o["table"] == i for o in self.orders)
            color = ORANGE if occupied else PANEL_LIGHT
            rounded(SCREEN, (x, y, 180, 58), color, 13)
            pygame.draw.circle(SCREEN, CREAM if occupied else MUTED, (x + 25, y + 29), 12)
            draw_text(SCREEN, f"TABLE {i + 1}", x + 47, y + 10, SMALL,
                      DARK if occupied else CREAM)
            draw_text(SCREEN, "WAITING" if occupied else "AVAILABLE",
                      x + 47, y + 29, SMALL, DARK if occupied else MUTED)

                      
        rounded(SCREEN, (326, 128, 420, 430), PANEL, 18)
        draw_text(SCREEN, "ACTIVE ORDERS", 346, 146, MEDIUM)
        draw_text(SCREEN, "Click a card to select it", 346, 178, SMALL, MUTED)
        if not self.orders:
            draw_text(SCREEN, "No orders right now.", 350, 235, FONT, MUTED)
        for index, order in enumerate(self.orders[:6]):
            y = 207 + index * 54
            selected = order["id"] == self.selected_id
            card_color = (66, 83, 111) if selected else PANEL_LIGHT
            rounded(SCREEN, (342, y, 388, 46), card_color, 10,
                    ORANGE if selected else None, 2 if selected else 1)
            status = "READY" if order["prepared"] else f"{order['prep']}s prep"
            draw_text(SCREEN, f"#{order['id']}  {order['dish']}", 354, y + 5, FONT)
            draw_text(SCREEN, f"{int(order['wait'])}s waiting  •  {status}",
                      354, y + 27, SMALL, GREEN if order["prepared"] else MUTED)
            if order["wait"] >= 18:
                pygame.draw.circle(SCREEN, RED, (710, y + 23), 5)

                       
        rounded(SCREEN, (766, 128, 310, 430), PANEL, 18)
        draw_text(SCREEN, "KITCHEN", 786, 146, MEDIUM)
        draw_text(SCREEN, "PREPARE SELECTED", 786, 186, SMALL, MUTED)
        order = self.selected_order()
        if order:
            rounded(SCREEN, (786, 210, 270, 84), PANEL_LIGHT, 12)
            draw_text(SCREEN, f"Order #{order['id']}", 802, 221, SMALL, MUTED)
            draw_text(SCREEN, order["dish"], 802, 243, MEDIUM, ORANGE)
            draw_text(SCREEN, f"Prep: {order['prep']} seconds", 802, 271, SMALL)
            draw_button(SCREEN, (786, 310, 270, 45), "PREPARE MEAL", GREEN,
                        enabled=not order["prepared"])
            draw_button(SCREEN, (786, 365, 270, 45), "SERVE CUSTOMER", BLUE,
                        enabled=order["prepared"])
            draw_text(SCREEN, "Recipe ingredients:", 786, 423, SMALL, MUTED)
            required = expand_recipe(order["dish"])
            ingredient_line = ", ".join(f"{k} x{v}" for k, v in required.items())
            draw_text(SCREEN, ingredient_line[:34], 786, 445, SMALL)
            draw_text(SCREEN, ingredient_line[34:68], 786, 465, SMALL)
        else:
            draw_text(SCREEN, "Choose an order card", 790, 220, FONT, MUTED)
            draw_text(SCREEN, "to prepare a meal.", 790, 247, FONT, MUTED)
            draw_button(SCREEN, (786, 310, 270, 45), "PREPARE MEAL", GREEN, False)
            draw_button(SCREEN, (786, 365, 270, 45), "SERVE CUSTOMER", BLUE, False)
                   
        draw_text(SCREEN, "INGREDIENT STOCK", 786, 490, SMALL, MUTED)
        stock_line = f"Bun {self.stock['bun']}  Patty {self.stock['patty']}  Potato {self.stock['potato']}"
        draw_text(SCREEN, stock_line, 786, 513, SMALL, CREAM)

    def draw_footer(self):
        rounded(SCREEN, (24, 574, WIDTH - 48, 122), PANEL, 18)
                        
        draw_button(SCREEN, (42, 591, 185, 42), "RANK WAIT TIME", ORANGE)
        draw_button(SCREEN, (239, 591, 185, 42), "QUICK ORDER", BLUE)
        draw_button(SCREEN, (436, 591, 185, 42), "RECIPE GUIDE", PANEL_LIGHT)
        draw_text(SCREEN, "SERVED", 658, 590, SMALL, MUTED)
        draw_text(SCREEN, self.served, 658, 610, MEDIUM, GREEN)
        draw_text(SCREEN, "LEFT", 750, 590, SMALL, MUTED)
        draw_text(SCREEN, self.missed, 750, 610, MEDIUM, RED)
        draw_text(SCREEN, "SHIFT TIP", 835, 590, SMALL, MUTED)
        draw_text(SCREEN, "Serve fast for bigger tips!", 835, 612, SMALL, YELLOW)
        if self.notice_time > 0:
            rounded(SCREEN, (42, 646, WIDTH - 84, 34), DARK, 9)
            draw_text(SCREEN, self.notice, 54, 653, SMALL, self.notice_color)

    def draw_menu(self):
        SCREEN.fill(BG)
                                       
        rounded(SCREEN, (85, 70, WIDTH - 170, 570), PANEL, 30)
        rounded(SCREEN, (125, 110, WIDTH - 250, 490), PANEL_LIGHT, 24)
        draw_center(SCREEN, "RESTAURANT", (WIDTH // 2, 190), SMALL, MUTED)
        draw_center(SCREEN, "RUSH", (WIDTH // 2, 255), TITLE, ORANGE)
        draw_center(SCREEN, "A fast-paced restaurant management game", (WIDTH // 2, 315), FONT, CREAM)
        draw_center(SCREEN, "Take orders • Prepare meals • Keep customers happy", (WIDTH // 2, 354), FONT, MUTED)
        draw_button(SCREEN, (WIDTH // 2 - 130, 410, 260, 58), "START SHIFT", GREEN)
        draw_center(SCREEN, "90 seconds per shift  |  No external images required", (WIDTH // 2, 500), SMALL, MUTED)
        draw_center(SCREEN, "Group 8 • Python + Pygame", (WIDTH // 2, 545), SMALL, MUTED)

    def draw_game_over(self):
        SCREEN.fill(BG)
        rounded(SCREEN, (170, 80, WIDTH - 340, 550), PANEL, 26)
        draw_center(SCREEN, "SHIFT COMPLETE", (WIDTH // 2, 165), BIG, ORANGE)
        result = "Great service!" if self.score >= 180 and self.satisfaction > 25 else "Keep practicing!"
        draw_center(SCREEN, result, (WIDTH // 2, 220), MEDIUM, GREEN if result == "Great service!" else YELLOW)
        stats = [
            f"Final score: {self.score}",
            f"Customers served: {self.served}",
            f"Orders abandoned: {self.missed}",
            f"Customer satisfaction: {self.satisfaction}%",
        ]
        for i, line in enumerate(stats):
            draw_center(SCREEN, line, (WIDTH // 2, 285 + i * 42), FONT, CREAM)
        draw_button(SCREEN, (WIDTH // 2 - 140, 480, 280, 54), "PLAY AGAIN", GREEN)
        draw_center(SCREEN, "Press ESC to quit", (WIDTH // 2, 560), SMALL, MUTED)

    def draw_recipe_guide(self):
        SCREEN.fill(BG)
        rounded(SCREEN, (110, 55, WIDTH - 220, HEIGHT - 110), PANEL, 24)
        draw_text(SCREEN, "RECIPE GUIDE", 150, 85, BIG, ORANGE)
        draw_text(SCREEN, "Base ingredients are checked against your unique ingredient set and stock.", 150, 145, SMALL, MUTED)
        y = 195
        for name, recipe in RECIPES.items():
            items = expand_recipe(name)
            line = ", ".join(f"{ingredient} x{amount}" for ingredient, amount in items.items())
            rounded(SCREEN, (150, y, WIDTH - 300, 55), PANEL_LIGHT, 12)
            draw_text(SCREEN, name, 170, y + 8, FONT, GREEN)
            draw_text(SCREEN, line, 360, y + 10, SMALL, CREAM)
            y += 68
        draw_button(SCREEN, (150, 590, 180, 44), "BACK TO SHIFT", BLUE)

    def draw(self):
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "playing":
            SCREEN.fill(BG)
            self.draw_header()
            self.draw_restaurant()
            self.draw_footer()
        elif self.state == "over":
            self.draw_game_over()
        elif self.state == "recipes":
            self.draw_recipe_guide()
        pygame.display.flip()

    def handle_click(self, pos):
        if self.state == "menu":
            if pygame.Rect(WIDTH // 2 - 130, 410, 260, 58).collidepoint(pos):
                self.reset_game()
            return
        if self.state == "over":
            if pygame.Rect(WIDTH // 2 - 140, 480, 280, 54).collidepoint(pos):
                self.reset_game()
            return
        if self.state == "recipes":
            if pygame.Rect(150, 590, 180, 44).collidepoint(pos):
                self.state = "playing"
            return

                             
        for index, order in enumerate(self.orders[:6]):
            card_rect = pygame.Rect(342, 207 + index * 54, 388, 46)
            if card_rect.collidepoint(pos):
                self.selected_id = order["id"]
                self.set_notice(f"Selected order #{order['id']}: {order['dish']}.", BLUE)
                return

        if pygame.Rect(786, 310, 270, 45).collidepoint(pos):
            self.prepare_selected()
        elif pygame.Rect(786, 365, 270, 45).collidepoint(pos):
            self.serve_selected()
        elif pygame.Rect(42, 591, 185, 42).collidepoint(pos):
            self.sort_by_wait()
        elif pygame.Rect(239, 591, 185, 42).collidepoint(pos):
            self.choose_shortest_prep()
        elif pygame.Rect(436, 591, 185, 42).collidepoint(pos):
            self.state = "recipes"

    def run(self):
        while True:
            dt = CLOCK.tick(FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.state == "recipes":
                            self.state = "playing"
                        elif self.state in ("playing", "over"):
                            pygame.quit()
                            sys.exit()
                    if self.state == "playing" and event.key == pygame.K_b:
                        self.sort_by_wait()
                    if self.state == "playing" and event.key == pygame.K_s:
                        self.choose_shortest_prep()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(event.pos)
            self.update(dt)
            self.draw()


if __name__ == "__main__":
    RestaurantRush().run()