import cv2
import matplotlib
import numpy as np
from matplotlib import pyplot as plt


def skew(x):
    return np.array([[0, -x[2], x[1]], [x[2], 0, -x[0]], [-x[1], x[0], 0]])


def two_view_geometry(intr1, extr1, intr2, extr2):
    relative_pose = extr2.dot(np.linalg.inv(extr1))
    R = relative_pose[:3, :3]
    T = relative_pose[:3, 3]
    tx = skew(T)
    E = np.dot(tx, R)
    F = np.linalg.inv(intr2[:3, :3]).T.dot(E).dot(np.linalg.inv(intr1[:3, :3]))
    return E, F, relative_pose


def draw_points_lines(img1, pts1, img2, lines2, colors):
    h, w = img2.shape[:2]
    for p, l, c in zip(pts1, lines2, colors):
        c = tuple(c.tolist())
        img1 = cv2.circle(img1, tuple(p), 5, c, -1)

        x0, y0 = map(int, [0, -l[2] / l[1]])
        x1, y1 = map(int, [w, -(l[2] + l[0] * w) / l[1]])
        img2 = cv2.line(img2, (x0, y0), (x1, y1), c, 1, lineType=cv2.LINE_AA)
    return img1, img2


def inspect_epipolor_geometry(img1, intr1, extr1, img2, intr2, extr2):
    """
    Terminology convention
        extr: world2camera
        intr: camera2pixel
        pose: camera2world
    """

    E, F, relative_pose = two_view_geometry(intr1, extr1, intr2, extr2)

    orb = cv2.ORB_create()
    kp1 = orb.detect(cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY), None)[:20]
    pts1 = np.array([[int(kp.pt[0]), int(kp.pt[1])] for kp in kp1])

    lines2 = cv2.computeCorrespondEpilines(pts1.reshape(-1, 1, 2), 1, F)
    lines2 = lines2.reshape(-1, 3)

    colors = np.random.randint(0, high=255, size=(len(pts1), 3))

    img1, img2 = draw_points_lines(img1, pts1, img2, lines2, colors)

    im_to_show = np.concatenate((img1, img2), axis=1)
    return im_to_show


def interactive_inspect_epipolar_geometry(img1, intr1, extr1, img2, intr2, extr2):
    # otherwise, mouse event does not work on macOS
    matplotlib.use("TkAgg")

    E, F, relative_pose = two_view_geometry(intr1, extr1, intr2, extr2)

    img1_h, img1_w = img1.shape[:2]
    img2_h, img2_w = img2.shape[:2]

    im_to_show = np.concatenate((img1, img2), axis=1)
    h, w = im_to_show.shape[:2]

    # note this resize
    fig = plt.figure(figsize=(8 * w / h, 8))

    def onclick(event):
        print("button=%d, x=%d, y=%d, xdata=%f, ydata=%f" % (event.button, event.x, event.y, event.xdata, event.ydata))
        color = np.random.random(size=(1, 3))
        plt.scatter(event.xdata, event.ydata, c=color, s=10)

        pts1 = np.array([[int(event.xdata), int(event.ydata)]])
        lines2 = cv2.computeCorrespondEpilines(pts1.reshape(-1, 1, 2), 1, F)
        lines2 = lines2.reshape(-1, 3)
        for line in lines2:
            x1, y1 = [img1_w, -line[2] / line[1]]
            x2, y2 = [img1_w + img2_w, -(line[2] + line[0] * img2_w) / line[1]]
            plt.plot([x1, x2], [y1, y2], c=color, linestyle="-", linewidth=1)
        fig.canvas.draw()

    cid = fig.canvas.mpl_connect("button_press_event", onclick)  # noqa
    plt.imshow(cv2.cvtColor(im_to_show, cv2.COLOR_BGR2RGB))
    plt.xlim((0, w))
    plt.ylim((h, 0))
    plt.tight_layout()
    plt.axis("off")
    plt.show()
