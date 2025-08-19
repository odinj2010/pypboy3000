# pypboy/modules/gpio/control_panel.py

import pygame
import config
import pypboy

# --- MODIFICATION: Import gpiozero for interactivity ---
try:
    from gpiozero import Device, LED, Button, PWMLED
    from gpiozero.pins.lgpio import LGPIOFactory
    Device.pin_factory = LGPIOFactory()
    GPIO_AVAILABLE = True
except Exception as e:
    print(f"GPIOZERO library not found or failed to load: {e}")
    GPIO_AVAILABLE = False


# Define pin types and their colors for the display
PIN_COLORS = {
    "5V": (200, 0, 0),
    "3.3V": (255, 128, 0),
    "GND": (50, 50, 50),
    "GPIO": (0, 150, 0),
    "I2C": (0, 0, 200),
    "SPI": (200, 0, 200),
    "UART": (0, 150, 150),
    "ID": (100, 100, 0),
    "PWM": (255, 105, 180) # Pink for PWM
}

# --- MODIFICATION: Added PWM flag to pin definitions ---
# Define the 40-pin header layout for Raspberry Pi 5
PIN_DEFINITIONS = {
    1: ("3.3V", "3.3V", None, False), 2: ("5V", "5V", None, False),
    3: ("GPIO 2", "I2C", 2, False), 4: ("5V", "5V", None, False),
    5: ("GPIO 3", "I2C", 3, False), 6: ("GND", "GND", None, False),
    7: ("GPIO 4", "GPIO", 4, False), 8: ("GPIO 14", "UART", 14, False),
    9: ("GND", "GND", None, False), 10: ("GPIO 15", "UART", 15, False),
    11: ("GPIO 17", "GPIO", 17, False), 12: ("GPIO 18", "PWM", 18, True),
    13: ("GPIO 27", "GPIO", 27, False), 14: ("GND", "GND", None, False),
    15: ("GPIO 22", "GPIO", 22, False), 16: ("GPIO 23", "GPIO", 23, False),
    17: ("3.3V", "3.3V", None, False), 18: ("GPIO 24", "GPIO", 24, False),
    19: ("GPIO 10", "SPI", 10, False), 20: ("GND", "GND", None, False),
    21: ("GPIO 9", "SPI", 9, False), 22: ("GPIO 25", "GPIO", 25, False),
    23: ("GPIO 11", "SPI", 11, False), 24: ("GPIO 8", "SPI", 8, False),
    25: ("GND", "GND", None, False), 26: ("GPIO 7", "SPI", 7, False),
    27: ("ID_SD", "ID", 0, False), 28: ("ID_SC", "ID", 1, False),
    29: ("GPIO 5", "GPIO", 5, False), 30: ("GND", "GND", None, False),
    31: ("GPIO 6", "GPIO", 6, False), 32: ("GPIO 12", "PWM", 12, True),
    33: ("GPIO 13", "PWM", 13, True), 34: ("GND", "GND", None, False),
    35: ("GPIO 19", "PWM", 19, True), 36: ("GPIO 16", "GPIO", 16, False),
    37: ("GPIO 26", "GPIO", 26, False), 38: ("GPIO 20", "GPIO", 20, False),
    39: ("GND", "GND", None, False), 40: ("GPIO 21", "GPIO", 21, False),
}

# --- NEW CLASS: PWM Control Slider ---
class PinPWMControl:
    def __init__(self, parent, bcm_pin, device, pos):
        self.parent = parent
        self.bcm_pin = bcm_pin
        self.device = device
        self.font = config.FONT_MED
        self.width = 400
        self.height = 120
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect(topleft=pos)
        
        # Slider properties
        self.slider_rect = pygame.Rect(20, 60, self.width - 40, 20)
        self.knob_rect = pygame.Rect(0, 0, 20, 40)
        self.knob_rect.centery = self.slider_rect.centery
        self.update_knob_pos()
        
        self.dragging = False
        self.draw()

    def update_knob_pos(self):
        self.knob_rect.centerx = self.slider_rect.x + self.device.value * self.slider_rect.width

    def draw(self):
        self.surface.fill((10, 20, 10))
        pygame.draw.rect(self.surface, config.TINTCOLOUR, self.surface.get_rect(), 1)
        
        # Title
        title_text = f"PWM Control: BCM {self.bcm_pin}"
        title_render = self.font.render(title_text, True, config.TINTCOLOUR)
        self.surface.blit(title_render, (10, 10))

        # Duty Cycle %
        duty_text = f"{int(self.device.value * 100)}%"
        duty_render = self.font.render(duty_text, True, config.TINTCOLOUR)
        self.surface.blit(duty_render, (self.width - duty_render.get_width() - 10, 10))

        # Slider bar and knob
        pygame.draw.rect(self.surface, (50, 50, 50), self.slider_rect)
        pygame.draw.rect(self.surface, config.TINTCOLOUR, self.knob_rect)

    def handle_event(self, event, parent_pos):
        local_pos = (event.pos[0] - self.rect.left - parent_pos[0], event.pos[1] - self.rect.top - parent_pos[1])
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.knob_rect.collidepoint(local_pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.knob_rect.centerx = max(self.slider_rect.left, min(local_pos[0], self.slider_rect.right))
            self.device.value = (self.knob_rect.centerx - self.slider_rect.x) / self.slider_rect.width
            self.draw()

class PinMenu:
    def __init__(self, parent, pin_number, bcm_pin, is_pwm, pos):
        self.parent = parent
        self.pin_number = pin_number
        self.bcm_pin = bcm_pin
        self.font = config.FONT_MED
        self.options = ["Set as OUTPUT", "Set as INPUT"]
        if is_pwm:
            self.options.append("Set as PWM")
        self.options.append("Release Pin")
        
        self.rects = []
        self.width = 300
        self.height = len(self.options) * 40 + 10
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((10, 20, 10))
        pygame.draw.rect(self.surface, config.TINTCOLOUR, self.surface.get_rect(), 1)

        for i, option in enumerate(self.options):
            text = self.font.render(option, True, config.TINTCOLOUR)
            rect = pygame.Rect(5, 5 + i * 40, self.width - 10, 40)
            self.surface.blit(text, (rect.x + 10, rect.y + 5))
            self.rects.append(rect)
        
        self.rect = self.surface.get_rect(topleft=pos)

    def handle_click(self, pos):
        local_pos = (pos[0] - self.rect.left, pos[1] - self.rect.top)
        for i, rect in enumerate(self.rects):
            if rect.collidepoint(local_pos):
                self.parent.set_pin_mode(self.bcm_pin, self.options[i].split()[-1])
                return True
        return False

class Module(pypboy.SubModule):
    
    label = "CONTROL PANEL" # <--- ADD THIS LINE

    def __init__(self, *args, **kwargs):
        super(Module, self).__init__(*args, **kwargs)
        
        self.active_pins = {}
        self.pin_rects = {}
        self.active_menu = None
        self.active_pwm_control = None
        
        self.image = pygame.Surface((config.WIDTH, config.HEIGHT - 80))
        self.redraw_display()

    def redraw_display(self):
        self.image.fill((0, 0, 0))
        title_text = "GPIO CONTROL PANEL"
        title_render = config.FONT_LRG.render(title_text, True, config.TINTCOLOUR)
        title_pos = ((self.image.get_width() - title_render.get_width()) // 2, 20)
        self.image.blit(title_render, title_pos)
        
        pin_box_width = 400
        pin_box_height = 40
        start_x_left = (config.WIDTH / 2) - pin_box_width - 50
        start_x_right = (config.WIDTH / 2) + 50
        start_y = 100
        y_spacing = 45

        for i in range(1, 41):
            pin_name, pin_type, bcm_pin, is_pwm = PIN_DEFINITIONS[i]
            color = PIN_COLORS.get(pin_type, (100, 100, 100))
            
            row = (i - 1) // 2
            x = start_x_left if (i % 2 != 0) else start_x_right
            y = start_y + (row * y_spacing)
            
            rect = pygame.Rect(x, y, pin_box_width, pin_box_height)
            self.pin_rects[i] = rect
            pygame.draw.rect(self.image, color, rect, 2)
            
            pin_num_text = f"{i:02d}"
            pin_num_render = config.FONT_MED.render(pin_num_text, True, config.TINTCOLOUR)
            self.image.blit(pin_num_render, (x + 10, y + 8))
            
            pin_name_render = config.FONT_MED.render(pin_name, True, config.TINTCOLOUR)
            self.image.blit(pin_name_render, (x + 80, y + 8))
            
            status_text = "[UNUSED]"
            status_color = (128, 128, 128)
            if bcm_pin in self.active_pins:
                device = self.active_pins[bcm_pin]
                if isinstance(device, PWMLED):
                    status_text = f"[PWM - {int(device.value * 100)}%]"
                    status_color = PIN_COLORS["PWM"]
                elif isinstance(device, LED):
                    state = "HIGH" if device.is_lit else "LOW"
                    status_text = f"[OUTPUT - {state}]"
                    status_color = (255, 255, 100) if device.is_lit else (180, 180, 80)
                elif isinstance(device, Button):
                    state = "HIGH" if device.is_pressed else "LOW"
                    status_text = f"[INPUT - {state}]"
                    status_color = (100, 255, 255) if device.is_pressed else (80, 180, 180)

            status_render = config.FONT_MED.render(status_text, True, status_color)
            status_pos_x = x + pin_box_width - status_render.get_width() - 10
            self.image.blit(status_render, (status_pos_x, y + 8))

    def set_pin_mode(self, bcm_pin, mode):
        if bcm_pin in self.active_pins:
            self.active_pins[bcm_pin].close()
            del self.active_pins[bcm_pin]

        if GPIO_AVAILABLE:
            if mode == "OUTPUT":
                self.active_pins[bcm_pin] = LED(bcm_pin)
            elif mode == "INPUT":
                self.active_pins[bcm_pin] = Button(bcm_pin)
            elif mode == "PWM":
                self.active_pins[bcm_pin] = PWMLED(bcm_pin)
        
        self.active_menu = None
        self.redraw_display()

    def handle_event(self, event):
        if self.active_pwm_control:
            self.active_pwm_control.handle_event(event, self.rect.topleft)
            return

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_pos = (event.pos[0] - self.rect.left, event.pos[1] - self.rect.top)
            
            if self.active_menu:
                if self.active_menu.rect.collidepoint(mouse_pos):
                    if self.active_menu.handle_click(mouse_pos): return
                self.active_menu = None
                self.redraw_display()
                return

            for pin_num, rect in self.pin_rects.items():
                if rect.collidepoint(mouse_pos):
                    pin_name, pin_type, bcm_pin, is_pwm = PIN_DEFINITIONS[pin_num]
                    
                    if bcm_pin in self.active_pins:
                        device = self.active_pins[bcm_pin]
                        if isinstance(device, LED) and not isinstance(device, PWMLED):
                            device.toggle()
                        elif isinstance(device, PWMLED):
                            self.active_pwm_control = PinPWMControl(self, bcm_pin, device, rect.topright)
                    elif pin_type not in ["5V", "3.3V", "GND", "ID"]:
                        self.active_menu = PinMenu(self, pin_num, bcm_pin, is_pwm, rect.topright)
                    break
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self.active_pwm_control:
                self.active_pwm_control = None

    def update(self, *args, **kwargs):
        self.redraw_display()
        super(Module, self).update(*args, **kwargs)

    def render(self, *args, **kwargs):
        if self.active_menu:
            self.image.blit(self.active_menu.surface, self.active_menu.rect)
        if self.active_pwm_control:
            self.image.blit(self.active_pwm_control.surface, self.active_pwm_control.rect)
        super(Module, self).render(*args, **kwargs)

    def handle_resume(self):
        self.parent.pypboy.header.headline = "GPIO"
        self.parent.pypboy.header.title = ["RASPBERRY PI 5 HEADER"]
        self.active_menu = None
        self.active_pwm_control = None
        self.redraw_display()
        super(Module, self).handle_resume()

    def handle_pause(self):
        for pin in self.active_pins.values():
            pin.close()
        self.active_pins.clear()
        super(Module, self).handle_pause()