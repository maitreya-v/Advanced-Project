# Import Streamlit.
import streamlit as st
# Import the HTML component renderer for PyVis output.
import streamlit.components.v1 as components
# Import PyVis.
from pyvis.network import Network

# Set the page configuration.
st.set_page_config(page_title="Chronological Causal Graph Explorer", layout="wide")

# Show the page title.
st.title("Chronological Causal Graph Explorer")
# Show a short description.
st.caption("Move the year slider to compare graph structure over time while keeping node positions fixed.")

# Define the two main nodes that always exist.
CORE_NODES = {
    "ADHD": {
        "label": "ADHD (Underlying Disorder)",
        "color": "#1f77b4",
        "size": 45,
        "x": 0,
        "y": 0,
    },
    "Diagnosis Status": {
        "label": "Diagnosis Status",
        "color": "#ff7f0e",
        "size": 45,
        "x": 0,
        "y": 350,
    },
}

# Define the base nodes and their fixed positions.
BASE_POSITIONED_NODES = {
    "Age": (-500, -200),
    "Gender": (-380, -200),
    "Genetic Risk": (-300, -80),
    "Symptom Severity": (-200, -200),
    "Symptom Type": (-200, -80),
    "Comorbid Conditions": (-100, -300),
    "Parental Awareness": (-500, 200),
    "Parenting Style": (-500, 80),
    "Family Stress": (-380, 130),
    "Household Stability": (-500, 320),
    "Teacher Referral Rate": (-100, -420),
    "Classroom Size": (100, -500),
    "Academic Demands": (300, -500),
    "School Resources": (300, -380),
    "Workplace Accommodations": (500, -200),
    "Access to Mental Health Care": (500, 200),
    "Provider Availability": (650, 80),
    "Diagnostic Criteria Variability": (300, 420),
    "Waiting Time for Assessment": (500, 350),
    "Cost of Evaluation": (500, 480),
    "Stigma": (400, -300),
    "Gender Bias": (200, -300),
    "Cultural Norms": (550, -380),
    "Socioeconomic Status": (650, -80),
    "Age at Diagnosis": (0, 500),
    "Misdiagnosis Rate": (200, 480),
    "Functional Impairment": (-300, 300),
    "Quality of Life": (-500, 450),
}

# Define the base edges that exist in the earliest version.
BASE_EDGES = [
    ("Genetic Risk", "ADHD", "+"),
    ("Comorbid Conditions", "ADHD", "+"),
    ("ADHD", "Symptom Severity", "+"),
    ("ADHD", "Symptom Type", "+"),
    ("Age", "Symptom Severity", "+"),
    ("Gender", "Symptom Type", "+"),
    ("Symptom Severity", "Functional Impairment", "+"),
    ("Comorbid Conditions", "Functional Impairment", "+"),
    ("Functional Impairment", "Quality of Life", "-"),
    ("Symptom Severity", "Teacher Referral Rate", "+"),
    ("Symptom Type", "Teacher Referral Rate", "+"),
    ("Classroom Size", "Teacher Referral Rate", "+"),
    ("Academic Demands", "Teacher Referral Rate", "+"),
    ("School Resources", "Teacher Referral Rate", "+"),
    ("Parenting Style", "Symptom Severity", "+"),
    ("Family Stress", "Symptom Severity", "+"),
    ("Household Stability", "Family Stress", "-"),
    ("Parental Awareness", "Diagnosis Status", "+"),
    ("Teacher Referral Rate", "Age at Diagnosis", "-"),
    ("Access to Mental Health Care", "Age at Diagnosis", "-"),
    ("Provider Availability", "Waiting Time for Assessment", "-"),
    ("Waiting Time for Assessment", "Age at Diagnosis", "+"),
    ("Cost of Evaluation", "Age at Diagnosis", "+"),
    ("Age at Diagnosis", "Diagnosis Status", "+"),
    ("Diagnostic Criteria Variability", "Misdiagnosis Rate", "+"),
    ("Misdiagnosis Rate", "Diagnosis Status", "-"),
    ("Cultural Norms", "Stigma", "+"),
    ("Stigma", "Parental Awareness", "-"),
    ("Gender Bias", "Teacher Referral Rate", "+"),
    ("Gender Bias", "Diagnosis Status", "+"),
    ("Socioeconomic Status", "Access to Mental Health Care", "+"),
    ("Socioeconomic Status", "Cost of Evaluation", "-"),
]

# Define year-specific additions.
YEAR_CONFIGS = {
    1970: {
        "period_label": "1970s",
        "new_nodes": {},
        "new_edges": [],
    },
    2010: {
        "period_label": "2010s",
        "new_nodes": {
            "School Screening Programs": (0, -620),
            "Inattentive Presentation Awareness": (-50, -300),
            "Female ADHD Recognition": (250, -420),
            "Social Media Awareness": (850, -320),
            "Online Self-Education": (850, -150),
            "Adult ADHD Awareness": (850, 20),
            "Telehealth Access": (850, 180),
            "Medication Availability": (850, 340),
            "College Accommodations": (700, -220),
            "Workplace Awareness": (700, -450),
            "Overdiagnosis Concern": (350, 620),
        },
        "new_edges": [
            ("Social Media Awareness", "Parental Awareness", "+"),
            ("Social Media Awareness", "Adult ADHD Awareness", "+"),
            ("Online Self-Education", "Parental Awareness", "+"),
            ("Online Self-Education", "Diagnosis Status", "+"),
            ("School Screening Programs", "Teacher Referral Rate", "+"),
            ("Inattentive Presentation Awareness", "Teacher Referral Rate", "+"),
            ("Female ADHD Recognition", "Diagnosis Status", "+"),
            ("Gender Bias", "Female ADHD Recognition", "-"),
            ("Adult ADHD Awareness", "Diagnosis Status", "+"),
            ("College Accommodations", "Diagnosis Status", "+"),
            ("Workplace Awareness", "Workplace Accommodations", "+"),
            ("Telehealth Access", "Access to Mental Health Care", "+"),
            ("Telehealth Access", "Waiting Time for Assessment", "-"),
            ("Medication Availability", "Diagnosis Status", "+"),
            ("Diagnostic Criteria Variability", "Diagnosis Status", "+"),
            ("Overdiagnosis Concern", "Misdiagnosis Rate", "+"),
            ("Stigma", "Diagnosis Status", "-"),
            ("Stigma", "Access to Mental Health Care", "-"),
        ],
    },
}

# Define a helper that returns all nodes available up to the selected year.
def get_nodes_for_year(selected_year):
    # Start with the base positions.
    nodes = dict(BASE_POSITIONED_NODES)
    # Loop through years in order.
    for year in sorted(YEAR_CONFIGS):
        # Stop once the selected year is passed.
        if year > selected_year:
            break
        # Merge in the new nodes for that year.
        nodes.update(YEAR_CONFIGS[year]["new_nodes"])
    # Return the accumulated nodes.
    return nodes

# Define a helper that returns all edges available up to the selected year.
def get_edges_for_year(selected_year):
    # Start with the base edges.
    edges = list(BASE_EDGES)
    # Loop through years in order.
    for year in sorted(YEAR_CONFIGS):
        # Stop once the selected year is passed.
        if year > selected_year:
            break
        # Extend with year-specific edges.
        edges.extend(YEAR_CONFIGS[year]["new_edges"])
    # Return the accumulated edges.
    return edges

# Define a helper that returns the nodes introduced exactly in the selected year.
def get_new_nodes_for_selected_year(selected_year):
    # Return the matching year's additions.
    return list(YEAR_CONFIGS[selected_year]["new_nodes"].keys())

# Define a helper that builds the network HTML.
def build_network_html(selected_year):
    # Create the network.
    net = Network(height="900px", width="100%", directed=True, bgcolor="#ffffff")
    # Disable unstable layout behavior.
    net.toggle_physics(False)
    # Apply fixed, comparison-friendly options.
    net.set_options(
        """
        var options = {
          "layout": {
            "improvedLayout": false
          },
          "physics": {
            "enabled": false
          },
          "interaction": {
            "dragNodes": false,
            "dragView": true,
            "zoomView": true,
            "hover": true
          },
          "edges": {
            "smooth": false,
            "font": {
              "size": 12,
              "align": "top"
            }
          }
        }
        """
    )
    # Get the nodes for the selected year.
    visible_nodes = get_nodes_for_year(selected_year)
    # Get the edges for the selected year.
    visible_edges = get_edges_for_year(selected_year)
    # Get the nodes introduced in the selected year.
    selected_year_new_nodes = set(get_new_nodes_for_selected_year(selected_year))
    # Add the two main nodes first.
    for node_id, attrs in CORE_NODES.items():
        # Add the main node.
        net.add_node(
            node_id,
            label=attrs["label"],
            color=attrs["color"],
            size=attrs["size"],
            x=attrs["x"],
            y=attrs["y"],
            fixed=True,
            physics=False,
            font={"size": 18, "color": "black"},
            title=f"{attrs['label']}<br>Present through all years",
        )
    # Add all other visible nodes.
    for node_id, (x_pos, y_pos) in visible_nodes.items():
        # Choose a different color for nodes newly introduced in the selected year.
        node_color = "#ffe599" if node_id in selected_year_new_nodes else "#dddddd"
        # Build a tooltip label for the node.
        node_title = f"{node_id}<br>Introduced in {selected_year}" if node_id in selected_year_new_nodes else f"{node_id}<br>Present by {selected_year}"
        # Add the node to the network.
        net.add_node(
            node_id,
            label=node_id,
            color=node_color,
            size=25,
            x=x_pos,
            y=y_pos,
            fixed=True,
            physics=False,
            font={"size": 13, "color": "black"},
            title=node_title,
        )
    # Add all edges.
    for source, target, sign in visible_edges:
        # Pick the edge color by sign.
        edge_color = "green" if sign == "+" else "red"
        # Add the edge.
        net.add_edge(
            source,
            target,
            label=sign,
            color=edge_color,
            arrows="to",
            title=f"{source} → {target} ({sign})",
        )
    # Add a legend box.
    net.add_node(
        "LEGEND_NODE",
        label="LEGEND:\n\nGreen Edge (+): Positive Effect\nRed Edge (-): Negative Effect\nYellow Node: Added in Selected Year",
        shape="box",
        color="#f5f5f5",
        size=30,
        x=1120,
        y=560,
        fixed=True,
        physics=False,
        font={"size": 14, "color": "black", "face": "Arial"},
    )
    # Add a period label box.
    net.add_node(
        "PERIOD_NODE",
        label=f"CHRONOLOGICAL HYPOTHESIS:\n\n{YEAR_CONFIGS[selected_year]['period_label']}",
        shape="box",
        color="#f5f5f5",
        size=30,
        x=1120,
        y=350,
        fixed=True,
        physics=False,
        font={"size": 14, "color": "black", "face": "Arial"},
    )
    # Return the final HTML.
    return net.generate_html(notebook=False)

# Show a sidebar section for controls.
st.sidebar.header("Controls")
# Show the year selector.
selected_year = st.sidebar.select_slider("Choose a year", options=sorted(YEAR_CONFIGS.keys()), value=1970)
# Show a small help note.
st.sidebar.info("Existing node positions stay fixed across years. Add later years by extending YEAR_CONFIGS.")

# Create a two-column layout for summary details.
left_col, right_col = st.columns([4, 1])

# Build the HTML for the selected year.
graph_html = build_network_html(selected_year)

# Render the graph in the large column.
with left_col:
    # Show the graph section title.
    st.subheader(f"Graph for {YEAR_CONFIGS[selected_year]['period_label']}")
    # Render the PyVis HTML.
    components.html(graph_html, height=930, scrolling=True)

# Render year-specific notes in the right column.
with right_col:
    # Show a small summary panel title.
    st.subheader("What changed")
    # Get the newly introduced nodes.
    newly_added = get_new_nodes_for_selected_year(selected_year)
    # Handle the case where there are no additions.
    if not newly_added:
        # Show a message for the base year.
        st.write("No new variables added in this baseline year.")
    # Handle years with additions.
    else:
        # Show the list of new variables.
        for item in newly_added:
            # Write each new variable.
            st.write(f"• {item}")
    # Show a divider.
    st.divider()
    # Show a short implementation note.
    st.write("To add another year, create a new entry inside `YEAR_CONFIGS` with:")
    # Show the implementation bullets.
    st.write("• `period_label`")
    st.write("• `new_nodes`")
    st.write("• `new_edges`")
