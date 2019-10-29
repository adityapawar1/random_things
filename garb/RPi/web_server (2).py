import pygame
import RPi.GPIO
import motor_functions as mf

# Define some colors.
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')
motor1 = mf.MiniCIMMotor(4)
motor2 = mf.MiniCIMMotor(17, inverse=True)
# motor3 = mf.MiniCIMMotor(27)

motors = [motor1, motor2]

# vexmotor = mf.VexMotor(4)
# vexmotor.toggle()
# vexmotor.test()
deadzone = 0.1

# This is a simple class that will help us print to the screen.
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint(object):
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def tprint(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, (self.x, self.y))
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10


pygame.init()

# Set the width and height of the screen (width, height).
screen = pygame.display.set_mode((500, 700))

pygame.display.set_caption("My Game")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates.
clock = pygame.time.Clock()

# Initialize the joysticks.
pygame.joystick.init()

# Get ready to print.
textPrint = TextPrint()

# -------- Main Program Loop -----------
while not done:
    output = open('power.txt', 'w+')
    for m in motors:
        m.run()
    # vexmotor.run()
    #
    # EVENT PROCESSING STEP
    #
    # Possible joystick actions: JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN,
    # JOYBUTTONUP, JOYHATMOTION
    for event in pygame.event.get(): # User did something.
        if event.type == pygame.QUIT: # If user clicked close.
            done = True # Flag that we are done so we exit this loop.
        elif event.type == pygame.JOYBUTTONDOWN:
            pass
        elif event.type == pygame.JOYBUTTONUP:
            pass
    # DRAWING STEP
    #
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    textPrint.reset()

    # Get count of joysticks.
    joystick_count = pygame.joystick.get_count()

    textPrint.tprint(screen, "Number of joysticks: {}".format(joystick_count))
    textPrint.indent()

    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        textPrint.tprint(screen, "Joystick {}".format(i))
        textPrint.indent()

        # Get the name from the OS for the controller/joystick.
        name = joystick.get_name()
        textPrint.tprint(screen, "Joystick name: {}".format(name))

        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        textPrint.tprint(screen, "Number of axes: {}".format(axes))
        textPrint.indent()
        
        axis3 = joystick.get_axis(3)

        if abs(axis3) >= deadzone:
            if axis3 < 0:
                for motor in motors:
                    motor.forward(abs(int(round(axis3 * 7 + 1))))
                    motor.backward(-1)
                    power = abs(int(round(axis3 * 7 + 1)))
                output.write("Motor Power (0-8): {} counter clockwise".format(abs(int(round(axis3 * 7 + 1)))))
                textPrint.tprint(screen, "Motor Power (0-8): {} counter clockwise".format(abs(int(round(axis3 * 7 + 1)))))
                
                
            elif axis3 > 0:
                for motor in motors:
                    motor.backward(abs(int(round(axis3 * 7 + 1))))
                    motor.forward(-1)
                    abs(int(round(axis3 * 7 + 1)))
                output.write("Motor Power (0-8): {} clockwise".format(abs(int(round(axis3 * 7 + 1)))))
                textPrint.tprint(screen, "Motor Power (0-8): {} clockwise".format(abs(int(round(axis3 * 7 + 1)))))
                
        else:
            output.write("Motor Power (0-8): Off")
            textPrint.tprint(screen, "Motor Power (0-8): Off")
            for motor in motors:
                motor.off()
        
        for i in range(axes-2):
            axis = joystick.get_axis(i)
            textPrint.tprint(screen, "Axis {} value: {:>6.3f}".format(i, axis))
                
        textPrint.unindent()

        buttons = joystick.get_numbuttons()
        textPrint.tprint(screen, "Number of buttons: {}".format(buttons))
        textPrint.indent()
        
        intake_toggle = joystick.get_button(6)
        """
        if intake_toggle == 1:
            vexmotor.toggle()
        print(vexmotor.on)
        """
        
        buttons_down = 0
        for i in range(buttons):
            button = joystick.get_button(i)
            if button == 1:
                buttons_down += 1
            textPrint.tprint(screen,
                             "Button {:>2} value: {}".format(i, button))
        textPrint.unindent()
        if buttons_down >= 2:
            done = True
        hats = joystick.get_numhats()
        textPrint.tprint(screen, "Number of hats: {}".format(hats))
        textPrint.indent()

        # Hat position. All or nothing for direction, not a float like
        # get_axis(). Position is a tuple of int values (x, y).
        for i in range(hats):
            hat = joystick.get_hat(i)
            textPrint.tprint(screen, "Hat {} value: {}".format(i, str(hat)))
        textPrint.unindent()

        textPrint.unindent()
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    #

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second.
    clock.tick(20)
    

# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE. app.run(debug=True, port=80, host='0.0.0.0')

for motor in motors:
    motor.close()
    
pygame.quit()


