import streamlit as st
import pandas as pd
import math

st.set_page_config(
    page_title="PendulumLab",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 PendulumLab")
st.write("SHM & Heat Loss Experiment Analyzer")

shm_tab, heat_tab, math_tab  = st.tabs([
    "📐 SHM & Gravity",
    "🌡️ Heat Loss",
    "➿ Chord Displacement"
])

# MODULE 1: SHM AND GRAVITY
with shm_tab:
    st.header("Simple Harmonic Motion - Length vs Period Analysis")
    
    st.write("Please enter the experimental data for **Length, l (m)** and **Time for 20 oscillations (s)** for 5 different lengths:")

    default_shm_data = pd.DataFrame({
        "Length, l (m)": [0.20, 0.30, 0.40, 0.50, 0.60],
        "Time for 20 Oscillations, t (s)": [18.0, 22.0, 25.3, 28.4, 31.0]
    })

    edited_shm_data = st.data_editor(default_shm_data, num_rows="fixed", use_container_width=True)

    edited_shm_data["Period, T (s)"] = round(edited_shm_data["Time for 20 Oscillations, t (s)"] / 20, 3)
    edited_shm_data["T² (s²)"] = round(edited_shm_data["Period, T (s)"]**2, 3)
    
    g_standard = 9.81
    edited_shm_data["Calculated g (m/s²)"] = round(
        (4 * math.pi**2 * edited_shm_data["Length, l (m)"]) / edited_shm_data["T² (s²)"], 3
    )
    edited_shm_data["Percentage Error (%)"] = round(
        abs(edited_shm_data["Calculated g (m/s²)"] - g_standard) / g_standard * 100, 2
    )

    st.subheader("Physics Experiment Results Table")
    st.dataframe(edited_shm_data, use_container_width=True)

    # --- TAMBAH TITIK (0,0) KHUSUS UNTUK GRAF SAHAJA ---
    chart_shm_data = edited_shm_data.copy()
    origin_row_shm = pd.DataFrame({"Length, l (m)": [0.0], "T² (s²)": [0.0]})
    chart_shm_data = pd.concat([origin_row_shm, chart_shm_data], ignore_index=True)

    st.subheader("Graph: T² against l (Length)")
    st.line_chart(
        chart_shm_data,
        x="Length, l (m)",
        y="T² (s²)"
    )

    st.info(
        "💡 The graph above displays the relationship of $T^2$ against $l$ where the slope of the graph can "
        "be used to determine the acceleration due to gravity $g$ graphically."
    )

# MODULE 2: HEAT LOSS
with heat_tab:
    st.header("Temperature & Heat Loss Analysis (Chemistry)")
    
    st.write(
        "This section covers Thermal Equilibrium calculations "
        "as well as the Rate of Heat Loss for stationary and moving pendulums."
    )

    st.subheader("1. Thermal Equilibrium (Specific Heat Capacity)")
    
    col_tc1, col_tc2 = st.columns(2)
    with col_tc1:
        mass_bob = st.number_input("Mass of pendulum bob, m (g)", value=50.0, step=1.0)
        initial_bob_temp = st.number_input("Initial temp of bob (°C)", value=90.0, step=1.0)
    with col_tc2:
        mass_water = st.number_input("Mass of distilled water, m_w (g)", value=200.0, step=5.0)
        initial_water_temp = st.number_input("Initial temp of water (°C)", value=28.0, step=0.5)

    final_mixture_temp = st.number_input("Final equilibrium temp (°C)", value=31.5, step=0.5)
    
    c_water = 4.18
    heat_gain_water = mass_water * c_water * (final_mixture_temp - initial_water_temp)
    temp_change_bob = initial_bob_temp - final_mixture_temp
    
    if temp_change_bob > 0:
        calc_c_bob = heat_gain_water / (mass_bob * temp_change_bob)
    else:
        calc_c_bob = 0.0

    st.metric("Calculated Specific Heat Capacity of Bob, c", f"{calc_c_bob:.2f} J/g°C")
    st.caption("Formula: mc(T₁ - T₃) = m_w c_w (T₃ - T₂)")

    st.divider()

    st.subheader("2. Rate of Heat Loss: Stationary vs Moving Pendulum")

    elapsed_time = st.number_input(
        "Elapsed time, t (seconds)",
        min_value=1,
        value=180, 
        step=30
    )

    col_m, col_s = st.columns(2)

    with col_m:
        st.markdown("**Moving Pendulum (Angle = 30°)**")
        initial_moving = st.number_input("Initial temp (°C)", value=80.0, step=1.0, key="im_chem")
        final_moving = st.number_input("Final temp (°C)", value=65.0, step=1.0, key="fm_chem")

    with col_s:
        st.markdown("**Stationary Pendulum (Angle = 0°)**")
        initial_stationary = st.number_input("Initial temp (°C)", value=80.0, step=1.0, key="is_chem")
        final_stationary = st.number_input("Final temp (°C)", value=70.0, step=1.0, key="fs_chem")

    theta_moving = initial_moving - final_moving
    theta_stationary = initial_stationary - final_stationary

    c_used = calc_c_bob if calc_c_bob > 0 else 0.90 
    
    q_moving = (mass_bob * c_used * theta_moving) / elapsed_time
    q_stationary = (mass_bob * c_used * theta_stationary) / elapsed_time

    res_a, res_b = st.columns(2)
    res_a.metric("Moving Heat Loss Rate, Q", f"{q_moving:.4f} J/s")
    res_b.metric("Stationary Heat Loss Rate, Q", f"{q_stationary:.4f} J/s")

    st.caption("Formula: Q = mcθ / t")

    chart_data = pd.DataFrame({
        "Condition": ["Moving (30°)", "Stationary (0°)"],
        "Heat Loss Rate Q (J/s)": [q_moving, q_stationary]
    })

    st.subheader("Heat Loss Rate Comparison Graph")
    st.bar_chart(
        chart_data,
        x="Condition",
        y="Heat Loss Rate Q (J/s)"
    )

    st.info(
        "💡 Conclusion: Compare the rate of heat loss between the dynamic motion "
        "and static conditions of the pendulum."
    )

# MODULE 3: MATHEMATICS ANALYSIS
with math_tab:
    st.header("Integrated STEM Mini-Research - Mathematics Analysis")
    st.write("Comparative analysis between Arc Length ($s$) and Chord Displacement ($d$) for amplitude angles.")

    length_L = st.number_input("Length of string, L (m)", min_value=0.01, value=0.50, step=0.05)

    st.write("Enter Amplitude / Angle values ($\theta$ in degrees):")
    default_math_data = pd.DataFrame({
        "Angle, θ (°)": [10.0, 30.0, 50.0]
    })
    
    edited_math_data = st.data_editor(default_math_data, num_rows="dynamic", use_container_width=True)

    angles_deg = edited_math_data["Angle, θ (°)"]
    radians_list = [math.radians(deg) for deg in angles_deg]

    edited_math_data["Arc Length, s (m)"] = [round(2 * length_L * r, 4) for r in radians_list]
    edited_math_data["Chord Displacement, d (m)"] = [round(2 * length_L * math.sin(r), 4) for r in radians_list]

    s_vals = edited_math_data["Arc Length, s (m)"]
    d_vals = edited_math_data["Chord Displacement, d (m)"]
    
    percentage_diff = []
    for s, d in zip(s_vals, d_vals):
        if s > 0:
            diff = abs(s - d) / s * 100
            percentage_diff.append(round(diff, 2))
        else:
            percentage_diff.append(0.0)
            
    edited_math_data["Percentage Diff (%)"] = percentage_diff

    st.subheader("Mathematics Results Table")
    st.dataframe(edited_math_data, use_container_width=True)

    # --- TAMBAH TITIK (0,0) KHUSUS UNTUK GRAF SAHAJA ---
    chart_math_data = edited_math_data.copy()
    origin_row_math = pd.DataFrame({"Angle, θ (°)": [0.0], "Percentage Diff (%)": [0.0]})
    chart_math_data = pd.concat([origin_row_math, chart_math_data], ignore_index=True)

    st.subheader("Graph: Angle vs Percentage Difference")
    st.line_chart(
        chart_math_data,
        x="Angle, θ (°)",
        y="Percentage Diff (%)"
    )

    st.info(
        "💡 Conclusions can be made on how the accuracy of the small angle approximation "
        "($\sin\theta \approx \theta$) changes as the angle amplitude increases."
    )