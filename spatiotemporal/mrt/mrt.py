#!/usr/bin/env python3
# From https://github.com/stogiannidis/srbench
# Copyright Stogiannidis et al. 2025 arxiv.org/abs/2503.19707
# MIT licensed
import os
import random
import argparse
import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.gridspec import GridSpec

# Global dictionary of polycube shapes
SHAPES = {
    "Snake": [
        (0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1),
        (1, 2, 1), (2, 2, 1), (2, 2, 2), (2, 3, 2),
    ],
    "Zigzag": [
        (0, 0, 0), (1, 0, 0), (1, 1, 0), (2, 1, 0),
        (2, 1, 1), (2, 2, 1), (3, 2, 1), (3, 2, 2),
    ],
    "SnakeComplex1": [
        (0, 0, 0), (1, 0, 0), (2, 0, 0), (2, 1, 0),
        (2, 1, 1), (2, 2, 1), (1, 2, 1), (1, 3, 1), (1, 3, 2),
    ],
    "HookedCorner": [
        (0, 0, 0), (1, 0, 0), (2, 0, 0), (0, 1, 0),
        (0, 2, 0), (0, 2, 1), (0, 2, 2),
    ],
    "TopPlate": [
        (0, 0, 0), (0, 1, 0), (0, 2, 0),
        (0, 2, 1), (1, 2, 1), (2, 2, 1),
    ],
    "CornerStaircase": [
        (0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 1, 0),
        (1, 1, 0), (2, 1, 0), (3, 1, 0), (3, 2, 0), (3, 3, 0),
    ],
    "TripleArm": [
        (3, -1, 0), (3, -1, 1), (3, -1, 2), (0, 0, 0),
        (1, 0, 0), (2, 0, 0), (3, 0, 0), (0, 1, 0), (0, 2, 0),
    ],
}

# Shapes available for each difficulty
EASY_SHAPES = ["Snake", "HookedCorner", "TopPlate", "CornerStaircase", "TripleArm"]
COMPLEX_SHAPES = list(SHAPES.keys())

# Dynamic similar-object mapping
all_shape_keys = list(SHAPES.keys())
SIMILAR_MAPPING = {
    key: [s for s in all_shape_keys if s != key] for key in all_shape_keys
}


def set_axes_equal(ax, all_vertices):
    """Make the aspect ratio equal and remove visual distractions."""
    all_vertices = np.array(all_vertices)
    x_limits = [np.min(all_vertices[:, 0]), np.max(all_vertices[:, 0])]
    y_limits = [np.min(all_vertices[:, 1]), np.max(all_vertices[:, 1])]
    z_limits = [np.min(all_vertices[:, 2]), np.max(all_vertices[:, 2])]
    
    x_range = x_limits[1] - x_limits[0]
    y_range = y_limits[1] - y_limits[0]
    z_range = z_limits[1] - z_limits[0]
    max_range = max(x_range, y_range, z_range)
    
    x_mid = np.mean(x_limits)
    y_mid = np.mean(y_limits)
    z_mid = np.mean(z_limits)
    
    ax.set_xlim(x_mid - max_range / 2, x_mid + max_range / 2)
    ax.set_ylim(y_mid - max_range / 2, y_mid + max_range / 2)
    ax.set_zlim(z_mid - max_range / 2, z_mid + max_range / 2)
    ax.set_box_aspect([1, 1, 1])
    
    # Set ticks and remove labels
    ax.set_xticks(np.linspace(x_limits[0], x_limits[1], 5))
    ax.set_yticks(np.linspace(y_limits[0], y_limits[1], 5))
    ax.set_zticks(np.linspace(z_limits[0], z_limits[1], 5))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])
    
    # Remove 3D visual elements for complex mode
    if hasattr(ax, '_remove_3d_elements'):
        ax.xaxis.pane.set_visible(False)
        ax.yaxis.pane.set_visible(False)
        ax.zaxis.pane.set_visible(False)
        ax.grid(False)
        ax._axis3don = False


def cube_vertices(origin, size=1.0):
    """Return the 8 corner vertices of a cube."""
    x, y, z = origin
    return np.array([
        [x, y, z], [x + size, y, z], [x + size, y + size, z], [x, y + size, z],
        [x, y, z + size], [x + size, y, z + size], 
        [x + size, y + size, z + size], [x, y + size, z + size],
    ])


def plot_cubes(ax, vertices, title="", facecolor="white", hide_3d_elements=False):
    """Plot cubes using their vertices."""
    if hide_3d_elements:
        ax._remove_3d_elements = True
    
    n_cubes = len(vertices) // 8
    vertices_reshaped = vertices.reshape((n_cubes, 8, 3))
    
    for cube_verts in vertices_reshaped:
        faces = [
            [0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4],
            [2, 3, 7, 6], [1, 2, 6, 5], [0, 3, 7, 4],
        ]
        for face in faces:
            polygon = Poly3DCollection(
                [cube_verts[face]], facecolors=facecolor,
                edgecolors="black", alpha=1.0,
            )
            ax.add_collection3d(polygon)
    
    ax.set_title(title, fontsize=12)
    set_axes_equal(ax, vertices)


def generate_shape_vertices(shape_name, cube_size=1.0):
    """Generate vertices for a given shape."""
    if shape_name not in SHAPES:
        raise ValueError(f"Unknown shape {shape_name}")
    
    cube_origins = SHAPES[shape_name]
    all_vertices = []
    for origin in cube_origins:
        corners = cube_vertices(origin, size=cube_size)
        all_vertices.append(corners)
    return np.vstack(all_vertices)


def get_transformed_candidate(transformation_func, original, max_attempts=10):
    """Apply transformation until result differs from original."""
    for _ in range(max_attempts):
        candidate = transformation_func(original)
        if not np.allclose(candidate, original, atol=1e-6):
            return candidate
    return candidate


def transform_rotate(vertices, difficulty="easy"):
    """Rotate shape based on difficulty level."""
    center = vertices.mean(axis=0)
    shifted = vertices - center
    
    if difficulty == "easy":
        # Single axis rotation with simple angles
        axis = random.choice(["x", "y", "z"])
        angle = np.deg2rad(random.choice([-90, 90, 180]))
        
        if axis == "x":
            R = np.array([
                [1, 0, 0],
                [0, np.cos(angle), -np.sin(angle)],
                [0, np.sin(angle), np.cos(angle)],
            ])
        elif axis == "y":
            R = np.array([
                [np.cos(angle), 0, np.sin(angle)],
                [0, 1, 0],
                [-np.sin(angle), 0, np.cos(angle)],
            ])
        else:  # z axis
            R = np.array([
                [np.cos(angle), -np.sin(angle), 0],
                [np.sin(angle), np.cos(angle), 0],
                [0, 0, 1],
            ])
    else:  # complex
        # Multi-axis rotation with varied angles
        angle_x = np.deg2rad(np.random.choice([0, 60, 90, 120]))
        angle_y = np.deg2rad(np.random.choice([0, 60, 90, 120]))
        angle_z = np.deg2rad(np.random.choice([0, 60, 90, 120]))
        
        Rx = np.array([
            [1, 0, 0],
            [0, np.cos(angle_x), -np.sin(angle_x)],
            [0, np.sin(angle_x), np.cos(angle_x)],
        ])
        Ry = np.array([
            [np.cos(angle_y), 0, np.sin(angle_y)],
            [0, 1, 0],
            [-np.sin(angle_y), 0, np.cos(angle_y)],
        ])
        Rz = np.array([
            [np.cos(angle_z), -np.sin(angle_z), 0],
            [np.sin(angle_z), np.cos(angle_z), 0],
            [0, 0, 1],
        ])
        R = Rz @ Ry @ Rx
    
    rotated = (R @ shifted.T).T
    return rotated + center


def transform_mirror(vertices, difficulty="easy"):
    """Mirror shape based on difficulty level."""
    center = vertices.mean(axis=0)
    shifted = vertices - center
    mirrored = shifted.copy()
    
    if difficulty == "easy":
        # Mirror across XY plane (Z-axis)
        mirrored[:, 2] = -mirrored[:, 2]
    else:  # complex
        # Mirror across random axis
        axis = random.choice([0, 1, 2])
        mirrored[:, axis] = -mirrored[:, axis]
    
    return mirrored + center


def get_visually_similar_candidate(chosen_shape_name, original_vertices, cube_size=1.0, difficulty="easy"):
    """Get a similar shape candidate."""
    if chosen_shape_name in SIMILAR_MAPPING:
        similar_candidates = SIMILAR_MAPPING[chosen_shape_name][:]
        random.shuffle(similar_candidates)
        
        for similar_shape_name in similar_candidates:
            if similar_shape_name in SHAPES:
                candidate_vertices = generate_shape_vertices(similar_shape_name, cube_size)
                candidate_vertices = get_transformed_candidate(
                    lambda v: transform_rotate(v, difficulty), candidate_vertices
                )
                if (candidate_vertices.shape != original_vertices.shape or 
                    not np.allclose(candidate_vertices, original_vertices, atol=1e-6)):
                    return candidate_vertices
    return None


def generate_one_image(index, difficulty="easy", facecolor="white", outdir="data/mrt"):
    """Generate a single MRT image based on difficulty."""
    cube_size = 1.0
    
    # Select shapes based on difficulty
    shapes_list = EASY_SHAPES if difficulty == "easy" else COMPLEX_SHAPES
    shape_name = random.choice(shapes_list)
    original_vertices = generate_shape_vertices(shape_name, cube_size=cube_size)
    
    # Generate correct candidate (rotation)
    correct_candidate = get_transformed_candidate(
        lambda v: transform_rotate(v, difficulty), original_vertices
    )
    
    # Generate wrong candidates
    mirror_candidate = get_transformed_candidate(
        lambda v: transform_rotate(transform_mirror(v, difficulty), difficulty),
        original_vertices
    )
    
    similar_candidate = get_visually_similar_candidate(
        shape_name, original_vertices, cube_size, difficulty
    )
    if similar_candidate is None:
        similar_candidate = mirror_candidate
    
    # Set up candidates based on difficulty
    if difficulty == "easy":
        candidates = [
            ("rotate", correct_candidate),
            ("mirror", mirror_candidate),
            ("similar", similar_candidate),
        ]
        num_candidates = 3
        figure_size = (6, 6)
    else:  # complex
        mirror_candidate2 = get_transformed_candidate(
            lambda v: transform_rotate(transform_mirror(v, difficulty), difficulty),
            original_vertices
        )
        candidates = [
            ("rotate", correct_candidate),
            ("mirror", mirror_candidate),
            ("similar", similar_candidate),
            ("mirror2", mirror_candidate2),
        ]
        num_candidates = 4
        figure_size = (12, 8)
    
    random.shuffle(candidates)
    correct_candidate_index = [
        i for i, cand in enumerate(candidates) if cand[0] == "rotate"
    ][0]
    
    # Create figure
    fig = plt.figure(figsize=figure_size)
    gs = GridSpec(2, num_candidates, height_ratios=[0.5, 1], wspace=0.1, hspace=0.1)
    
    # Plot original shape
    ax_orig = fig.add_subplot(gs[0, :], projection="3d")
    plot_cubes(ax_orig, original_vertices, title="Original Shape", 
               facecolor=facecolor, hide_3d_elements=(difficulty == "complex"))
    
    # Plot candidates
    for i in range(num_candidates):
        ax = fig.add_subplot(gs[1, i], projection="3d")
        _, candidate_vertices = candidates[i]
        plot_cubes(ax, candidate_vertices, title=f"Option {chr(65 + i)}", 
                   facecolor=facecolor, hide_3d_elements=(difficulty == "complex"))
    
    # Save image
    filename = f"{shape_name}_{index}.png"
    output_path = os.path.join(outdir, filename)
    plt.savefig(output_path, dpi=120, bbox_inches="tight", pad_inches=0.1)
    plt.close(fig)
    
    # Save metadata
    metadata = {
        "filename": filename,
        "difficulty": difficulty,
        "shape": shape_name,
        "candidate_order": [tag for tag, _ in candidates],
        "answer": chr(65 + correct_candidate_index),
    }
    with open(os.path.join(outdir, "metadata.jsonl"), "a") as f:
        f.write(json.dumps(metadata) + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Generate mental rotation test images with variable difficulty."
    )
    parser.add_argument(
        "--difficulty", "-d", type=str, choices=["easy", "complex"], default="easy",
        help="Difficulty level: 'easy' (3 candidates, simple rotations) or 'complex' (4 candidates, complex transformations)"
    )
    parser.add_argument(
        "--num_images", "-n", type=int, default=1,
        help="Number of images to generate"
    )
    parser.add_argument(
        "--color", "-c", type=str, default="white",
        help="Color for the polycubes"
    )
    parser.add_argument(
        "--seed", "-s", type=int, default=69,
        help="Seed for reproducible results"
    )
    parser.add_argument(
        "--outdir", "-o", type=str, default=None,
        help="Output directory (defaults to data/mrt/{difficulty})"
    )
    
    args = parser.parse_args()
    
    # Set default output directory based on difficulty
    if args.outdir is None:
        args.outdir = f"data/mrt/{args.difficulty}"
    
    os.makedirs(args.outdir, exist_ok=True)
    
    # Set seed for reproducibility
    if args.seed is not None:
        random.seed(args.seed)
        np.random.seed(args.seed)
    
    # Generate images
    for i in range(args.num_images):
        generate_one_image(i, difficulty=args.difficulty, 
                          facecolor=args.color, outdir=args.outdir)
    
    print(f"Generated {args.num_images} {args.difficulty} MRT images in {args.outdir}")


if __name__ == "__main__":
    main()
