from datetime import datetime
import math as m
import pygame as pg


class Rectangle:
    def __init__(self, x=0, y=0, w=0, h=0, color=''):
        self.x = x  # Position X
        self.y = y  # Position Y
        self.w = w  # Width
        self.h = h  # Height
        self.color = color

    def draw(self, screen):
        pg.draw.rect(screen, self.color,
                     (self.x, self.y, self.w, self.h), 2)


class Circle:
    def __init__(self, x, y, r, color=''):
        self.x = x  # Position X
        self.y = y  # Position Y
        self.r = r  # Radius
        self.color = color

    def draw(self, screen,):
        pg.draw.circle(screen, self.color, (self.x, self.y), self.r, 2)


class Hover(Circle):
    def __init__(self, x_circle=0, y_circle=0, r_circle=0, circle_color='', hover_chain=False, cooldown_timer=0):
        Circle.__init__(self, x_circle, y_circle, r_circle, circle_color)
        self.hover_chain = hover_chain
        self.cooldown_timer = cooldown_timer

    def isChained(self):
        if ((pg.mouse.get_pos()[0] - self.x)**2 + (pg.mouse.get_pos()[1] - self.y)**2 <= (self.r)**2):
            self.hover_chain = True
        if self.cooldown_timer < 1:
            if not (((pg.mouse.get_pos()[0] - self.x)**2 + (pg.mouse.get_pos()[1] - self.y)**2 <= (self.r)**2) or ((350 <= pg.mouse.get_pos()[0] <= (350+440)) and (40 <= pg.mouse.get_pos()[1] <= (40+330)))):
                self.hover_chain = False

    def isMouseOn(self):
        if self.hover_chain:
            return True if (((pg.mouse.get_pos()[0] - self.x)**2 + (pg.mouse.get_pos()[1] - self.y)**2 <= (self.r)**2) or ((350 <= pg.mouse.get_pos()[0] <= (350+440)) and (40 <= pg.mouse.get_pos()[1] <= (40+330)))) else False
        else:
            return True if ((pg.mouse.get_pos()[0] - self.x)**2 + (pg.mouse.get_pos()[1] - self.y)**2 <= (self.r)**2) else False

    def popup(self, x_rect=0, y_rect=0, w_rect=0, h_rect=0, rect_color='', rect_edge_color='', option_switch=False):
        popup_cooldown = False if self.isMouseOn() else True
        self.isChained()
        if popup_cooldown:
            if self.cooldown_timer > 0:
                self.cooldown_timer -= 1
        else:
            self.cooldown_timer = 150

        if self.cooldown_timer > 1:
            # draw
            pg.draw.rect(screen, rect_color, (x_rect, y_rect, w_rect, h_rect))
            pg.draw.rect(screen, rect_edge_color,
                         (x_rect, y_rect, w_rect, h_rect), 2)
            screen.blit(TextBox(black, "Scale",
                        FONT_RB_30).txt_surface, (360, 50))
            screen.blit(TextBox(black, "+ and - button changes scale by 1",
                        FONT_RB_25).txt_surface, (360, 75))
            screen.blit(TextBox(black, "+ and - key on numpad to change scale by 10",
                        FONT_RB_25).txt_surface, (360, 100))
            screen.blit(TextBox(black, "Scaling can be changed between Manual and Auto",
                        FONT_RB_25).txt_surface, (360, 125))
            screen.blit(TextBox(black, "Main scale displayed on the left are 10 cm apart",
                        FONT_RB_25).txt_surface, (360, 150))
            screen.blit(TextBox(black, "Variables",
                        FONT_RB_30).txt_surface, (360, 200))
            screen.blit(TextBox(black, "Cannot exceed the length of 3",
                        FONT_RB_25).txt_surface, (360, 225))
            screen.blit(TextBox(black, "S1: 65-303 mm    s2: 0-800 mm    degree: 0-89 ° ",
                        FONT_RB_25).txt_surface, (360, 250))
            screen.blit(TextBox(black, "Input editing options",
                        FONT_RB_30).txt_surface, (360, 300))
            screen.blit(TextBox(black, "     Backspace            Input new",
                        FONT_RB_25).txt_surface, (360, 333))
            # option switches
            option_switch = backspace.select_option(option_switch, Input_new)
            backspace.draw(screen)
            Input_new.draw(screen)
        return option_switch


class Button(Rectangle):
    def __init__(self, x=0, y=0, w=0, h=0, color='', mouse_output=False, press=[], auto=[False, False]):
        Rectangle.__init__(self, x, y, w, h, color)
        self.mouse_output = mouse_output
        self.press = press
        self.auto = auto

    def isMouseOn(self):
        return True if self.x <= pg.mouse.get_pos()[0] <= (self.x + self.w) and self.y <= pg.mouse.get_pos()[1] <= (self.y + self.h) else False

    def isPressed(self, var, value):
        if self.isMouseOn():
            if pg.mouse.get_pressed()[0]:
                pg.draw.rect(screen, ACTIVE,
                             (self.x, self.y, self.w, self.h), 5)
                for i in range(len(var)):
                    var[i] = value[i]
            else:
                pg.draw.rect(screen, ACTIVE,
                             (self.x, self.y, self.w, self.h), 2)
        else:
            pg.draw.rect(screen, self.color,
                         (self.x, self.y, self.w, self.h), 2)
        return var
    # optimised mouse input

    def mouse_logic(self, mouse_trig):
        mouse_release = True if pg.mouse.get_pressed()[0] == False else False
        if mouse_release:  # if mouse button is released
            mouse_trig[0] = True
        if not mouse_release:  # if mouse button is pressed
            mouse_trig[1] = True
        # trigger only if mouse button already pressed and releasde at least once
        if mouse_trig == [True, True]:
            self.press.append('pressed')
            # trigger only when mouse button pressed but not when release
            mouse_trig = [False, False]
        if len(self.press) == 2:
            # output = True
            self.mouse_output = not self.mouse_output
            self.press = []
        return mouse_trig

    # Manual to auto with a click and vice versa.
    def toggle_auto(self, var, Auto_Manual_text_toggle):
        if self.isMouseOn():
            self.auto = self.mouse_logic(self.auto)
            if self.mouse_output:
                pg.draw.rect(screen, ACTIVE,
                             (self.x, self.y, self.w, self.h), 5)
                Auto_Manual_text_toggle = True
                var = True
            else:
                pg.draw.rect(screen, ACTIVE,
                             (self.x, self.y, self.w, self.h), 2)
                Auto_Manual_text_toggle = False
                var = False
        else:
            pg.draw.rect(screen, black, (self.x, self.y, self.w, self.h), 2)
        return var, Auto_Manual_text_toggle

    def isPressed_with_condition(self, var, increment, mouse_trig, Auto_Manual_text_toggle):
        if Auto_Manual_text_toggle:
            pg.draw.rect(screen, ACTIVE,
                         (self.x, self.y, self.w, self.h), 2)
        else:
            if self.isMouseOn():
                mouse_trig = self.mouse_logic(mouse_trig)
                if self.mouse_output:
                    pg.draw.rect(screen, ACTIVE,
                                 (self.x, self.y, self.w, self.h), 5)
                    var += increment
                    self.mouse_output = False
                else:
                    pg.draw.rect(screen, ACTIVE,
                                 (self.x, self.y, self.w, self.h), 2)
            else:
                pg.draw.rect(screen, self.color,
                             (self.x, self.y, self.w, self.h), 2)
        return var, mouse_trig

    def select_option(self, option_switch, pair):
        if self.isMouseOn():
            if pg.mouse.get_pressed()[0]:
                option_switch = False
        if pair.x <= pg.mouse.get_pos()[0] <= (pair.x + pair.w) and pair.y <= pg.mouse.get_pos()[1] <= (pair.y + pair.h):
            if pg.mouse.get_pressed()[0]:
                option_switch = True

        if option_switch:
            pg.draw.rect(screen, ACTIVE, (backspace.x,
                                          backspace.y, backspace.w, backspace.h))
            pg.draw.rect(screen, light_green, (Input_new.x,
                                               Input_new.y, Input_new.w, Input_new.h))
        else:
            pg.draw.rect(screen, light_green, (backspace.x,
                                               backspace.y, backspace.w, backspace.h))
            pg.draw.rect(screen, ACTIVE, (Input_new.x,
                                          Input_new.y, Input_new.w, Input_new.h))
        return option_switch


class TextBox:
    def __init__(self, col, text='', font=''):
        # self.rect = pg.Rect(x, y, w, h)
        self.color = col
        self.text = text
        self.txt_surface = font.render(text, True, self.color)

    def draw(self, Screen):
        # Blit the text.
        Screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y))


class InputBox:

    def __init__(self, x, y, w, h, text='', type='', l=100, location='', font='', color=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = color
        self.default_color = color
        self.text = text
        self.return_text = ''
        self.type = type
        self.len = l
        self.location = location
        self.txt_surface = font.render(text, True, self.color)
        self.font = font
        self.active = False
        self.enter_switch = 0

    def return_location(self, location, location_cooldown):
        if self.active == True:
            location = self.location
            location_cooldown = 0
        elif self.active == False:
            location = location
            location_cooldown = 1
        return location, location_cooldown

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:  # ทำการเช็คว่ามีการคลิก Mouse หรือไม่
            # ทำการเช็คว่าตำแหน่งของ Mouse อยู่บน InputBox นี้หรือไม่
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
                if self.active:
                    if option_switch:
                        self.text = ''
                        self.return_text = ''
            else:
                self.return_text = self.text
                self.active = False
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.return_text = self.text
                    self.active = False
                elif event.key == pg.K_KP_ENTER:
                    self.return_text = self.text
                    self.active = False
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if self.type == 'str':
                        self.text += event.unicode
                    elif self.type == 'int':
                        if event.unicode.isnumeric():
                            if len(self.text) < self.len and self.text != '0':
                                self.text += event.unicode
                        else:
                            self.text = self.text
        # Re-render the text.
        self.txt_surface = self.font.render(
            self.text, True, self.default_color)
        self.color = ACTIVE if self.active else self.default_color  # เปลี่ยนสีของ InputBox

    def update(self):
        # Resize the box if the text is too long.
        width = max(self.rect.w, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, Screen):
        # Blit the text.
        Screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y))
        # Blit the rect.
        pg.draw.rect(Screen, self.color, self.rect, 2)

    def inputbox_return(self, var, multiplier=1):
        if self.return_text != '':
            var = int(self.text)/multiplier
            self.return_text = ''
            self.enter_switch = 0
        if self.return_text == '':
            if self.active:
                self.enter_switch = 1
            else:
                self.enter_switch = 0
        return var

    def notify_user(self, text, px, py):
        if self.enter_switch == 1:
            screen.blit(TextBox(red, text, FONT_IMP_20).txt_surface, (px, py))


# Squash Object------------------------------------------------------------------------------
class Ball:
    def __init__(self, pos_x, pos_y, u, size, color, curr_x_distance, curr_y_distance):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.u = u
        self.size = size
        self.color = color
        self.curr_x_distance = curr_x_distance
        self.curr_y_distance = curr_y_distance
        self.lx = []
        self.ly = []

    def update_position(self, t):
        self.pos_x = ini_sx+(ux*(t/1000*speed_multiplier))*scale_multiplier
        self.pos_y = (ini_sy-h*scale_multiplier)-(uy*(t/1000*speed_multiplier) +
                                                  (-a*(t/1000*speed_multiplier)**2)/2)*scale_multiplier
        self.curr_x_distance = str(ux*t/1000)[:5]
        self.curr_y_distance = str(h+(uy*(t/1000)-0.5*(a*((t/1000)**2))))[:5]

    def dots_track(self, t, speed_multiplier):
        # Re-fill the background with coordinates from list
        for i, j in zip(range(len(self.lx)), range(len(self.ly))):
            pg.draw.circle(screen, black, (self.lx[i], self.ly[i]), 2)
        # Frequency of dots in the path tracer
        if (t*speed_multiplier % 80 == 0):
            self.lx.append(int(squash.pos_x))
            self.ly.append(int(squash.pos_y))

    def reset(self, pos_x, pos_y, curr_x_distance, curr_y_distance):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.curr_x_distance = curr_x_distance
        self.curr_y_distance = curr_y_distance
        self.lx = []
        self.ly = []

    def draw(self, screen, scale_multiplier):
        pg.draw.circle(screen, self.color,
                       (self.pos_x, self.pos_y), self.size*scale_multiplier)

# Simulation Object-------------------------------------------------------------------------------------


class Simulation:

    def __init__(self, t, last_t, pos_y_max, wall_logic=0):
        self.t = t
        self.last_t = last_t
        self.pos_y_max = pos_y_max
        self.wall_logic = wall_logic

    def initiate_sim(self, toggle_start):
        if self.pos_y_max > squash.pos_y:
            self.pos_y_max = squash.pos_y
        # toggleable simulation
        if toggle_start == 1:
            # dotted tracing#---------------------------------------------------------------------------------------------------#
            squash.dots_track(self.t, speed_multiplier)
            # position vector#---------------------------------------------------------------------------------------------------#
            squash.draw(screen, scale_multiplier)
            if (squash.pos_y <= ini_sy-0.35*scale_multiplier):  # run simulation
                if ((ini_sx+(1+s2)*scale_multiplier <= squash.pos_x <= (ini_sx+(1+s2)*scale_multiplier)+0.03*scale_multiplier) and (ini_sy+5-wall*scale_multiplier <= squash.pos_y <= (ini_sy+5-wall*scale_multiplier)+wall*scale_multiplier)):
                    operation.show_status(
                        1050, 425, 10, light_red, black, 'Fail')
                    operation.show_status(
                        895, 425, 10, light_blue, black, 'Frozen')
                    self.wall_logic = 1
                if self.wall_logic == 1:
                    self.last_t = self.t
                    self.t = 0
                else:
                    operation.show_status(
                        1050, 425, 10, ACTIVE, black, 'Status')
                    operation.show_status(
                        895, 425, 10, light_red, black, 'Simulating')
                    squash.update_position(self.t)
                    self.t += 1
            else:  # freeze simulation
                operation.show_status(
                    1050, 425, 10, light_green, black, 'Pass')
                operation.show_status(
                    895, 425, 10, light_blue, black, 'Frozen')
                self.last_t = self.t
                self.t = 0
            pg.draw.rect(screen, red, (0, sim.pos_y_max, win_x-400, 2))
        elif toggle_start == 0:
            operation.show_status(1050, 425, 10, ACTIVE, black, 'Status')
            operation.show_status(895, 425, 10, light_green, black, 'Ready')
            self.pos_y_max = 900
            squash.reset(ini_sx-5+(0.015*scale_multiplier), ini_sy -
                         (h*scale_multiplier), squash.curr_x_distance, squash.curr_y_distance)
            squash.draw(screen, scale_multiplier)

    def reset_sim(self, toggle_reset, toggle_start):
        if toggle_reset == 1:
            squash.reset(ini_sx, ini_sy-h*scale_multiplier, 0, h)
            self.t = 0
            toggle_reset = 0
            toggle_start = 0
            self.wall_logic = 0
        return toggle_reset, toggle_start


class Operation(Rectangle):
    def __init__(self, x=0, y=0, w=0, h=0, color=''):
        Rectangle.__init__(self, x, y, w, h, color)
    # Calculate functions----------------------------------------------------------------------------------

    def calculate(self, s1, s2, h, deg, M, k):
        u = m.sqrt((4.9*(s1+s2+2)**2)/((h-0.35+m.tan(m.radians(deg))
                                        * (s1+s2+2))*m.cos(m.radians(deg))**2))
        # print("u =", str(u)[:5])
        x = (19.6*M*m.sin(m.radians(deg)) +
             m.sqrt((19.6*M*m.sin(m.radians(deg))**2+4*k*1000*M*(u**2))))/(2*k*1000)
        # print("x =", str(x)[:5])
        H = m.tan(m.radians(deg))*(s1+1)-4.9 * \
            ((s1+1)/(u*m.cos(m.radians(deg))))**2+h
        # print("H =", str(H)[:5])
        ux = u*m.cos(m.radians(deg))
        uy = u*m.sin(m.radians(deg))
        time = (s1+s2+2)/ux
        return u, x, H, ux, uy, time

    def show_status(self, x, y, r, color, edge_color, text=''):
        pg.draw.circle(screen, color, (x, y), r)
        pg.draw.circle(screen, edge_color, (x, y), r, 2)
        screen.blit(TextBox(black, text, FONT_RB_25).txt_surface, (x+26, y-6))

    def ping_location(self, x, y, ct_G, ct_B):
        pg.draw.circle(screen, (255, 51+ct_G, 51+ct_B),
                       (x, y), ct_G/500*scale_multiplier)
        if ct_G+51 < 255:
            ct_G += 1
        else:
            ct_G = ct_G
        if ct_B+51 < 204:
            ct_B += (204/255)
        else:
            ct_B = ct_B
        return ct_G, ct_B

    def activate_ping(self, location, ct_G, ct_B):
        if location == '':
            ct_G, ct_B = 0, 0
        if location == 'degree':
            ct_G, ct_B = operation.ping_location(
                ini_sx, ini_sy-h*scale_multiplier, ct_G, ct_B)
        if location == 's2':
            ct_G, ct_B = operation.ping_location(
                ini_sx, ini_sy-h*scale_multiplier, ct_G, ct_B)
        if location == 's1':
            ct_G, ct_B = operation.ping_location(
                ini_sx+(2+s2)*scale_multiplier,
                ini_sy-0.5*h*scale_multiplier, ct_G, ct_B)
        if location == 'wall':
            ct_G, ct_B = operation.ping_location(
                ini_sx+(1+s2)*scale_multiplier, ini_sy+5-0.5*wall*scale_multiplier, ct_G, ct_B)
        return location, ct_G, ct_B

    def draw_scale(self):
        for i in range(60):
            pg.draw.rect(screen, black, (0, ini_sy-(0.1*i*scale_multiplier),
                                         0.05*scale_multiplier, 0.01*scale_multiplier))
            pg.draw.rect(screen, black, (0, ini_sy-(0.05*scale_multiplier)-(0.1*i*scale_multiplier),
                                         0.025*scale_multiplier, 0.01*scale_multiplier))

    # set field function--------------------------------------------------------------------------
    def draw_field(self, location, location_time, location_cooldown):
        pg.draw.rect(screen, bg_color_highlight,
                     (0, win_y-65, 215, 66))  # S1 input highlight
        pg.draw.rect(screen, black, (0, ini_sy+5, win_x-400, 2))  # floor
        pg.draw.rect(screen, black, (ini_sx-5, ini_sy+5-h*scale_multiplier,
                                     0.03*scale_multiplier, h*scale_multiplier))  # shooter
        pg.draw.rect(screen, black, (ini_sx+(1+s2)*scale_multiplier,
                                     ini_sy+5-wall*scale_multiplier, 0.03*scale_multiplier, wall*scale_multiplier))  # wall
        pg.draw.rect(screen, light_blue, ((ini_sx+(2+s2)*scale_multiplier),
                                          ini_sy+3, 0.433*scale_multiplier, 4))
        pg.draw.rect(screen, dark_blue, ((ini_sx+(2+s1+s2)*scale_multiplier)-(0.065*scale_multiplier),
                                         ini_sy+5-0.35*scale_multiplier, 0.13*scale_multiplier, 0.35*scale_multiplier))
        pg.draw.rect(screen, light_blue, ((ini_sx+(-0.8+s2)*scale_multiplier),
                                          ini_sy+3, 0.8*scale_multiplier, 4))
        pg.draw.rect(screen, bg_color, (win_x-400, 0, 400, win_y))
        pg.draw.rect(screen, bg_color_highlight,
                     (800, 40, 400, 60))  # output highlight
        pg.draw.rect(screen, black, (win_x-400, 0, 2, win_y))  # divider
        pg.draw.rect(screen, black, (800, 275, win_x-800, 2))
        pg.draw.rect(screen, black, (72, 554, 52, 32), 2)  # S1 inputbox shadow
        # alternative mode
        if location == 'degree':
            pg.draw.line(screen, red, (ini_sx-1, ini_sy-h*scale_multiplier),
                         (ini_sx+int((0.5*scale_multiplier) * m.cos(m.radians(deg))), ini_sy-h*scale_multiplier-int((0.5*scale_multiplier)*m.sin(m.radians(deg)))), 2)
            pg.draw.line(screen, red, (ini_sx-1, ini_sy-h*scale_multiplier),
                         (ini_sx+0.5*scale_multiplier, ini_sy-h*scale_multiplier), 2)
            pg.draw.arc(screen, red, (ini_sx-0.15*scale_multiplier, ini_sy-(h+0.15)*scale_multiplier,
                        0.3*scale_multiplier, 0.3*scale_multiplier), 0, m.radians(deg), 2)
        if location == 's1':
            pg.draw.line(screen, red, (ini_sx+(2+s2)*scale_multiplier,
                                       ini_sy), (ini_sx+(2+s2)*scale_multiplier, ini_sy-(0.34+0.05)*scale_multiplier), 2)
            pg.draw.line(screen, red, (ini_sx+(2+s1+s2)*scale_multiplier,
                                       ini_sy-0.34*scale_multiplier), (ini_sx+(2+s1+s2)*scale_multiplier, ini_sy-(0.34+0.05)*scale_multiplier), 2)
            pg.draw.line(screen, red, (ini_sx+(2+s2)*scale_multiplier, ini_sy-(0.34+0.025)*scale_multiplier),
                         (ini_sx+(2+s1+s2)*scale_multiplier, ini_sy-(0.34+0.025)*scale_multiplier), 2)
        if location == 's2':
            pg.draw.line(screen, red, (ini_sx-1, ini_sy-(h+0.05) *
                                       scale_multiplier), (ini_sx-1, ini_sy-(h+0.1)*scale_multiplier), 2)
            pg.draw.line(screen, red, (ini_sx-1+s2*scale_multiplier, ini_sy),
                         (ini_sx-1+s2*scale_multiplier, ini_sy-(h+0.1)*scale_multiplier), 2)
            pg.draw.line(screen, red, (ini_sx-1, ini_sy-(h+0.1-0.025)*scale_multiplier),
                         (ini_sx+s2*scale_multiplier, ini_sy-(h+0.1-0.025)*scale_multiplier), 2)
        if location == 'wall':
            pg.draw.line(screen, red, (ini_sx+(1+s2+0.1)*scale_multiplier,
                                       ini_sy+5-wall*scale_multiplier), (ini_sx+(1+s2+0.1)*scale_multiplier,
                                                                         ini_sy+5), 2)
            pg.draw.line(screen, red, (ini_sx+(1+s2+0.05)*scale_multiplier,
                                       ini_sy+5-wall*scale_multiplier), (ini_sx+(1+s2+0.125)*scale_multiplier,
                                                                         ini_sy+5-wall*scale_multiplier), 2)
            pg.draw.line(screen, red, (ini_sx+(1+s2+0.05)*scale_multiplier,
                                       ini_sy+5), (ini_sx+(1+s2+0.125)*scale_multiplier,
                                                   ini_sy+5), 2)
        # visual guidelines delay
        if location_cooldown == 1:
            location_time += 1
        else:
            location_time = 0

        if location_time >= 1000:
            location = ''

        return location, location_time, location_cooldown

    # get speed_multiplier functions------------------------------------------------------------------------
    def find_speed_multiplier(self, x_speed_switches):
        x_speed_switches = x_02.isPressed(
            x_speed_switches, [1, 0, 0, 0, 0])
        x_speed_switches = x_05.isPressed(
            x_speed_switches, [0, 1, 0, 0, 0])
        x_speed_switches = x_1.isPressed(
            x_speed_switches, [0, 0, 1, 0, 0])
        x_speed_switches = x_16.isPressed(
            x_speed_switches, [0, 0, 0, 1, 0])
        x_speed_switches = x_2.isPressed(
            x_speed_switches, [0, 0, 0, 0, 1])

        # speed button adjustment
        if x_speed_switches[0] == 1:  # x_02_switch
            pg.draw.rect(screen, ACTIVE, (x_02.x,
                                          x_02.y, x_02.w, x_02.h), 5)
            speed_multiplier = 0.2
        elif x_speed_switches[1] == 1:  # x_05_switch
            pg.draw.rect(screen, ACTIVE, (x_05.x,
                                          x_05.y, x_05.w, x_05.h), 5)
            speed_multiplier = 0.5
        elif x_speed_switches[2] == 1:  # x_1_switch
            pg.draw.rect(screen, ACTIVE, (x_1.x,
                                          x_1.y, x_1.w, x_1.h), 5)
            speed_multiplier = 1
        elif x_speed_switches[3] == 1:  # x_16_switch
            pg.draw.rect(screen, ACTIVE, (x_16.x,
                                          x_16.y, x_16.w, x_16.h), 5)
            speed_multiplier = 1.6
        elif x_speed_switches[4] == 1:  # x_2_switch
            pg.draw.rect(screen, ACTIVE, (x_2.x,
                                          x_2.y, x_2.w, x_2.h), 5)
            speed_multiplier = 2
        return speed_multiplier, x_speed_switches

    # update text function---------------------------------------------------------------------------------

    def update_textboxs(self):
        screen.blit(TextBox(black,
                    'Launch deg =        °', FONT_RB_25).txt_surface, (396, 561))
        screen.blit(TextBox(black,
                    'S1 =              (mm)', FONT_IMP_26).txt_surface, (19, 552))
        screen.blit(TextBox(orange,
                    'S1 =              (mm)', FONT_IMP_26).txt_surface, (18, 550))
        screen.blit(TextBox(black,
                    f'{input_box2.text}', FONT_IMP_26).txt_surface, (76, 554))
        screen.blit(TextBox(black,
                    'S2 =            (mm)', FONT_RB_25).txt_surface, (225, 561))
        screen.blit(TextBox(black,
                    'Wall Height =           (cm)', FONT_RB_25).txt_surface, (583, 561))
        screen.blit(TextBox(black,
                    '0.2', FONT_IMP_20).txt_surface, (985, 350))
        screen.blit(TextBox(black,
                    '0.5', FONT_IMP_20).txt_surface, (1025, 350))
        screen.blit(TextBox(black,
                    '1', FONT_IMP_20).txt_surface, (1073, 350))
        screen.blit(TextBox(black,
                    '1.5', FONT_IMP_20).txt_surface, (1106, 350))
        screen.blit(TextBox(black,
                    '2', FONT_IMP_20).txt_surface, (1152, 350))
        screen.blit(TextBox(black,
                    'i', FONT_IMP_20).txt_surface, (777, 7))
        screen.blit(TextBox(black,
                    '+', FONT_IMP_20).txt_surface, (1000, 301))
        screen.blit(TextBox(black,
                    '-', FONT_IMP_20).txt_surface, (953, 300))
        screen.blit(TextBox(dark_blue,
                    'INITIATE', FONT_IMP_20).txt_surface, (969, 474))
        screen.blit(TextBox(red,
                    'RESET', FONT_IMP_20).txt_surface, (978, 524))
        screen.blit(TextBox(black,
                    'Speed Multiplier : ', FONT_RB_25).txt_surface, (820, 355))
        screen.blit(TextBox(black,
                    'Scale :', FONT_RB_25).txt_surface, (820, 305))
        screen.blit(TextBox(black, f'{scale_multiplier}',
                    FONT_IMP_20).txt_surface, (885, 300))
        screen.blit(TextBox(black,
                    "Spring deformation = {x} m".format(x=str(x)[:5]), FONT_IMP_30).txt_surface, (822, 52))
        screen.blit(TextBox(orange,
                    "Spring deformation = {x} m".format(x=str(x)[:5]), FONT_IMP_30).txt_surface, (820, 50))
        screen.blit(TextBox(mystic_green,
                    "Initial Velocity = {u} m/s".format(u=str(u)[:5]), FONT_RB_25).txt_surface, (820, 125))
        screen.blit(TextBox(mystic_green,
                    "Height over wall while passing  = {H} m".format(H=str(H-wall)[:5]), FONT_RB_25).txt_surface, (820, 175))
        screen.blit(TextBox(mystic_green,
                    "Time required to reach the target  = {T} sec".format(T=str(time)[:4]), FONT_RB_25).txt_surface, (820, 225))
        screen.blit(TextBox(black,
                    "X displacement from start : {x_pos} m".format(x_pos=squash.curr_x_distance), FONT_RB_25).txt_surface, (20, 5))
        screen.blit(TextBox(black,
                    "Y displacement from ground : {y_pos} m".format(y_pos=squash.curr_y_distance), FONT_RB_25).txt_surface, (20, 30))
        if Auto_Manual_text_toggle:
            screen.blit(TextBox(mystic_green, 'Auto',
                        FONT_IMP_20).txt_surface, (1093, 300))
        if not Auto_Manual_text_toggle:
            screen.blit(TextBox(black, 'Manual',
                        FONT_IMP_20).txt_surface, (1080, 300))

    # toggle scale recommnedation

    def recommend_adjustment(self, toggle_recc, scale_multiplier):
        if toggle_recc == True:
            while (2+s2+s1)*scale_multiplier < 690:
                scale_multiplier += 1
                if (2+s2+s1)*scale_multiplier >= 690:
                    break
        if toggle_recc == True:
            while (2+s2+s1)*scale_multiplier > 700:
                scale_multiplier -= 1
                if (2+s2+s1)*scale_multiplier <= 700:
                    break
        # toggle_recc = 0
        return toggle_recc, scale_multiplier


# Class declaration
operation = Operation()

# logic#---------------------------------------------------------------------------------------------------#
scale_multiplier = 300  # to manually fit the screen
speed_multiplier = 1  # to manually control time as see fit
toggle_start = 0
toggle_reset = 0
toggle_recc = False
increase_mouse_trig = [False, False]
decrease_mouse_trig = [False, False]
Auto_Manual_text_toggle = False  # Manual
x_02_switch = 0
x_05_switch = 0
x_1_switch = 1
x_16_switch = 0
x_2_switch = 0
option_switch = False
location_cooldown = 0
location = ''
x_speed_switches = [x_02_switch, x_05_switch,
                    x_1_switch, x_16_switch, x_2_switch]
# Scientific variables#---------------------------------------------------------------------------------------------------#
M = 0.243  # net weight of ball and platform
k = 0.88  # spring constant
deg = 60  # degree
s1 = 0.303  # at target
s2 = 0  # at shooter
wall = 1  # wall's height
h = 0.433  # shooter's height
a = 9.81  # earth's gravitational acceleration

u, x, H, ux, uy, time = operation.calculate(s1, s2, h, deg, M, k)


ini_sx = 50  # initial floor position on X-axis
ini_sy = 530  # initial floor position on Y-axis
pos_x = ini_sx
pos_y = ini_sy-h*scale_multiplier  # initial ball position
pos_y_max = pos_y
curr_x_distance = 0
curr_y_distance = h
last_t = 0
location_time = 0
ct_G = 0
ct_B = 0
t = 0  # initial time
# Color code#---------------------------------------------------------------------------------------------------#
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 51, 51)
light_red = (255, 102, 102)
blue = (153, 153, 255)
light_blue = (153, 204, 255)
dark_blue = (0, 0, 153)
green = (51, 255, 51)
light_green = (180, 255, 180)
orange = (255, 128, 0)
light_orange = (255, 204, 153)
dark_orange = (204, 102, 0)
mystic_green = (29, 120, 116)
lavender = (153, 51, 255)
bg_color = (255, 255, 204)
bg_color_highlight = (255, 216, 124)
ACTIVE = (192, 192, 192)

pg.init()
pg.display.set_caption("G03_Simulation")
FONT_NONE = pg.font.SysFont(None, 32)
FONT_IMP_20 = pg.font.SysFont("impact", 20)
FONT_IMP_26 = pg.font.SysFont("impact", 26)
FONT_IMP_30 = pg.font.SysFont("impact", 30)
FONT_RB_25 = pg.font.SysFont('Raleway bold', 25)
FONT_RB_30 = pg.font.SysFont('Raleway bold', 30)
win_x = 1200
win_y = 600
screen = pg.display.set_mode((win_x, win_y))
running = True

# Hover
hover_info = Hover(780, 20, 12, black)

# Buttons
initiate = Button(900, 470, 200, 32, black)
Reset = Button(900, 520, 200, 32, red)
recommend = Button(1050, 298, 125, 32, black)
x_02 = Button(978, 348, 40, 32, black)
x_05 = Button(1018, 348, 40, 32, black)
x_1 = Button(1058, 348, 40, 32, black)
x_16 = Button(1098, 348, 40, 32, black)
x_2 = Button(1138, 348, 40, 32, black)
backspace = Button(360, 330, 20, 20, black)
Input_new = Button(500, 330, 20, 20, black)
increase = Button(990, 298, 32, 32, black)
decrease = Button(940, 298, 32, 32, black)

buttons = [x_02, x_05, x_1, x_16, x_2,
           initiate, Reset, recommend, hover_info, increase, decrease]

# Input boxes
input_box1 = InputBox(510, 556, 32, 25, '60', 'int',
                      2, 'degree', FONT_IMP_20, black)
input_box2 = InputBox(70, 552, 42, 32, '303', 'int',
                      3, 's1', FONT_IMP_26, orange)
input_box3 = InputBox(270, 556, 42, 25, '0', 'int',
                      3, 's2', FONT_IMP_20, black)
input_box4 = InputBox(700, 556, 42, 25, '100', 'int',
                      3, 'wall', FONT_IMP_20, black)
input_boxes = [input_box1, input_box2, input_box3, input_box4]

# Squash
squash = Ball(pos_x, pos_y, u, 0.02, black, curr_x_distance, curr_y_distance)

# Simulation
sim = Simulation(t, last_t, pos_y_max)
while (running):
    screen.fill((255, 255, 204))
    # alternative visual display
    location, ct_G, ct_B = operation.activate_ping(location, ct_G, ct_B)
    location, location_time, location_cooldown = operation.draw_field(
        location, location_time, location_cooldown)

    # inputtable variables
    deg = input_box1.inputbox_return(deg)
    s1 = input_box2.inputbox_return(s1, 1000)
    s2 = input_box3.inputbox_return(s2, 1000)
    wall = input_box4.inputbox_return(wall, 100)

    # Calculations
    u, x, H, ux, uy, time = operation.calculate(s1, s2, h, deg, M, k)

    # simulation init#
    sim.initiate_sim(toggle_start)

    # simulation reset#
    toggle_reset, toggle_start = sim.reset_sim(toggle_reset, toggle_start)

    # initiate button interaction
    for button in buttons:
        button.draw(screen)

    # Buttons#
    [toggle_start] = initiate.isPressed([toggle_start], [1])
    [toggle_reset] = Reset.isPressed([toggle_reset], [1])

    # recommend button
    toggle_recc, Auto_Manual_text_toggle = recommend.toggle_auto(
        toggle_recc, Auto_Manual_text_toggle)
    toggle_recc, scale_multiplier = operation.recommend_adjustment(
        toggle_recc, scale_multiplier)
    # scale buttons
    scale_multiplier, increase_mouse_trig = increase.isPressed_with_condition(
        scale_multiplier, 1, increase_mouse_trig, Auto_Manual_text_toggle)
    scale_multiplier, decrease_mouse_trig = decrease.isPressed_with_condition(
        scale_multiplier, -1, decrease_mouse_trig, Auto_Manual_text_toggle)

    # get speed_multiplier
    speed_multiplier, x_speed_switches = operation.find_speed_multiplier(
        x_speed_switches)
    # Textboxes
    operation.update_textboxs()

    # ทำการเรียก InputBox ทุกๆตัว โดยการ Loop เข้าไปยัง list ที่เราเก็บค่า InputBox ไว้
    location_cooldowns = []
    for box in input_boxes:
        location, location_cooldown = box.return_location(
            location, location_cooldown)
        location_cooldowns.append(location_cooldown)
        box.update()  # เรียกใช้ฟังก์ชัน update() ของ InputBox
        # เรียกใช้ฟังก์ชัน draw() ของ InputBox เพื่อทำการสร้างรูปบน Screen
        box.draw(screen)
    location_cooldown = min(location_cooldowns)
    # draw scale
    operation.draw_scale()
    # hover over other obejcts
    option_switch = hover_info.popup(
        350, 40, 440, 330, white, black, option_switch)

    pg.display.update()
    for event in pg.event.get():
        for box in input_boxes:
            box.handle_event(event)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_KP_MINUS:
                if toggle_start == 0:
                    scale_multiplier -= 10
                toggle_reset = 1
            elif event.key == pg.K_KP_PLUS:
                if toggle_start == 0:
                    scale_multiplier += 10
                toggle_reset = 1
        if event.type == pg.QUIT:
            pg.quit()
            exit()
'''pg.draw.circle(screen, black, (ini_sx-5+(0.015*scale_multiplier),
                   ini_sy-(h*scale_multiplier)), 0.03*scale_multiplier)'''