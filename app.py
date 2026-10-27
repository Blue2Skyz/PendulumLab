import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import math

st.set_page_config(
    page_title="PendulumLab",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 PendulumLab")
st.write("Integrated STEM Mini-Research Project Analyzer")

# --- TOP TABS (Optimized for Mobile Browsing) ---
home_tab, shm_tab, heat_tab, math_tab, industrial_tab = st.tabs([
    "🏠 Home",
    "📐 SHM & Gravity",
    "🌡️ Heat Loss",
    "➿ Chord Displacement",
    "🏗️ Industrial App"
])

# --- 1. HOME TAB ---
with home_tab:
    st.header("Welcome to PendulumLab")
    st.write("### Integrated STEM Mini-Research Project Analyzer")
    
    st.markdown(r"""
    This interactive web application is specially developed to analyze experimental laboratory data based on the **Simple Pendulum** concept across various STEM disciplines:
    
    * **📐 Physics:** Interactive Pendulum Simulator (up to 90° drag limit with top metrics bar), SHM Analysis, and $T^2$ vs $l$ graph.
    * **🌡️ Chemistry:** Thermal equilibrium (specific heat capacity) and heat loss rates ($Q$) between stationary and moving pendulums.
    * **➿ Mathematics:** Geometric comparison between *Arc Length* ($s$) and *Chord Displacement* ($d$), and small-angle approximation error ($\sin\theta \approx \theta$).
    * **🏗️ Industrial App:** Real-world engineering applications separated by Physics, Chemistry, and Mathematics.
    """)
    
    st.info("👆 Tap on the tabs above to switch between different experimental modules easily on your phone!")

# --- 2. MODULE 1: SHM AND GRAVITY (SIMULATOR UP TO 90° WITH TOP METRICS BAR) ---
with shm_tab:
    st.header("Simple Harmonic Motion & Live Simulator")
    
    st.subheader("Live pendulum simulator (interactive)")
    st.write(r"θ = -(g/L) sin θ — Drag the bob up to 90° with real-time metrics displayed at the top:")

    # HTML5 Canvas with 90-degree limit and top metrics bar
    components.html("""
    <div style="display: flex; flex-direction: column; align-items: center; background-color: #0e1117; padding: 12px; border-radius: 12px; font-family: sans-serif;">
        <!-- Top Metrics Bar -->
        <div style="display: flex; justify-content: space-around; width: 100%; max-width: 360px; margin-bottom: 10px; font-size: 13px; font-weight: bold; background: #1f2937; padding: 8px; border-radius: 8px;">
            <span id="angleText" style="color: #60a5fa;">θ: 45.0°</span>
            <span id="sText" style="color: #34d399;">s: 0.79 m</span>
            <span id="dText" style="color: #f43f5e;">d: 0.76 m</span>
        </div>
        <canvas id="simCanvas" width="360" height="260" style="background: #181c24; border-radius: 8px; cursor: grab;"></canvas>
    </div>
    <script>
    const canvas = document.getElementById('simCanvas');
    const ctx = canvas.getContext('2d');

    const L_meters = 1.0; 
    const L_pixels = 140; 
    let angle = Math.PI / 4; 
    let omega = 0; 
    let alpha = 0; 
    const g = 9.81; 

    const originX = canvas.width / 2;
    const originY = 25;

    let isDragging = false;
    let lastTime = performance.now();
    let trail = [];

    canvas.addEventListener('mousedown', (e) => { isDragging = true; canvas.style.cursor = 'grabbing'; });
    window.addEventListener('mouseup', () => { isDragging = false; canvas.style.cursor = 'grab'; });

    canvas.addEventListener('mousemove', (e) => {
        if (isDragging) {
            const rect = canvas.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            const mouseY = e.clientY - rect.top;
            angle = Math.atan2(mouseX - originX, mouseY - originY);
            if (angle < -Math.PI / 2) angle = -Math.PI / 2;
            if (angle > Math.PI / 2) angle = Math.PI / 2;
            omega = 0;
            trail = [];
        }
    });

    canvas.addEventListener('touchmove', (e) => {
        if (isDragging && e.touches.length > 0) {
            const rect = canvas.getBoundingClientRect();
            const mouseX = e.touches[0].clientX - rect.left;
            const mouseY = e.touches[0].clientY - rect.top;
            angle = Math.atan2(mouseX - originX, mouseY - originY);
            if (angle < -Math.PI / 2) angle = -Math.PI / 2;
            if (angle > Math.PI / 2) angle = Math.PI / 2;
            omega = 0;
            trail = [];
        }
    });
    canvas.addEventListener('touchstart', () => { isDragging = true; });
    window.addEventListener('touchend', () => { isDragging = false; });

    function animate(currentTime) {
        const dt = Math.min((currentTime - lastTime) / 1000, 0.1);
        lastTime = currentTime;

        ctx.clearRect(0, 0, canvas.width, canvas.height);

        if (!isDragging) {
            alpha = -(g / L_meters) * Math.sin(angle);
            omega += alpha * dt;
            omega *= Math.pow(0.993, dt * 60); 
            angle += omega * dt;
        }

        const bobX = originX + L_pixels * Math.sin(angle);
        const bobY = originY + L_pixels * Math.cos(angle);

        trail.push({x: bobX, y: bobY});
        if (trail.length > 12) trail.shift();

        for (let i = 0; i < trail.length; i++) {
            let p = trail[i];
            let alphaVal = i / trail.length;
            ctx.beginPath();
            ctx.arc(p.x, p.y, 7 * alphaVal, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(59, 130, 246, ${alphaVal * 0.4})`;
            ctx.fill();
        }

        ctx.beginPath();
        ctx.arc(originX, originY, L_pixels, Math.PI/2 - Math.PI/2, Math.PI/2 + Math.PI/2);
        ctx.strokeStyle = '#374151';
        ctx.setLineDash([3, 3]);
        ctx.stroke();
        ctx.setLineDash([]);

        ctx.beginPath();
        ctx.moveTo(originX, originY);
        ctx.lineTo(bobX, bobY);
        ctx.strokeStyle = '#f3f4f6';
        ctx.lineWidth = 2.5;
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(originX, originY);
        ctx.lineTo(originX, originY + L_pixels + 10);
        ctx.strokeStyle = '#4b5563';
        ctx.setLineDash([2, 2]);
        ctx.stroke();
        ctx.setLineDash([]);

        ctx.beginPath();
        ctx.arc(originX, originY, 6, 0, Math.PI * 2);
        ctx.fillStyle = '#9ca3af';
        ctx.fill();

        ctx.beginPath();
        ctx.arc(bobX, bobY, 18, 0, Math.PI * 2);
        let grad = ctx.createRadialGradient(bobX-4, bobY-4, 2, bobX, bobY, 18);
        grad.addColorStop(0, '#60a5fa');
        grad.addColorStop(1, '#1d4ed8');
        ctx.fillStyle = grad;
        ctx.fill();
        ctx.lineWidth = 2;
        ctx.strokeStyle = '#93c5fd';
        ctx.stroke();
        ctx.closePath();

        const degVal = Math.abs(angle * (180 / Math.PI));
        const arcS = L_meters * Math.abs(angle);
        const chordD = 2 * L_meters * Math.sin(Math.abs(angle) / 2);

        document.getElementById('angleText').innerText = 'θ: ' + degVal.toFixed(1) + '°';
        document.getElementById('sText').innerText = 's: ' + arcS.toFixed(2) + ' m';
        document.getElementById('dText').innerText = 'd: ' + chordD.toFixed(2) + ' m';

        requestAnimationFrame(animate);
    }
    requestAnimationFrame(animate);
    </script>
    """, height=315)

    st.divider()

    st.subheader("📊 Experimental Data Analysis")
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
        r"💡 The graph above displays the relationship of $T^2$ against $l$ where the slope of the graph can "
        "be used to determine the acceleration due to gravity $g$ graphically."
    )

# --- 3. MODULE 2: HEAT LOSS ---
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

# --- 4. MODULE 3: MATHEMATICS ANALYSIS ---
with math_tab:
    st.header("Integrated STEM Mini-Research - Mathematics Analysis")
    st.write("Comparative analysis between Arc Length ($s$) and Chord Displacement ($d$) for amplitude angles.")

    length_L = st.number_input("Length of string, L (m)", min_value=0.01, value=0.50, step=0.05)

    st.write(r"Enter Amplitude / Angle values ($\theta$ in degrees):")
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
        r"💡 Conclusions can be made on how the accuracy of the small angle approximation "
        r"($\sin\theta \approx \theta$) changes as the angle amplitude increases."
    )

# --- 5. MODULE 4: INDUSTRIAL APPLICATIONS (SEPARATED INTO SUB-TABS) ---
with industrial_tab:
    st.header("Industrial & Real-World Applications")
    st.write(
        "Explore real-world engineering and industrial implementations bridged from our STEM laboratory experiments."
    )
    
    # Nested Sub-Tabs to completely separate Physics, Chemistry, and Mathematics
    ind_phys_sub, ind_chem_sub, ind_math_sub = st.tabs([
        "📐 Physics (TMD)", 
        "🌡️ Chemistry (Cooling)", 
        "➿ Math (Robotics)"
    ])
    
    with ind_phys_sub:
        st.subheader("Physics Application: Tuned Mass Damper (TMD) in Skyscrapers")
        st.write(
            "High-rise buildings like Taipei 101 use large pendulum systems to counteract lateral forces from "
            "typhoons and earthquakes, applying Simple Harmonic Motion (SHM) and resonance control."
        )
        
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            building_mass = st.number_input("Effective Building Mass (Tonnes)", value=50000.0, step=1000.0, key="ind_bm")
            damper_mass = st.number_input("Damper Pendulum Mass, M (Tonnes)", value=660.0, step=10.0, key="ind_dm")
        with col_p2:
            natural_freq = st.number_input("Structural Natural Frequency, f₀ (Hz)", value=0.25, step=0.01, key="ind_nf")
            external_freq = st.number_input("External Wind/Quake Frequency, f (Hz)", value=0.24, step=0.01, key="ind_ef")
            
        freq_diff = abs(natural_freq - external_freq)
        mass_ratio = (damper_mass / building_mass) * 100
        
        col_res1, col_res2 = st.columns(2)
        col_res1.metric("Mass Ratio (μ)", f"{mass_ratio:.2f}%")
        col_res2.metric("Frequency Difference (|f₀ - f|)", f"{freq_diff:.3f} Hz")
        
        if freq_diff < 0.02:
            st.warning("⚠️ Resonance risk detected! TMD is actively counter-oscillating to dissipate kinetic energy.")
        else:
            st.success("✅ Structure is stable. Pendulum damping is on standby.")
            
    with ind_chem_sub:
        st.subheader("Chemistry Application: Industrial Quenching & Turbine Cooling")
        st.write(
            "In manufacturing and aerospace, moving components (like turbine blades) experience forced convection "
            "and rapid heat loss compared to static parts, heavily relying on specific heat capacity and thermal equilibrium."
        )
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            fluid_flow_speed = st.number_input("Coolant Flow Speed / Motion (m/s)", value=5.0, step=0.5, key="ind_c_speed")
            surface_area = st.number_input("Component Surface Area (m²)", value=2.5, step=0.1, key="ind_c_area")
        with col_c2:
            initial_temp_ind = st.number_input("Initial Component Temp (°C)", value=500.0, step=10.0, key="ind_c_temp")
            coolant_temp = st.number_input("Coolant Bath Temp (°C)", value=30.0, step=1.0, key="ind_c_bath")
            
        heat_transfer_coeff = 25.0 + (5.0 * fluid_flow_speed)
        q_dissipation = heat_transfer_coeff * surface_area * (initial_temp_ind - coolant_temp) / 1000
        
        st.metric("Estimated Heat Dissipation Rate (Q)", f"{q_dissipation:.2f} kW")
        st.info(
            "💡 **Industry Connection:** Just like our moving pendulum experiment, dynamic fluid motion significantly "
            "accelerates the rate of heat loss ($Q$), crucial for designing efficient turbine cooling systems and metal quenching baths."
        )
        
    with ind_math_sub:
        st.subheader("Mathematics Application: Robotics & Cable Suspension Geometry")
        st.write(
            r"Engineers use small-angle approximations ($\sin\theta \approx \theta$) and arc-to-chord length variations "
            "to linearize complex trigonometric equations in robotic joint movements and suspension bridge cable designs."
        )
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            joint_angle_deg = st.number_input("Robot Joint / Cable Angle (degrees)", value=15.0, step=1.0, key="ind_m_angle")
        with col_m2:
            link_length = st.number_input("Link / Cable Length, L (m)", value=2.0, step=0.1, key="ind_m_len")
            
        rad_val = math.radians(joint_angle_deg)
        approx_arc = 2 * link_length * rad_val
        exact_chord = 2 * link_length * math.sin(rad_val)
        math_error = abs(approx_arc - exact_chord) / approx_arc * 100 if approx_arc > 0 else 0
        
        m_res1, m_res2, m_res3 = st.columns(3)
        m_res1.metric("Arc Length (Linear Model)", f"{approx_arc:.4f} m")
        m_res2.metric("Chord Length (Exact Model)", f"{exact_chord:.4f} m")
        m_res3.metric("Linearization Error", f"{math_error:.4f}%")
        
        st.info(
            "💡 **Industry Connection:** For small angles (< 15°), the linearization error is minimal (< 0.5%), "
            "allowing microcontrollers in robotic arm kinematics to calculate movements instantly without processing delays."
        )
