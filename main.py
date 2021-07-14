from sys import platform
from kivy.config import Config
Config.set('graphics', 'width', '900') 
Config.set('graphics', 'height', '400')
from kivy.uix.relativelayout import RelativeLayout
from kivy.app import App
from kivy.graphics import Line
from kivy.graphics import Color
from kivy.clock import Clock
from kivy.graphics.vertex_instructions import Triangle
from kivy.graphics import Quad
from random import randint
from kivy.core.window import Window
from kivy.utils import platform
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.core.audio import SoundLoader

Builder.load_file("menu.kv")



class Game(RelativeLayout):
    from control import on_touch_down, on_keyboard_down, keyboard_hidden, on_keyboard_up
    #ObjectProperties
    menu_canvas = ObjectProperty()
    score_widget = ObjectProperty()
    easy_button_widget = ObjectProperty()
    medium_button_widget = ObjectProperty()
    hard_button_widget = ObjectProperty()

    #Vertical lines variables
    V_LINES = 3
    vertical_lines = []
    V_spacing = .1

    #Horizontal lines variables
    H_LINES = 10
    H_SPACING = .2
    horizontal_lines = []

    #Offset
    offset_y = 0

    # SPEED
    GAME_SPEED = 0
    current_game_speed = 0
    
    #Hero position
    hero = None
    hero_cords = [(0,0),(0,0),(0,0)]
    base_height = 0.04
    hero_width = 0.04
    hero_height = 0.08

    # quad stuff
    quad_nb = 15
    quad_x = 0
    quad_y = -1
    quads = []
    quads_coordinates = []

    # number of loops
    loop_number = 0

    # Booleans
    go_to_right = True
    go_to_left = True
    game_over = False
    game_started = False

    #Button booleans
    level_selected = False
    easy_selected = False
    medium_selected = False
    hard_selected = False
   
    # Menu texts
    button_text = StringProperty("Start")
    label_text = StringProperty("Welcome   in   Heaven   Runner")

    #Score
    score = NumericProperty()
    score_Label = StringProperty()
    end_score = 0
    last_Score = []
    last_Score_Label = StringProperty()

    #Sounds
    start_sound = SoundLoader.load("music/startSound.wav")
    main_theme = SoundLoader.load("music/mainTheme.wav")
    game_over_boom = SoundLoader.load("music/gameOverBoom.wav")

    #game number
    game_number = 0

    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.start_sound.play()
        self.init_vertical_line()
        self.init_horizontal_line()
        self.init_quad()
        self.init_hero()
        self.start_quads()
        self.quad_generation()
        if self.is_desktop():
            self.keyboard = Window.request_keyboard(self.keyboard_hidden, self)
            self.keyboard.bind(on_key_down=self.on_keyboard_down)
            self.keyboard.bind(on_key_up=self.on_keyboard_up)
        Clock.schedule_interval(self.update, 1/60)

    def game_restart(self):
        self.quads_coordinates = []
        self.loop_number = 0
        self.start_quads()
        self.quad_generation()
        
    def is_desktop(self):
        if platform in "win, linux, macosx":
            return True
        return False
    def init_hero(self):
            with self.canvas:
                Color(0,1,0)
                self.hero = Triangle(points=(0,0,0,0,0,0))

    def update_hero(self):
        center_x = int(self.width/2) 
        spacing = self.V_spacing * self.width 
        ymax = self.height * self.hero_height
        ymin = self.height * self.hero_height
        if self.game_started:
            if self.go_to_left is True:
                self.hero_cords[0] = (center_x - spacing*.25, ymin)
                self.hero_cords[1] = (center_x - spacing *.5, ymax + ymin)
                self.hero_cords[2] = (center_x - spacing*.75, ymin)
                x1, y1 = (center_x - spacing*.25, ymin)
                x2, y2 = (center_x - spacing *.5, ymax + ymin)
                x3, y3 = (center_x - spacing*.75, ymin)
                self.hero.points = [ x1,y1,x2,y2,x3,y3]


            if self.go_to_right is True:
                self.hero_cords[0] = (center_x + spacing*.25, ymin)
                self.hero_cords[1] = (center_x + spacing *.5, ymax + ymin)
                self.hero_cords[2] = (center_x + spacing*.75, ymin)
                x1, y1 = (center_x + spacing*.25, ymin)
                x2, y2 = (center_x + spacing *.5, ymax + ymin)
                x3, y3 = (center_x + spacing*.75, ymin)
                self.hero.points = [ x1,y1,x2,y2,x3,y3]

    def hero_collision(self, quad_x, quad_y):
        xmin,ymin = self.get_quad_cord(quad_x, quad_y)
        xmax,ymax = self.get_quad_cord(quad_x + 1, quad_y + 1)
        if self.go_to_right is True:
               px,py =  self.hero_cords[1]
               if  xmin <= px <=  xmax and ymin <= py <=  ymax:
                return True
        if self.go_to_left is True:
               px,py =  self.hero_cords[1]
               if  xmin <= px <=  xmax and ymin <= py <=  ymax:
                return True
        return False

    def check_hero_collision(self):
        for i in range (0, len(self.quads_coordinates)):
            quad_x, quad_y = self.quads_coordinates[i]
            if self.hero_collision(quad_x, quad_y):
                return True
        return False
                
    def init_vertical_line(self):
            with self.canvas:
                Color(1, 1, 1)
                for i in range(0, self.V_LINES):
                    self.vertical_lines.append(Line())

    def init_quad(self):
            with self.canvas:
                Color(1, 1, 1)
                for i in range(0, self.quad_nb):
                    self.quads.append(Quad())
    def start_quads(self):
        for i in range(0,15):
            self.quads_coordinates.append((0,i))
            self.quads_coordinates.append((-1,i))
    def quad_generation(self):
        last_y = 0
        last_x = 0

        for i in range (len(self.quads_coordinates)-1, -1, -1):

            if self.quads_coordinates[i][1] < self.loop_number:
                del self.quads_coordinates[i]
        
        if len(self.quads_coordinates) > 0:
           last_coordinates = self.quads_coordinates[-1]
           last_x = last_coordinates[0] 
           last_y = last_coordinates[1] + 1
                

        for i in range(len(self.quads_coordinates), self.quad_nb):
            r = randint(0, 1)
            self.quads_coordinates.append((last_x, last_y))
            if r == 0:
                last_x =-1
                self.quads_coordinates.append((last_x, last_y))
                last_y += 1
                self.quads_coordinates.append((last_x, last_y))
            if last_x <= - 1:
                last_x += 1
            if r == 1:
                last_x = 0
                self.quads_coordinates.append((last_x, last_y))
                last_y += 1
                self.quads_coordinates.append((last_x, last_y))
            if last_x >= 0:
                last_x -= 1

    def get_quad_cord(self, quad_x, quad_y):
        quad_y = quad_y - self.loop_number
        x = self.vertical_line_from_index(quad_x)
        #print("X VALUE IS " + str(x))
        y = self.horizontal_line_from_index(quad_y)
        #print("Y VALUE IS " + str(y))
        return x, y

    def quad_update(self):
        for i in range(0, self.quad_nb):
            quad = self.quads[i]
            quad_coordinate = self.quads_coordinates[i]
            xmin, ymin = self.get_quad_cord(quad_coordinate[0], quad_coordinate[1])
            xmax, ymax = self.get_quad_cord(quad_coordinate[0] + 1, quad_coordinate[1] + 1)
            x1, y1 = xmin,ymin
            x2, y2 = xmin, ymax
            x3, y3 = xmax, ymax
            x4, y4 = xmax, ymin
            quad.points = [x1, y1, x2, y2, x3, y3, x4, y4] 

    def vertical_line_from_index(self, index):
        center_x = int(self.width/2) 
        spacing = self.V_spacing * self.width 
        offset = index 
        line_x = center_x + offset * spacing
        return line_x

    def update_vertical_lines(self):
        first_index = -int(self.V_LINES / 2) 
        for i in range (first_index, first_index + self.V_LINES):
            line_x = self.vertical_line_from_index(i)
            self.vertical_lines[i].points = [line_x, 0, line_x , self.height]

    
    def init_horizontal_line(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range (0, self.H_LINES):
                self.horizontal_lines.append(Line())

    def horizontal_line_from_index(self, index):
        y_spacing = self.H_SPACING * self.height
        line_y = y_spacing * index - self.offset_y
        return line_y

    def update_horizontal_line(self):
        center_x = int(self.width/2)
        spacing_y = self.V_spacing * self.width 
        offset = -int(self.V_LINES/2) 
        xmin = center_x + offset * spacing_y 
        xmax = center_x - offset * spacing_y 

        for i in range(0, self.H_LINES):
            line_y =  self.horizontal_line_from_index(i)
            x1, y1 = (xmin, line_y)
            x2, y2 = (xmax, line_y)
            self.horizontal_lines[i].points = [x1, y1, x2, y2]

    def easy_level(self):
        if self.easy_button_widget.state == "down":
            self.level_selected = True
            self.GAME_SPEED = 0.5
            self.medium_button_widget.state = "normal" 
            self.hard_button_widget.state = "normal"
           
    def medium_level(self):
        if self.medium_button_widget.state == "down":
            self.level_selected = True
            self.GAME_SPEED = 1
            self.easy_button_widget.state  = "normal"  
            self.hard_button_widget.state = "normal"


    def hard_level(self):
        if self.hard_button_widget.state == "down":
            self.level_selected = True
            self.GAME_SPEED = 2
            self.easy_button_widget.state  = "normal"
            self.medium_button_widget.state = "normal"

    def update(self, dt):
        time_factor =  dt*60
        self.update_vertical_lines()
        self.update_horizontal_line()
        self.quad_update()
        self.quad_generation()
        self.update_hero()
        self.score_board()

        if not self.check_hero_collision() and not self.game_over and self.game_started:
            self.game_over_boom.play()
            self.main_theme.stop()
            self.button_text = "Try again"
            self.game_over = True
            self.game_started = False

        if self.game_over and not self.game_started:
            self.score_widget.opacity = 0
            self.menu_canvas.opacity = 1
            self.label_text = "Your score: " + str(self.score) 

        if not self.game_over and self.game_started:
            y_spacing = self.H_SPACING * self.height
            self.current_game_speed = (self.GAME_SPEED * self.height / 100)  * time_factor
            self.offset_y += self.current_game_speed
            if self.offset_y >= y_spacing:
                self.offset_y -= y_spacing
                self.loop_number += 1
                self.score = self.loop_number
                if self.loop_number % 100 == 0:
                    self.GAME_SPEED += 0.1

    def score_board(self):
        if self.game_over:
            self.end_score = self.score
            self.last_Score.append((self.end_score))
            if len(self.last_Score) > self.game_number:
                del self.last_Score[-1]
            try:
                self.last_Score_Label = "Your last score: " + str(self.last_Score[-2])
            except:
                self.last_Score_Label = "Your last score: " +  str(self.last_Score[-1])
              
    def start_button(self):
        self.game_number +=1
        if self.level_selected:
            self.menu_canvas.opacity = 0
            self.score_widget.opacity = 1
            self.main_theme.play()
            self.start_sound.stop()
            self.game_over_boom.stop()
            self.game_started = True
            if self.game_over:
                self.game_over = False
                self.game_started = True
                self.menu_canvas.opacity = 0
                self.game_restart()

class HeavenRunner(App):
    pass

HeavenRunner().run()