"""Touch keyboard."""

from lib.display.DISPLAY import *


class TouchKeyboard(object):
    """Touchscreen keyboard for ILI9341."""

    YELLOW = const(65504)
    GREEN = const(2016)

    KEYS = (
        (
            ('q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'),
            ('a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'),
            ('\t', 'z', 'x', 'c', 'v', 'b', 'n', 'm', '\b', '\b'),
            ('\n', ' ', '\r')
        ),
        (
            ('Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'),
            ('A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'),
            ('\t', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '\b', '\b'),
            ('\n', ' ', '\r')
        ),
        (
            ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0'),
            ('@', '#', '$', '%', '^', '&', '*', '(', ')'),
            ('\f', '+', ',', '.', '-', '_', '!', '?', '\b', '\b'),
            ('\a', ' ', '\r')
        ),
        (
            ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0'),
            ('<', '>', '|', '\\', '/', '{', '}', '[', ']'),
            ('\f', '=', '"', '\'', ';', ':', '`', '~', '\b', '\b'),
            ('\a', ' ', '\r')
        )
    )

    def __init__(self, font):
        """Initialize Keybaord.

        Args:
            display (Display class): LCD Display
            font (XglcdFont class): Font to display text above keyboard
        """
        self.font = font
        self.kb_screen = 0
        self.kb_text = ''
        self.load_keyboard()
        self.waiting = False
        self.locked = False

    def clear_text(self):
        """Clear the keyboard text."""
        getdisplay().fill_hrect(0, 11, getdisplay().width, self.font.height(), 0)
        self.kb_text = ''

    def set_text(self, text):
        self.kb_text = text
        getdisplay().fill_hrect(0, 11, getdisplay().width, self.font.height(), 0)
        getdisplay().set_pos(0, 11)
        getdisplay().write(self.kb_text)

    def handle_keypress(self, x, y, debug=False):
        """Get  pressed key.

        Args:
            x, y (int): Pressed screen coordinates.
        Returns:
            bool: True indicates return pressed otherwise False
        """
        if self.locked is True:
            return False

        if self.waiting is True:
            self.clear_text()
            self.waiting = False
            return False

        key = self.raw_keypress(x, y, debug)
        if key is not None:
            return self.handle_key(key)
        return False

    def raw_keypress(self, x, y, debug=False):

        x, y = y, x  # Touch coordinates need to be swapped.

        if debug:
            getdisplay().fill_circle(x, y, 5, self.GREEN)

        # Calculate keyboard row and column
        if y >= 47:  # Check if press within keyboard area
            row = int(y / 47) - 1
            if row == 0:
                column = int(x/32)
            elif row == 1 or row == 2:
                column = max(0, int((x-16)/32))
            else:
                # Row 3
                if x < 80:
                    column = 0
                elif x > 240:
                    column = 2
                else:
                    column = 1

            return self.KEYS[self.kb_screen][row][column]
        return None

    def handle_key(self, key):
        if key == '\t' or key == '\f':
            self.kb_screen ^= 1  # Toggle caps or flip symbol sets
            self.load_keyboard()
        elif key == '\a':
            self.kb_screen = 0  # Switch to alphabet screen
            self.load_keyboard()
        elif key == '\n':
            self.kb_screen = 2  # Switch to numeric / symbols screen
            self.load_keyboard()
        elif key == '\b':  # Backspace
            marginold = self.font.get_width(self.kb_text)
            self.kb_text = self.kb_text[:-1]
#                margin = self.font.measure_text(self.kb_text)
            margin = self.font.get_width(self.kb_text)
            
            getdisplay().fill_vrect(margin, 11, marginold - margin, self.font.height(), 0)
        elif key == '\r':
            # Keyboard return pressed (start search)
            #if self.kb_text != '':
            return True
        else:
            margin = self.font.get_width(self.kb_text)
            if margin < 300:
                #margin = self.font.measure_text(self.kb_text)
                self.kb_text += key
                getdisplay().set_pos(margin, 11)
                getdisplay().write(key)
        return False

    def load_keyboard(self):
        """Display the currently selected keyboard."""
        getdisplay().draw_image('images/kb{0}.raw'.format(self.kb_screen),
                                0, 47, 320, 192)

    def show_message(self, msg, color):
        """Display message above keyboard."""
        self.clear_text()
        msg_length = self.font.get_width(msg)
        #msg_length = self.font.measure_text(msg)
        display = getdisplay()
        margin = (display.width - msg_length) // 2
        display.set_pos(margin, 11)
        display.set_color(color, 0)
        display.write(msg)
