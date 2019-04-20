import gizeh
import moviepy.editor as mpy
import numpy as np
import matplotlib.pyplot as plt

# constants
w, h = 512, 512
duration = 10.0
pi = 3.141592
num_circles = 10
num_helicies = 2
stick_height = 300
stick_buffer = 100
max_ellipse_r = 50
min_ellipse_r = 20

def make_frame(t):
    surface = gizeh.Surface(w, h, bg_color=(1,1,1))
    rotation = 2*pi * t/duration
    # major axis for ellipse on which circle rotates
    a = (max_ellipse_r - min_ellipse_r) * np.sin(rotation) + min_ellipse_r
    b = (max_ellipse_r - min_ellipse_r) * np.cos(rotation) + min_ellipse_r
    circle_x = a * np.cos(rotation) + w/2
    circle_y = b * np.sin(rotation) + h/2
    circle = gizeh.circle(xy=(circle_x, circle_y),
                          r=10,
                          fill=(0,0,0),
                          stroke=(1,1,1),
                          stroke_width=5,
                          )
    center = gizeh.circle(xy=(w/2, h/2),
                          r=2,
                          fill=(0,0,0),
                          )
    rect = gizeh.rectangle(xy=(w/2, h/2),
                           lx=10,
                           ly=300,
                           angle=rotation,
                           fill=(0,0,0),
                           )
    # circle.draw(surface)
    rect.draw(surface)
    center.draw(surface)
    return surface.get_npimage()

clip = mpy.VideoClip(make_frame, duration=duration)
clip.write_gif('encircle.gif', fps=30)

