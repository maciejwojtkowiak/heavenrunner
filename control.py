from kivy.uix.relativelayout import RelativeLayout
def on_touch_down(self, touch):
        if touch.x < self.width/2:
            self.go_to_right = False
            self.go_to_left = True
        else:
            self.go_to_left = False
            self.go_to_right = True
        return super(RelativeLayout,self).on_touch_down(touch)
            

def keyboard_hidden(self):
        self._keyboard.unbind(on_key_down=self.on_keyboard_down)
        self._keyboard.unbind(on_key_up=self.on_keyboard_up)
        self._keyboard = None

def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'right':
             self.go_to_left = False
             self.go_to_right = True
        elif keycode[1] == 'left':
            self.go_to_right = False
            self.go_to_left = True
        return True

def on_keyboard_up(self, keyboard, keycode):
    return True