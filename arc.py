import gizeh
import moviepy.editor as mpy

# constants
w, h = 512, 512
duration = 2
pi = 3.141592

def make_frame(t):
    surface = gizeh.Surface(w, h)
    rotation = 2*pi * t/duration
    circle = gizeh.circle(xy=(w/2, h/2),
                          r=80,
                          fill=(0,0,0))
    arc = gizeh.arc(xy=(w/2, h/2),
                    r=100, 
                    a1=0 + rotation, 
                    a2=pi/2 + rotation, 
                    fill=(1,1,1),
                    # stroke=(1,1,1),
                    # stroke_width=5
                    )
    arc.draw(surface)
    circle.draw(surface)
    return surface.get_npimage()

clip = mpy.VideoClip(make_frame, duration=duration)
clip.write_gif('arc.gif', fps=30)

