import arcade
import math
import example
import evaluate
import re
import cut
import sqlite3
import os
import multiprocessing as mp

height = width = 480
k = height//16
rad = k//2
start_field = k
end_field = 15*k


def init_dimensions(height):
    global k
    global rad
    global start_field
    global end_field
    k = height // 16
    rad = k // 2
    start_field = k
    end_field = 15 * k


def get_coord(num):
    return num*k


class Database:
    def insert_line(self, player, x, y, base):
        conn = sqlite3.connect(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), r'log.db'))
        cursor = conn.cursor()
        cursor.execute('insert into "{}" values(?, ?, ?)'.format(base),
                       (player, x, y))
        conn.commit()
        conn.close()

    def clear(self, base):
        conn = sqlite3.connect(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), r'log.db'))
        cursor = conn.cursor()
        cursor.execute('delete from "{}"'.format(base))
        conn.commit()
        conn.close()

    def is_empty(self, base):
        return len(self.get_all(base)) == 0

    def get_all(self, base):
        conn = sqlite3.connect(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), r'log.db'))
        cursor = conn.cursor()
        cursor.execute('select * from "{}"'.format(base))
        list = cursor.fetchall()
        conn.commit()
        conn.close()
        return list

    def get_color(self, color):
        conn = sqlite3.connect(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), r'log.db'))
        cursor = conn.cursor()
        cursor.execute('select x, y from saved where name=(?)', (color,))
        list = cursor.fetchall()
        conn.commit()
        conn.close()
        return list

    def get_first_step(self):
        conn = sqlite3.connect(os.path.join(
            os.path.dirname(os.path.abspath(__file__)), r'log.db'))
        cursor = conn.cursor()
        cursor.execute('select name from saved where x=-1')
        list = cursor.fetchall()
        conn.commit()
        conn.close()
        return list


class Player:
    def __init__(self, color, database):
        self.chip = Chip(0, 0, color)
        self.memory = [[0 for n in range(0, 15)] for n in range(0, 15)]
        self.color = 'white'
        self.db = database
        if color == arcade.color.BLACK:
            self.memory[7][7] = 1
            self.color = 'black'

    def make_step(self, x, y, others):
        if self.memory[x][y] != 1 and others[x][y] != 1:
            self.memory[x][y] = 1
            self.db.insert_line(self.color, x, y, "mylog")
            if self.victory_check():
                return "VICTORY " + self.color
            return True
        return False

    def victory_check(self):
        pat = re.compile(r'1{5}')
        mem = cut.main(self.memory, 0)
        slices = evaluate.get_slices(mem[0])
        for sl in slices:
            for e in sl.values():
                mo = re.search(pat, e)
                if mo:
                    return True
        return False

    def in_bounds(self, n):
        return 14 >= n > 0

    def draw_chips(self):
        for x in range(0, 15):
            for y in range(0, 15):
                if self.memory[x][y] == 1:
                    self.chip.y = get_coord(y+1)
                    self.chip.x = get_coord(x+1)
                    self.chip.draw()


class Chip:
    def __init__(self, x, y, col):
        self.x = x
        self.y = y
        self.col = col

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, rad, self.col)


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, False, True)
        self.my_init()

    def my_init(self):
        self.queue = mp.Queue()
        self.db = Database()
        self.victory = False
        self.thinking = False
        self.menu = Menu(self.db)
        self.stepped = ""
        self.first_player_step = False
        self.player1 = Player(arcade.color.BLACK, self.db)
        self.player2 = Player(arcade.color.WHITE, self.db)
        arcade.set_background_color(arcade.color.BISQUE)
        self.chip = Chip(k * 8, k * 8, arcade.color.BRIGHT_GREEN)
        self.last_chip = Chip(k * 8, k * 8, arcade.color.DARK_RED)

    def on_close(self):
        self.db.clear('mylog')
        self.close()

    def on_resize(self, wdth, hght):
        super().on_resize(wdth, hght)
        if self.menu.show:
            self.menu.on_resize(wdth, hght)
        global width
        global height
        if wdth >= hght:
            init_dimensions(hght)
        else:
            init_dimensions(wdth)
        width = wdth
        height = hght
        self.set_chip_coord(self.chip, self.chip.x, self.chip.y)

    def set_chip_coord(self, chip, x, y):
        point = self.find_point(x, y)
        if self.in_bounds_pixel(point[0], point[1]):
            chip.x = point[0]
            chip.y = point[1]

    def get_field(self):
        field = [[0 for n in range(0, 15)] for n in range(0, 15)]
        f1 = self.player1.memory
        d1 = len(f1)
        for x in range(0, d1):
            for y in range(0, d1):
                field[x][y] = f1[x][y]
        f2 = self.player2.memory
        d2 = len(f2)
        for x in range(0, d2):
            for y in range(0, d2):
                field[x][y] = f2[x][y]*2 if field[x][y] != 1 else field[x][y]
        return field

    def messing_with_log(self):
        log = self.db.get_all('mylog')
        if len(log) > 10:
            list_offset = len(log) - 10
            log = log[list_offset:]
        off = 0
        for tup in log:
            stri = tup[0]
            stri += " " + str(tup[1])
            stri += " " + str(tup[2])
            arcade.draw_text(stri, 15 * k + 10, height - 3 * k - 125 - off,
                             arcade.color.AZURE, 20,
                             font_name="FFF_Tusj")
            off += 25

    def show_move(self, show_move):
        if show_move:
            move = "white move"
            if self.first_player_step:
                move = "black move"
            arcade.draw_text(move, k, height-k,
                             arcade.color.AZURE, 20,
                             font_name="FFF_Tusj")

    def main_draw(self, color):
        arcade.draw_lrtb_rectangle_filled(0, width, height,
                                          0, color)
        arcade.draw_rectangle_filled(k * 8, k * 8, 14 * k, 14 * k,
                                     arcade.color.SEASHELL)
        arcade.draw_rectangle_outline(k * 8, k * 8, 4 * k, 4 * k,
                                      arcade.color.SADDLE_BROWN, 3)
        for num in range(1, 16):
            arcade.draw_line(get_coord(num), start_field,
                             get_coord(num), end_field,
                             arcade.color.DARK_RED, 1)
            arcade.draw_line(start_field, get_coord(num),
                             end_field, get_coord(num),
                             arcade.color.DARK_RED, 1)
        arcade.draw_text("press SPACE\n  to return\n   to menu",
                         15 * k + 10, height - 3 * k - 5,
                         arcade.color.AZURE, 20,
                         font_name="FFF_Tusj")
        arcade.draw_text("press S\n  to save\n   the game",
                         15 * k + 10, height - 3 * k - 95,
                         arcade.color.AZURE, 20,
                         font_name="FFF_Tusj")

    def my_on_draw(self, color, show_move):
        self.main_draw(color)
        self.messing_with_log()
        self.show_move(show_move)
        self.player1.draw_chips()
        self.player2.draw_chips()
        self.chip.draw()
        self.last_chip.draw()

    def victory_update(self):
        arcade.draw_lrtb_rectangle_filled(0, width, height, 0,
                                          arcade.color.BISQUE)
        arcade.draw_text(self.victory, width // 7, height // 7 * 4,
                         arcade.color.AZURE, 40,
                         font_name="FFF_Tusj")
        arcade.draw_text("press SPACE to return to menu",
                         width // 7, height // 7 * 3,
                         arcade.color.AZURE, 20,
                         font_name="FFF_Tusj")

    def thinking_update(self):
        self.my_on_draw(arcade.color.AMARANTH, False)
        arcade.draw_text("black move", k, height - k,
                         arcade.color.AZURE, 20,
                         font_name="FFF_Tusj")
        arcade.draw_text("CPU is thinking", 1.5 * k, height // 7 * 4,
                         arcade.color.AZURE, 40,
                         font_name="FFF_Tusj")
        self.set_mouse_visible(True)

    def on_draw(self):
        if self.queue.qsize() > 0:
            x1 = self.queue.get()
            y1 = self.queue.get()
            self.stepped = self.player1.make_step(y1, x1,
                                                  self.player2.memory)
            if self.stepped == "VICTORY black":
                self.victory = self.stepped
            self.last_chip.x = get_coord(y1 + 1)
            self.last_chip.y = get_coord(x1 + 1)
            self.thinking = False
        if self.menu.ask:
            self.menu.ask.ask_update()
        elif self.menu.show:
            self.menu.on_draw()
        elif self.victory:
            self.my_on_draw(arcade.color.BISQUE, True)
            arcade.draw_lrtb_rectangle_filled(0, width, height, 0,
                                              (255, 228, 196, 180))
            arcade.draw_text(self.victory, width // 20, height // 7 * 6,
                             arcade.color.AMARANTH, 40,
                             font_name="FFF_Tusj")
            arcade.draw_text("press SPACE to return to menu",
                             width // 20, height // 9 * 7,
                             arcade.color.CERULEAN_BLUE, 20,
                             font_name="FFF_Tusj")
        elif self.thinking:
            self.thinking_update()
        else:
            self.my_on_draw(arcade.color.BISQUE, True)

    def in_bounds_pixel(self, x, y):
        return x >= start_field and x <= end_field\
            and y >= start_field and y <= end_field

    def on_mouse_motion(self, x, y, dx, dy):
        if not self.menu.show:
            self.set_chip_coord(self.chip, x, y)

    def get_index_from_point(self, x):
        x -= 1
        x //= k
        x = 0 if x < 0 else 14 if x > 14 else x
        return x

    def DB_points_to_memory(self, color):
        points = self.db.get_color(color)
        mem = [[0 for n in range(0, 15)] for n in range(0, 15)]
        for e in points:
            y = e[1]
            x = e[0]
            mem[x][y] = 1
        if color == "black":
            self.player1.memory = mem
        elif color == "white":
            self.player2.memory = mem

    def set_game_state(self):
        self.DB_points_to_memory("black")
        self.DB_points_to_memory("white")
        wow = self.db.get_first_step()
        if wow[0][0] == "False":
            self.first_player_step = False
        else:
            self.first_player_step = True

    def turn_off_ask_show(self):
        self.menu.show = False
        self.menu.ask = False

    def save_press(self):
        self.db.clear('saved')
        if self.first_player_step:
            self.db.insert_line("True", -1, -1, 'saved')
        else:
            self.db.insert_line("False", -1, -1, 'saved')
        self.write_memory_to_DB(self.player1.memory, "black")
        self.write_memory_to_DB(self.player2.memory, "white")

    def on_key_press(self, symbol: int, modifiers: int):
        if self.menu.ask:
            self.menu.ask.ask_press(symbol)
            if symbol == arcade.key.ENTER:
                if self.menu.ask.result == 'yes':
                    self.set_game_state()
                    if self.menu.mode and self.first_player_step:
                        self.CPU_move()
                self.turn_off_ask_show()
        elif self.menu.show:
            res = self.menu.on_key_press(symbol, modifiers)
            if res == "close":
                self.on_close()
        elif symbol == arcade.key.SPACE:
            self.db.clear('mylog')
            self.my_init()
        elif symbol == arcade.key.S:
            self.save_press()

    def write_memory_to_DB(self, mem, name):
        my_list = []
        for x in range(0, len(mem)):
            for y in range(0, len(mem[0])):
                if mem[x][y] != 0:
                    my_list.append([name, x, y])
        for e in my_list:
            self.db.insert_line(e[0], e[1], e[2], 'saved')

    def CPU_move(self):
        self.set_mouse_visible(False)
        self.thinking = True
        my_m = self.get_field()
        my_queue = mp.Queue()
        my_p = mp.Process(target=example.main,
                          args=(my_m, my_queue,), daemon=True)
        my_p.start()
        self.queue = my_queue

    def my_on_mouse_press(self, button, x, y):
        if not self.menu.show and not self.victory and not self.thinking:
            if button == arcade.MOUSE_BUTTON_LEFT:
                point = self.find_point(x, y)
                chip_x = self.get_index_from_point(point[0])
                chip_y = self.get_index_from_point(point[1])
                stepped = ""
                if self.first_player_step:
                    if not self.menu.mode:
                        stepped = self.player1.make_step(chip_x, chip_y,
                                                         self.player2.memory)
                        if stepped == "VICTORY black":
                            self.victory = stepped
                else:
                    stepped = self.player2.make_step(chip_x, chip_y,
                                                     self.player1.memory)
                    if stepped == "VICTORY white":
                        self.victory = stepped
                    if self.menu.mode:
                        self.CPU_move()
                    if self.stepped == "VICTORY black" \
                            and stepped != "VICTORY white":
                        self.victory = self.stepped
                if (stepped or self.stepped) and not self.menu.mode:
                    self.first_player_step = not self.first_player_step

    def on_mouse_press(self, x, y, button, modifiers):
        self.my_on_mouse_press(button, x, y)

    def find_closest(self, n):
        lesser = n//k * k
        larger = lesser+k
        if n - lesser < larger - n:
            return lesser
        return larger

    def find_point(self, x, y):
        x_close = self.find_closest(x)
        y_close = self.find_closest(y)
        first_point = (x_close, y_close)
        second_point = (y_close, x_close)
        dist1 = math.sqrt((x-first_point[0])**2+(y-first_point[1])**2)
        dist2 = math.sqrt((x-first_point[1])**2+(y-first_point[0])**2)
        if dist1 < dist2:
            return first_point
        return second_point


class Ask:
    def __init__(self):
        self.ask_set_buttons(width, height)
        self.result = None

    def __bool__(self):
        return True

    def ask_set_buttons(self, width, height):
        color1 = arcade.color.AERO_BLUE
        color2 = arcade.color.AQUAMARINE
        delta_w = width // 3
        delta_h = height // 3
        self.b1 = Button(delta_w + 25, delta_w + 80, delta_h *
                         2 - 115, delta_h * 2 - 160, color1, 'yes')
        self.b2 = Button(delta_w + 95,
                         delta_w + 145,
                         delta_h * 2 - 115,
                         delta_h * 2 - 160, color2,
                         "no")
        self.b2.checked = True

    def ask_update(self):
        delta_w = width // 3
        delta_h = height // 3
        arcade.draw_lrtb_rectangle_filled(delta_w, delta_w * 2,
                                          delta_h * 2, height // 4,
                                          arcade.color.BABY_BLUE)
        arcade.draw_text("You have a saved\ngame."
                         "\nDo you want to\n continue it?",
                         delta_w + 5, delta_h * 2 - 110,
                         arcade.color.AMERICAN_ROSE, 20, font_name="FFF_Tusj")
        self.b1.draw_button()
        self.b2.draw_button()

    def ask_press(self, symbol):
        color1 = arcade.color.AERO_BLUE
        color2 = arcade.color.AQUAMARINE
        if symbol == arcade.key.LEFT:
            self.b1.checked = True
            self.b2.checked = False
            self.b1.color = color2
            self.b2.color = color1
        elif symbol == arcade.key.RIGHT:
            self.b2.checked = True
            self.b1.checked = False
            self.b2.color = color2
            self.b1.color = color1
        elif symbol == arcade.key.ENTER:
            if self.b1.checked:
                self.result = 'yes'


class Menu:
    def __init__(self, database):
        self.checked = None
        self.db = database
        self.show = True
        self.ask = None
        self.mode = True
        self.color1 = arcade.color.AERO_BLUE
        self.color2 = arcade.color.AQUAMARINE
        self.set_buttons(width, height)

    def set_buttons(self, width, height):
        new_h = height // 15
        self.b1 = Button(0, width, new_h * 12, new_h * 10,
                         self.color1, "2 players")
        self.b2 = Button(0, width, new_h * 9, new_h * 7, self.color1,
                         "Play with bot")
        self.b3 = Button(0, width, new_h * 6, new_h * 4, self.color2, "Exit")
        self.checked = self.b3
        self.b1.upper_button = self.b3
        self.b1.lower_button = self.b2
        self.b2.upper_button = self.b1
        self.b2.lower_button = self.b3
        self.b3.upper_button = self.b2
        self.b3.lower_button = self.b1

    def on_resize(self, width, height):
        self.set_buttons(width, height)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("RENDZU", 50, height//5*4,
                         arcade.color.CERULEAN_BLUE,
                         50, font_name="FFF_Tusj")
        self.b1.draw_button()
        self.b2.draw_button()
        self.b3.draw_button()

    def change_checked(self, next_button):
        self.checked.color = self.color1
        self.checked = next_button
        self.checked.color = self.color2

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.UP:
            self.change_checked(self.checked.upper_button)
        elif symbol == arcade.key.DOWN:
            self.change_checked(self.checked.lower_button)
        elif symbol == arcade.key.ENTER:
            if self.checked == self.b3:
                return "close"
            self.mode = False
            if self.checked == self.b2:
                self.mode = True
            if not self.db.is_empty('saved'):
                self.ask = Ask()
            else:
                self.show = False


class Button:
    def __init__(self, l, r, t, b, col, text):
        self.left = l
        self.right = r
        self.top = t
        self.bottom = b
        self.color = col
        self.text = text
        self.upper_button = None
        self.lower_button = None
        self.checked = False

    def draw_button(self):
        deltay = (self.top-self.bottom)//3*2
        font_size = (self.top-self.bottom)//5*2
        arcade.draw_lrtb_rectangle_filled(self.left, self.right,
                                          self.top, self.bottom, self.color)
        text_x = self.left+10
        text_y = self.top-deltay
        arcade.draw_text(self.text, text_x, text_y,
                         arcade.color.BLACK, font_size, font_name="FFF_Tusj")


def main():
    MyGame(width+200, height, "rendzu")
    arcade.run()


if __name__ == '__main__':
    main()
