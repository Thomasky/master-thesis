from matplotlib.path import Path
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np


def plot_polygons(polys, inclusions):
    """ Plots a polygon with center (x,y)

    """
    ax = plt.subplot(111)

    for poly in polys:
        # Add first vertex at the end again
        verts = np.vstack((poly, poly[0, :]))

        # Configure polygon
        codes = [Path.LINETO] * (verts.shape[0] - 1)
        codes[0] = Path.MOVETO
        codes.append(Path.CLOSEPOLY)

        path = Path(verts, codes)
        patch = patches.PathPatch(path, facecolor='none', lw=2)
        ax.add_patch(patch)

    ax.plot(inclusions[:, 0], inclusions[:, 1],
            linestyle='none', marker='o', color='r')

    plt.title('Best Polygon')
#     plt.xlim(0, 1)
#     plt.ylim(0, 1)
    plt.gca().set_aspect('equal', adjustable='box')

#     var = np.zeros(np.size(scores, axis=1))
#     for i in range(0, np.size(scores, axis=1)):
#         var[i] = np.var(scores[:, i])
#
#     x1 = [2 ** i for i in range(0, np.size(scores, axis=1))]
#     conv = np.vstack((x1, var))

    # fig = plt.figure()


#     plt.subplot(212)
#     plt.loglog(conv[0], conv[1])
#     plt.title('Convergence')

    plt.show()


def plot_scores(scores):
    x = range(0, np.size(scores))
    plt.plot(x, scores[0])
    plt.title('Scores')
    plt.show()
