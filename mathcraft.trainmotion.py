import streamlit as st
import time
import plotly.graph_objects as go

# Set up the page
st.set_page_config(page_title="Train Motion App", layout="centered")

# Header with logo and author
st.markdown("""
<div style='text-align: center; padding: 1rem 0;'>
    <h1 style='font-size: 3em; color: #1f77b4;'>🚂 MathCraft: Directional Motion & Relative Speed</h1>
    <p style='font-size: 1.5em; font-weight: bold;'>by Xavier Honablue, M.Ed.</p>
    <p style='color: gray; font-size: 0.9em;'>All rights reserved. | Inspired by earlier MathCraft projects like Algebra Rules & Fraction Adventures</p>
</div>
""", unsafe_allow_html=True)

# Lead with a sample word problem
with st.container():
    st.subheader("🎯 Sample Problem")
    st.markdown("""
    **Train A leaves a station at 40 mph. Two hours later, Train B leaves the same station at 60 mph.**
    
    **Question:** When will Train B catch up with Train A?

    This is a classic **same-direction relative motion** problem. You'll see it solved below with interactive controls and animation.
    """)

# User inputs
scenario = st.radio("Choose the scenario:", ["Same Direction", "Opposite Direction"])
trainA_speed = st.slider("Train A Speed (mph)", 20, 200, 40)
trainB_speed = st.slider("Train B Speed (mph)", 30, 300, 60)
head_start = st.slider("Head Start (hours)", 0.5, 5.0, 2.0, 0.5)

# Additional reflection questions
st.markdown("🧪 What happens if Train B is slower than Train A?")
st.markdown("🧠 Can you make it so Train B never catches up?")

# Alternate controls to encourage experimentation
train_a_speed = st.slider("Train A Speed", 10, 100, 40)
train_b_speed = st.slider("Train B Speed", 10, 120, 60)
head_start = st.slider("Train A Head Start (hours)", 0, 5, 2)

# Discovery Challenge
st.markdown("### 💡 Discovery Challenge:")
st.write("Try different values. Can you figure out a formula for how long it takes for Train B to catch Train A?")

# General Rule
st.markdown("🎯 General Rule: Time = Head Start ÷ (Train B Speed – Train A Speed)")

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

# Hint Button
if st.button("Need a Hint?"):
    st.markdown("🔍 Hint 1: Think about how far ahead Train A is.")
    st.markdown("Hint 2: What is the relative speed if trains move in the same direction?")
    st.markdown("Hint 3: Time = Distance ÷ Relative Speed")

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

# Build Your Own Problem Section
st.markdown("---")
st.header("🛠️ Build Your Own Problem")

with st.form("custom_problem"):
    custom_scenario = st.radio("Scenario Type:", ["Same Direction", "Opposite Direction"], key="custom_scenario")
    custom_r1 = st.number_input("Train A Speed (mph)", min_value=1, max_value=500, value=30, key="r1")
    custom_r2 = st.number_input("Train B Speed (mph)", min_value=1, max_value=500, value=60, key="r2")
    custom_headstart = st.number_input("Head Start (hours)", min_value=0.0, max_value=24.0, value=2.0, step=0.5, key="headstart")
    submitted = st.form_submit_button("Solve My Problem")

    if submitted:
        if custom_scenario == "Same Direction":
            if custom_r2 <= custom_r1:
                st.error("Train B must be faster than Train A to catch up.")
            else:
                t = (custom_r1 * custom_headstart) / (custom_r2 - custom_r1)
                st.success(f"📍 Trains will meet after {t:.2f} hours (Same Direction).")
        else:
            d = custom_r1 * custom_headstart
            t = d / (custom_r1 + custom_r2)
            st.success(f"📍 Trains will meet after {t:.2f} hours (Opposite Direction).")

# Reflection Section
st.markdown("### 🧠 Reflect On Your Strategy")
st.text_input("1. What was your plan to solve this?")
st.text_input("2. Did your solution work? Why or why not?")
st.text_input("3. What did you try when it didn’t work right away?")
