import gizeh
import moviepy.editor as mpy
import numpy as np
import matplotlib.pyplot as plt

# constants
w, h = 512, 512
duration = 100.0
pi = 3.141592
# major axis for ellipse on which circle rotates
a = 50
b = 20
num_circles = 21
num_helicies = 6
stick_height = 300
stick_buffer = 100

def make_frame(t):
    surface = gizeh.Surface(w, h, bg_color=(1,1,1))
    circle_ids = range(num_circles)
    circles_to_draw = [[[], []] for i in circle_ids]
    for j in range(num_helicies):
        for i in circle_ids:
            y_factor = (i - np.median(circle_ids)) * stick_height / num_circles
            if i % 2 == 0:
                opposite = 1
            else:
                opposite = 1
            start_position = (i * 2*pi/num_circles) + j * 2*pi/num_helicies
            rotation = opposite * 2*pi * t/duration * (i+1)
            absolute_rotation = rotation + start_position
            # factor defining how large the ellipse of circle rotation is
            rot_r_factor = 4 * np.sqrt(1 - (abs(y_factor)/(stick_height/2))**2)
            # rot_r_factor = 4 * (1 - abs(y_factor)/(stick_height/2))
            circle_x = rot_r_factor * a * np.cos(absolute_rotation) + w/2
            circle_y = rot_r_factor * b * np.sin(absolute_rotation) + h/2 + y_factor
            #color = (0,1*(j+1)/num_helicies,0)
            colormap = plt.get_cmap('plasma')
            color = colormap(j / num_helicies)
            periodic_t = t/duration if t/duration < 0.5 else 1 - t/duration
            # if j == 0:
            #     color = (1 * np.sin(periodic_t * pi), 0, 1 * np.cos(periodic_t * pi))
            # elif j == 1:
            #     color = (0, 1 * np.cos(periodic_t * pi), 1 * np.sin(periodic_t * pi))
            circle = gizeh.circle(xy=(circle_x, circle_y),
                                  r=10, 
                                  fill=color,
                                  #stroke=(1,1,1),
                                  #stroke_width=5,
                                  )
            # index of 0 on innermost list means to draw the circle before the rectangle
            # 1 means after
            if (rotation + start_position) % (2 * pi) > pi:
                # circle.draw(surface)
                circles_to_draw[i][0].insert(0, circle)
            else:
                circles_to_draw[i][1].append(circle)
    rec = gizeh.rectangle(xy=(w/2, h/2),
                          lx=10,
                          ly=stick_height + stick_buffer,
                          fill=(0,0,0),
                          )
    for i in reversed(circles_to_draw):
        for circle in i[0]:
            circle.draw(surface)
    rec.draw(surface)
    for i in reversed(circles_to_draw):
        for circle in i[1]:
            circle.draw(surface)
    # for circle in circles_to_draw:
    #     circle.draw(surface)
    return surface.get_npimage()

clip = mpy.VideoClip(make_frame, duration=duration)
clip.write_gif('encircle.gif', fps=30)

