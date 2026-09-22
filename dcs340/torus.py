import matplotlib.pyplot as plt
import numpy as np


def main():
    major_radius = 2.0
    minor_radius = 0.75

    u = np.linspace(0, 2 * np.pi, 120)
    v = np.linspace(0, 2 * np.pi, 60)
    u, v = np.meshgrid(u, v)

    x = (major_radius + minor_radius * np.cos(v)) * np.cos(u)
    y = (major_radius + minor_radius * np.cos(v)) * np.sin(u)
    z = minor_radius * np.sin(v)

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot_surface(
        x,
        y,
        z,
        cmap="viridis",
        edgecolor="none",
        antialiased=True,
    )
    ax.set_title("Torus")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_box_aspect((1, 1, 0.6))
    ax.view_init(elev=30, azim=45)

    plt.tight_layout()
    fig.savefig("torus.png", dpi=150)
    plt.show()


if __name__ == "__main__":
    main()
