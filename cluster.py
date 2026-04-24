import ast
import json
from pathlib import Path

from dotenv import load_dotenv
import os

import numpy as np
import umap
from sklearn.neighbors import NearestNeighbors
from collections import Counter

load_dotenv()

key = os.getenv("OPENAI_API_KEY") #kept this for future use, if open ai needs to be used
print("Loaded key:", key[:7] + "..." if key else None)

BASE_DIR = Path(__file__).resolve().parent


# ---------------------------------------------
# STEP 1: Discover all graph files
# ---------------------------------------------
def get_all_files():
    return sorted(BASE_DIR.glob("*yo.py"))


# ---------------------------------------------
# STEP 2: Parse node_groups safely from each file
# ---------------------------------------------
def extract_node_groups_from_file(file_path):
    text = file_path.read_text(encoding="utf-8")
    tree = ast.parse(text)

    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "node_groups":
                    parsed = ast.literal_eval(node.value)

                    if isinstance(parsed, dict):
                        cleaned = {}
                        for k, v in parsed.items():
                            if isinstance(k, str) and isinstance(v, str):
                                cleaned[k] = v
                        return cleaned

    return {}


# ---------------------------------------------
# STEP 3: Build GLOBAL node -> domain map
# ---------------------------------------------
def build_global_node_group_map(files):
    node_group_map = {}

    for file in files:
        file_map = extract_node_groups_from_file(file)
        node_group_map.update(file_map)

    return node_group_map


# ---------------------------------------------
# STEP 4: Build GLOBAL node list
# ---------------------------------------------
def build_global_node_list(node_group_map):
    return sorted(node_group_map.keys())


# ---------------------------------------------
# STEP 5: Get embeddings
# ---------------------------------------------
def get_embeddings(nodes):
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer("all-MiniLM-L6-v2")
    vectors = model.encode(nodes, convert_to_numpy=True)

    return vectors


# ---------------------------------------------
# STEP 6: Convert embeddings -> 2D positions
# ---------------------------------------------
def reduce_to_2d(vectors):
    reducer = umap.UMAP(
        n_components=2,
        random_state=42,
        n_neighbors=5,
        min_dist=0.3
    )

    coords = reducer.fit_transform(vectors)
    return coords


# ---------------------------------------------
# STEP 7: Domain pastel colors
# ---------------------------------------------
def get_domain_colors():
    return {
        "core": "#B5EAD7",
        "clinical": "#FFD1DC",
        "family": "#AEC6CF",
        "school": "#FFDAC1",
        "access": "#CBAACB",
        "bias": "#F3E5AB",
        "environment": "#C7CEEA",
        "controversial": "#D5E1DF",
        "work": "#FFB7B2",
        "unknown": "#D3D3D3",
    }


# ---------------------------------------------
# STEP 8: Compute local neighborhood signal in 2D
# local_domain = dominant domain among neighbors
# confidence = fraction of neighbors matching manual domain
# ---------------------------------------------
def compute_local_domain_info(nodes, coords, node_group_map, k=5):
    if len(nodes) == 0:
        return [], []

    effective_k = min(k + 1, len(nodes))

    nbrs = NearestNeighbors(n_neighbors=effective_k)
    nbrs.fit(coords)

    _, indices = nbrs.kneighbors(coords)

    local_domains = []
    confidences = []

    for i, node in enumerate(nodes):
        manual_domain = node_group_map.get(node, "unknown")

        neighbor_indices = [idx for idx in indices[i] if idx != i]

        neighbor_domains = []
        for idx in neighbor_indices:
            neighbor_node = nodes[idx]
            neighbor_domain = node_group_map.get(neighbor_node, "unknown")
            if neighbor_domain != "unknown":
                neighbor_domains.append(neighbor_domain)

        if neighbor_domains:
            counts = Counter(neighbor_domains)
            local_domain = counts.most_common(1)[0][0]
            agreement_count = sum(1 for d in neighbor_domains if d == manual_domain)
            confidence = agreement_count / len(neighbor_domains)
        else:
            local_domain = manual_domain
            confidence = 0.0

        local_domains.append(local_domain)
        confidences.append(float(round(confidence, 3)))

    return local_domains, confidences


# ---------------------------------------------
# STEP 9: Scale positions + attach domain/color
# domain = manual/expert domain
# local_domain = neighborhood-based suggestion
# confidence = local agreement with manual domain
# ---------------------------------------------
def scale_positions(nodes, coords, node_group_map, local_domains, confidences):
    positions = {}

    x_vals = coords[:, 0]
    y_vals = coords[:, 1]

    x_vals = (x_vals - x_vals.min()) / (x_vals.max() - x_vals.min() + 1e-9)
    y_vals = (y_vals - y_vals.min()) / (y_vals.max() - y_vals.min() + 1e-9)

    domain_colors = get_domain_colors()

    for i, node in enumerate(nodes):
        domain = node_group_map.get(node, "unknown")
        local_domain = local_domains[i]

        positions[node] = {
            "x": float((x_vals[i] - 0.5) * 1200),
            "y": float((y_vals[i] - 0.5) * 1200),
            "domain": domain,
            "local_domain": local_domains[i],
            "confidence": confidences[i],
            "color": domain_colors.get(local_domain, "#D3D3D3")
        }

    # mild collision avoidance so very close nodes separate a bit
    min_dist = 50
    iterations = 3
    node_list = list(nodes)

    for _ in range(iterations):
        for i in range(len(node_list)):
            for j in range(i + 1, len(node_list)):
                n1 = node_list[i]
                n2 = node_list[j]

                dx = positions[n2]["x"] - positions[n1]["x"]
                dy = positions[n2]["y"] - positions[n1]["y"]
                dist = (dx**2 + dy**2) ** 0.5

                if dist < 1e-6:
                    dx, dy = 1.0, 1.0
                    dist = (dx**2 + dy**2) ** 0.5

                if dist < min_dist:
                    push = (min_dist - dist) / 2
                    ux = dx / dist
                    uy = dy / dist

                    positions[n1]["x"] -= ux * push
                    positions[n1]["y"] -= uy * push
                    positions[n2]["x"] += ux * push
                    positions[n2]["y"] += uy * push

    return positions


# ---------------------------------------------
# STEP 10: Save positions to JSON
# ---------------------------------------------
def save_positions(positions):
    output_path = BASE_DIR / "clusters.json"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(positions, f, indent=2)

    print(f"\n✅ Saved positions to {output_path}")


# ---------------------------------------------
# MAIN PIPELINE
# ---------------------------------------------
def main():
    print("\nScanning files...")
    files = get_all_files()
    print(f"Found {len(files)} files")

    print("\nBuilding node -> domain map...")
    node_group_map = build_global_node_group_map(files)
    print(f"Total labeled nodes: {len(node_group_map)}")

    print("\nBuilding global node list...")
    nodes = build_global_node_list(node_group_map)
    print(f"Total unique nodes: {len(nodes)}")

    print("\nGetting embeddings...")
    vectors = get_embeddings(nodes)

    print("\nReducing to 2D...")
    coords = reduce_to_2d(vectors)

    print("\nComputing local neighborhood info...")
    local_domains, confidences = compute_local_domain_info(
        nodes,
        coords,
        node_group_map,
        k=5
    )

    print("\nScaling positions...")
    positions = scale_positions(
        nodes,
        coords,
        node_group_map,
        local_domains,
        confidences
    )

    print("\nSaving positions...")
    save_positions(positions)

    print("\nDone!")


if __name__ == "__main__":
    main()