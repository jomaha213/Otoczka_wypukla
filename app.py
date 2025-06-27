import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random
import plotly.graph_objects as go
import math

def convex_hull(points):
    if len(points) <= 1:
        return points

    if all(p == points[0] for p in points):
        return [points[0]]

    points = sorted(set(points))

    def cross(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    return lower[:-1] + upper[:-1]


def determine_hull_type(hull):
    if len(hull) == 1:
        return "punkt"
    elif len(hull) == 2:
        return "odcinek"
    elif len(hull) == 3:
        return "trójkąt"
    elif len(hull) == 4:
        return "czworokąt"
    elif len(hull) >= 4:
        return f"wielokąt ({len(hull)} wierzchołków)"
    else:
        return "nieokreślony"


st.set_page_config(layout="wide")
st.title("Otoczka Wypukła (algorytm monotoniczny Adrewsa) - Analiza Punktów ")

with st.sidebar:
    st.header("⚙️ Ustawienia")

    point_mode = st.radio("Tryb punktów:", ["Ręczne", "Losowe"])
    point_count = st.slider("Liczba punktów", 1, 100, 4)

    if point_mode == "Losowe":
        range_val = st.number_input("Zakres losowania współrzędnych", value=10.0) 
        points = [(random.uniform(-range_val, range_val), random.uniform(-range_val, range_val)) for _ in range(point_count)]
    else:
        points = []
        for i in range(point_count):
            col1, col2 = st.columns(2)
            with col1:
                x = st.number_input(f"P{i+1} - x", key=f"x{i}")
            with col2:
                y = st.number_input(f"P{i+1} - y", key=f"y{i}")
            points.append((x, y))

# Obliczenia
if points:
    hull = convex_hull(points)
    hull_type = determine_hull_type(hull)

    st.subheader("Wyniki")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Typ otoczki:** {hull_type}")
        st.markdown(f"**Liczba punktów:** {len(points)}")
        st.markdown(f"**Punkty w otoczce:** {len(hull)}")

        st.markdown("**Wierzchołki otoczki:**")
        for i, (x, y) in enumerate(hull):
            st.markdown(f"{i+1}. ({x:.2f}, {y:.2f})")

    # with col2:
    #     fig, ax = plt.subplots(figsize=(6, 6))
    #     x_all, y_all = zip(*points)
    #     ax.scatter(x_all, y_all, label="Punkty", c='blue')

    #     if len(hull) >= 2:
    #         hull_points = np.array(hull + [hull[0]])
    #         ax.plot(hull_points[:, 0], hull_points[:, 1], c='red', linewidth=2, label="Otoczka")

    #     ax.axhline(0, color='gray', linewidth=0.5)
    #     ax.axvline(0, color='gray', linewidth=0.5)
    #     ax.set_xlabel("X")
    #     ax.set_ylabel("Y")
    #     ax.set_title("Wizualizacja otoczki wypukłej")
    #     ax.grid(True, linestyle='--', alpha=0.5)
    #     ax.legend()
    #     st.pyplot(fig)
with col2:
    # Dane punktów
    x_all, y_all = zip(*points)

    # Tworzenie wykresu
    fig = go.Figure()

    # Punkty
    fig.add_trace(go.Scatter(
        x=x_all, y=y_all,
        mode='markers',
        name='Punkty',
        marker=dict(color='blue'),
        hovertemplate='X: %{x:.2f}<br>Y: %{y:.2f}<extra></extra>'      
    ))

    # Otoczka wypukła (jeśli istnieje)
    if len(hull) >= 2:
        hull_points = np.array(hull + [hull[0]])
        fig.add_trace(go.Scatter(
            x=hull_points[:, 0],
            y=hull_points[:, 1],
            mode='lines',
            name='Otoczka',
            line=dict(color='red', width=2),
            hovertemplate='X: %{x:.2f}<br>Y: %{y:.2f}<extra></extra>'
        ))

    # Oś X i Y
    fig.add_hline(y=0, line=dict(color='gray', width=0.5))
    fig.add_vline(x=0, line=dict(color='gray', width=0.5))

    # Layout i tytuły
    fig.update_layout(
        title='Wizualizacja otoczki wypukłej',
        xaxis_title='X',
        yaxis_title='Y',
        showlegend=True,
        width=600,
        height=600,
        plot_bgcolor='white'
    )

    fig.update_xaxes(showgrid=True, gridwidth=0.5, gridcolor='lightgray')
    fig.update_yaxes(showgrid=True, gridwidth=0.5, gridcolor='lightgray')

    # Wyświetlenie w Streamlit
    st.plotly_chart(fig, use_container_width=True)
