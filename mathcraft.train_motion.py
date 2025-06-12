import streamlit as st
import time
import plotly.graph_objects as go

# Set up the page
st.set_page_config(page_title="Train Motion App", layout="centered")
st.title("🚆 Train Motion Simulator")

# User inputs
scenario = st.radio("Choose the scenario:", ["Same Direction", "Opposite Direction"])
trainA_speed = st.slider("Train A Speed (mph)", 20, 200, 40)
trainB_speed = st.slider("Train B Speed (mph)", 30, 300, 60)
head_start = st.slider("Head Start (hours)", 0.5, 5.0, 2.0, 0.5)

# Calculate meeting time and distances
def calculate_meeting():
    if scenario == "Same Direction":
        if trainB_speed <= trainA_speed:
            return None
        t = (trainA_speed * head_start) / (trainB_speed - trainA_speed)
        return t
    else:
        distance = trainA_speed * head_start
        t = distance / (trainA_speed + trainB_speed)
        return t

meeting_time = calculate_meeting()

# Display result
if meeting_time is not None:
    st.success(f"📍 Trains will meet after {meeting_time:.2f} hours.")
else:
    st.error("Train B is not faster than Train A. They will never meet in the same direction.")

# Animation section
if st.button("Start Animation") and meeting_time is not None:
    max_time = meeting_time + 2
    frame = st.empty()
    track_width = 600  # Scale for plot

    for t in range(0, int(max_time * 10) + 1):
        t = t / 10.0
        trainA_dist = trainA_speed * (t + head_start)
        trainB_dist = trainB_speed * t if t > 0 else 0

        if scenario == "Opposite Direction":
            trainB_dist = trainB_dist
            positionA = trainA_dist
            positionB = (trainA_speed * head_start + trainB_dist)
        else:
            positionA = trainA_dist
            positionB = trainB_dist

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[positionA], y=[1], mode='markers+text',
                                 marker=dict(size=20), text=["Train A"], name="Train A"))
        fig.add_trace(go.Scatter(x=[positionB], y=[-1], mode='markers+text',
                                 marker=dict(size=20), text=["Train B"], name="Train B"))

        fig.update_layout(
            title=f"Time: {t:.1f} hours",
            xaxis=dict(title="Distance (mi)", range=[0, trainA_speed * (max_time + head_start)]),
            yaxis=dict(visible=False),
            height=300,
            showlegend=False
        )
        frame.plotly_chart(fig)
        time.sleep(0.1)

# Explanation Panel
with st.expander("📘 Learn the Math"):
    st.markdown("""
    ### Same Direction:
    If Train A leaves earlier, and Train B is faster:
    - **Formula**: `t = (r1 * h) / (r2 - r1)`
    - r1 = slower speed (Train A), r2 = faster speed (Train B), h = head start time

    ### Opposite Direction:
    If trains move toward each other:
    - **Formula**: `t = d / (r1 + r2)`
    - d = initial distance = `r1 * h`
    """)

