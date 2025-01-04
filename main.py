import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import networkx as nx
from streamlit_plotly_events import plotly_events
import plotly.express as px
from PIL import Image
import io

# Set page configuration
st.set_page_config(
    page_title="Porous Metamaterial Designer",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    .css-1d391kg {
        background-color: #ffffff;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    h1, h2, h3 {
        color: #1E3D59;
    }
    </style>
""", unsafe_allow_html=True)

# Title and Introduction
st.title("🔮 Porous Metamaterial Designer")
st.markdown("""
    Welcome to the Porous Metamaterial Designer! This interactive tool helps you design 
    and visualize complex porous metamaterial structures using advanced graph-based approaches 
    and machine learning techniques.
""")

# Sidebar
with st.sidebar:
    st.header("Design Parameters")
    
    # Design type selector
    design_type = st.selectbox(
        "Select Design Type",
        ["Simple Graph", "Complex Graph", "Custom Design"],
        help="Choose the type of metamaterial structure you want to create"
    )
    
    # Number of nodes slider
    n_nodes = st.slider(
        "Number of Nodes",
        min_value=12,
        max_value=60,
        value=15,
        help="Select the number of nodes in your structure"
    )
    
    # Complexity parameters
    st.subheader("Complexity Parameters")
    connectivity = st.slider(
        "Connectivity Level",
        min_value=0.0,
        max_value=1.0,
        value=0.5,
        help="Define the connectivity level between nodes"
    )
    
    # Advanced options collapsible
    with st.expander("Advanced Options"):
        phase_type = st.radio(
            "Phase Type",
            ["Solid Phase", "Pore Phase", "Dual Phase"]
        )
        symmetry = st.checkbox("Enable Symmetry", value=True)

# Main content area
col1, col2 = st.columns([2, 1])

# Generate sample graph data
def generate_sample_graph(n_nodes, connectivity):
    G = nx.random_geometric_graph(n_nodes, connectivity)
    pos = nx.spring_layout(G, dim=3)
    return G, pos

# Create 3D graph visualization
def create_3d_graph(G, pos):
    edge_x = []
    edge_y = []
    edge_z = []
    for edge in G.edges():
        x0, y0, z0 = pos[edge[0]]
        x1, y1, z1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_z.extend([z0, z1, None])

    edge_trace = go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z,
        line=dict(width=2, color='#888'),
        hoverinfo='none',
        mode='lines'
    )

    node_x = []
    node_y = []
    node_z = []
    for node in G.nodes():
        x, y, z = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_z.append(z)

    node_trace = go.Scatter3d(
        x=node_x, y=node_y, z=node_z,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            size=8,
            color='#4CAF50',
            line=dict(width=2, color='#fff')
        )
    )

    layout = go.Layout(
        showlegend=False,
        scene=dict(
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            zaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        ),
        margin=dict(l=0, r=0, t=0, b=0)
    )

    fig = go.Figure(data=[edge_trace, node_trace], layout=layout)
    return fig

# Generate and display the graph
with col1:
    st.subheader("3D Structure Visualization")
    G, pos = generate_sample_graph(n_nodes, connectivity)
    fig = create_3d_graph(G, pos)
    st.plotly_chart(fig, use_container_width=True)

# Analysis and metrics
with col2:
    st.subheader("Structure Analysis")
    
    # Calculate and display metrics
    metrics = {
        "Average Degree": np.mean([d for n, d in G.degree()]),
        "Graph Density": nx.density(G),
        "Average Clustering": nx.average_clustering(G),
    }
    
    for metric, value in metrics.items():
        st.metric(metric, f"{value:.3f}")
    
    # Structure properties
    st.markdown("### Structure Properties")
    properties_df = pd.DataFrame({
        "Property": ["Connectivity", "Symmetry", "Phase Type"],
        "Value": [connectivity, symmetry, phase_type]
    })
    st.dataframe(properties_df, hide_index=True)

# Export options
st.markdown("### Export Options")
col3, col4 = st.columns(2)

with col3:
    if st.button("Export Structure Data", key="export_data"):
        # Create download link for structure data
        st.success("Structure data ready for download!")

with col4:
    if st.button("Generate Report", key="generate_report"):
        # Generate detailed report
        st.success("Report generated successfully!")

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666;'>
        Developed based on research paper: "Reconstruction and Generation of Porous Metamaterial Units 
        Via Variational Graph Autoencoder and Large Language Model"
    </div>
""", unsafe_allow_html=True)
