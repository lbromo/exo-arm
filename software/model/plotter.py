import socket, sys
import matplotlib
matplotlib.use('GTKAgg')
import matplotlib.pyplot as plt
import numpy as np

sys.path.append('mechanics')
import params
## Plot wtuff we dont care about
fig, ax = plt.subplots(1, 1)
ax.set_aspect('equal')
ax.set_xlim(-0.35, 0.35)
ax.set_ylim(-0.35, 0.35)
ax.hold(True)

plt.ion()
plt.draw()
plt.show(False)

lines, = ax.plot([0,
                 params.l1 * np.sin(0),
                 params.l1 * np.sin(0) + params.l2 * np.sin(0)],
                [0,
                 params.l1 * -np.cos(0),
                 params.l1 * -np.cos(0) - params.l2 * np.cos(0)],
                'o-', lw=2)

background = fig.canvas.copy_from_bbox(ax.bbox)

fig.canvas.draw()
ax.figure.canvas.draw()

UDP_IP = "127.0.0.1"
UDP_PORT = 7331

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

while True:
   data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
   x = [float(val) for val in data.split(',')]
   # in function
   lines.set_data([0,
                   params.l1 * np.sin(x[0]),
                   params.l1 * np.sin(x[0]) + params.l2 * np.sin(x[1])],
                  [0,
                   params.l1 * -np.cos(x[0]),
                   params.l1 * -np.cos(x[0]) - params.l2 * np.cos(x[1])])
   
   fig.canvas.restore_region(background)
   ax.draw_artist(lines)
   fig.canvas.blit(ax.bbox)

