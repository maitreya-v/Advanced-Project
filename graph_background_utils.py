# graph_background_utils.py

import os
import webbrowser
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def soft_weight(conf):
    if conf >= 0.8:
        return 1.00
    if conf >= 0.6:
        return 0.85
    if conf >= 0.4:
        return 0.65
    if conf >= 0.2:
        return 0.45
    return 0.25


def build_domain_points(positioned_nodes, group_colors):
    domain_points = {}

    for node, x, y, color, domain, local_domain, confidence in positioned_nodes:
        region = local_domain if local_domain else "unknown"
        weight = soft_weight(confidence)

        if region not in domain_points:
            domain_points[region] = {
                "color": group_colors.get(region, color),
                "points": []
            }

        domain_points[region]["points"].append((x, y, weight))

    return domain_points


def compute_canvas_bounds(positioned_nodes):
    xs = [x for _, x, _, _, _, _, _ in positioned_nodes]
    ys = [y for _, _, y, _, _, _, _ in positioned_nodes]

    xs.extend([760, 760])
    ys.extend([470, 250])

    pad_x = 220
    pad_y = 180

    return min(xs) - pad_x, max(xs) + pad_x, min(ys) - pad_y, max(ys) + pad_y


def build_density_grid(domain_points, bounds, grid_size=260, sigma=120.0):
    min_x, max_x, min_y, max_y = bounds

    xs = np.linspace(min_x, max_x, grid_size)
    ys = np.linspace(min_y, max_y, grid_size)
    X, Y = np.meshgrid(xs, ys)

    fields = {}

    for domain, info in domain_points.items():
        Z = np.zeros_like(X, dtype=float)

        for px, py, weight in info["points"]:
            d2 = (X - px) ** 2 + (Y - py) ** 2
            Z += weight * np.exp(-d2 / (2.0 * sigma ** 2))

        fields[domain] = {
            "color": info["color"],
            "Z": Z
        }

    return X, Y, fields


def polygon_to_svg_path(seg):
    if seg is None or len(seg) < 3:
        return None

    parts = [f"M {seg[0][0]:.2f} {seg[0][1]:.2f}"]

    for pt in seg[1:]:
        parts.append(f"L {pt[0]:.2f} {pt[1]:.2f}")

    parts.append("Z")
    return " ".join(parts)


def extract_domain_polygons(X, Y, fields):
    domain_polygons = {}
    opacities = [0.16, 0.22, 0.30]

    for domain, info in fields.items():
        Z = info["Z"]
        color = info["color"]
        zmax = float(np.max(Z))

        if zmax <= 1e-8:
            continue

        raw_levels = [zmax * 0.22, zmax * 0.40, zmax * 0.62, zmax * 1.001]
        levels = sorted(set(raw_levels))

        if len(levels) < 2:
            continue

        fig, ax = plt.subplots(figsize=(4, 4))
        cs = ax.contourf(X, Y, Z, levels=levels)
        plt.close(fig)

        polygons = []

        for band_idx, segs in enumerate(cs.allsegs):
            opacity = opacities[min(band_idx, len(opacities) - 1)]

            for seg in segs:
                if seg is None or len(seg) < 3:
                    continue

                path_d = polygon_to_svg_path(seg)

                if path_d:
                    polygons.append({
                        "path": path_d,
                        "opacity": opacity
                    })

        if polygons:
            domain_polygons[domain] = {
                "color": color,
                "polygons": polygons
            }

    return domain_polygons


def write_regions_svg(svg_filename, bounds, domain_polygons):
    min_x, max_x, min_y, max_y = bounds
    width = max_x - min_x
    height = max_y - min_y

    domain_order = [
        "bias",
        "school",
        "family",
        "access",
        "environment",
        "work",
        "controversial",
        "clinical",
        "core",
        "unknown"
    ]

    svg_parts = []

    svg_parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{min_x:.2f} {min_y:.2f} {width:.2f} {height:.2f}" preserveAspectRatio="none">'
    )

    svg_parts.append("""
<defs>
  <filter id="softBlur" x="-20%" y="-20%" width="140%" height="140%">
    <feGaussianBlur stdDeviation="6" />
  </filter>
</defs>
""")

    for domain in domain_order:
        if domain not in domain_polygons:
            continue

        color = domain_polygons[domain]["color"]
        polygons = domain_polygons[domain]["polygons"]

        svg_parts.append(f'<g id="region-{domain}" filter="url(#softBlur)">')

        for poly in polygons:
            svg_parts.append(
                f'<path d="{poly["path"]}" '
                f'fill="{color}" fill-opacity="{poly["opacity"]:.3f}" '
                f'stroke="{color}" stroke-opacity="0.35" stroke-width="8" '
                f'stroke-linejoin="round" />'
            )

        svg_parts.append("</g>")

    svg_parts.append("</svg>")

    with open(svg_filename, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_parts))


def attach_background_to_canvas(html_filename, svg_filename, bounds):
    min_x, max_x, min_y, max_y = bounds
    width = max_x - min_x
    height = max_y - min_y

    with open(html_filename, "r", encoding="utf-8") as f:
        html = f.read()

    js_block = f"""
<script type="text/javascript">
window.addEventListener("load", function() {{
    var bgImage = new Image();
    bgImage.src = "{os.path.basename(svg_filename)}";

    bgImage.onload = function() {{
        if (typeof network !== "undefined") {{
            network.on("beforeDrawing", function(ctx) {{
                ctx.save();
                ctx.globalAlpha = 1.0;
                ctx.drawImage(
                    bgImage,
                    {min_x},
                    {min_y},
                    {width},
                    {height}
                );
                ctx.restore();
            }});
            network.redraw();
        }}
    }};
}});
</script>
"""

    if "</body>" in html:
        html = html.replace("</body>", js_block + "\n</body>", 1)
    else:
        html += "\n" + js_block

    with open(html_filename, "w", encoding="utf-8") as f:
        f.write(html)


def save_graph_with_fuzzy_background(
    net,
    positioned_nodes,
    group_colors,
    html_filename,
    svg_filename,
    grid_size=260,
    sigma=120.0
):
    domain_points = build_domain_points(positioned_nodes, group_colors)
    bounds = compute_canvas_bounds(positioned_nodes)
    X, Y, fields = build_density_grid(domain_points, bounds, grid_size=grid_size, sigma=sigma)
    domain_polygons = extract_domain_polygons(X, Y, fields)

    write_regions_svg(svg_filename, bounds, domain_polygons)

    net.write_html(html_filename)
    # net.show(html_filename, notebook=False)
    attach_background_to_canvas(html_filename, svg_filename, bounds)

    print("Graph saved as:", html_filename)
    webbrowser.open("file://" + os.path.realpath(html_filename))