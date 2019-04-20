import gizeh
import moviepy.editor as mpy
import numpy as np
import matplotlib.pyplot as plt

def sq_arc(xy, r, a1, a2, **kw):
    # https://people.mozilla.org/~jmuizelaar/Riskus354.pdf
    # see Figure 4
    k = 0.5522847498
    theta = (a2 - a1) / 2
    p0 = gizeh.polar2cart(r, a1)
    p3 = gizeh.polar2cart(r, a2)
    p1 = (p0[0] + k*r*np.sin(theta), 
          p0[1] - k*r*np.cos(theta))
    p2 = (p3[0] + k*r*np.sin(theta), 
          p3[1] + k*r*np.cos(theta))
    ps = [(p[0] + xy[0], p[1] + xy[1]) for p in (p0, p1, p2, p3)]
    return gizeh.bezier_curve(ps, line_cap='square', **kw)

# constants
w, h = 512, 512
duration = 2.0
pi = 3.141592

def make_frame(t):
    surface = gizeh.Surface(w, h, bg_color=(1,1,1))
    arc = gizeh.arc(xy=(w/2, h/2),
                    r=100,
                    a1=0,
                    a2=pi/2,
                    fill=(0,0,0),
                    )
    sqarc = sq_arc(xy=(w/2, h/2),
                   r=50, 
                   a1=3*pi/4, 
                   a2=2*pi, 
                   stroke=(0,0,0),
                   stroke_width=5,
                   )
    arc.draw(surface)
    sqarc.draw(surface)
    return surface.get_npimage()

clip = mpy.VideoClip(make_frame, duration=duration)
clip.write_gif('arzeda.gif', fps=30)

