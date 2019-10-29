import pygame
pygame.joystick.init()
joystick = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
joystick = joystick[len(joystick)-1]
joystick.init()
print(joystick)
print(pygame.joystick.get_count())
print(joystick.get_name())


print(joystick.get_numaxes())
print(joystick.get_numbuttons())
print(joystick.get_numhats())

while True:
    """
    print(joystick.get_axis(1))
    """
    joystick.gethat(0)
    
    
    



