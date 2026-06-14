import numpy as np

z = np.zeros((400,400))

print(z)

# specify circle parameters: centre ij and radius
ci,cj=232,145
cr=20

# Create index arrays to z
I,J=np.meshgrid(np.arange(z.shape[0]),np.arange(z.shape[1]))

# calculate distance of all points to centre
dist=np.sqrt((I-ci)**2+(J-cj)**2)

print(dist)

# Assign value of 1 to those points where dist<cr:
z[np.where(dist<cr)]=1

# show result in a simple plot
fig=plt.figure()
ax=fig.add_subplot(111)
ax.pcolormesh(z)
ax.set_aspect('equal')