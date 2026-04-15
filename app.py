import streamlit as st
import random
import math
import matplotlib.pyplot as plt

# -----------------------------
# Sidebar Inputs
# -----------------------------
st.sidebar.title("⚙️ Input Parameters")

demand = st.sidebar.slider("Energy Demand (MW)", 50, 200, 120)
iterations = st.sidebar.slider("Iterations", 100, 1000, 500)
penalty_factor = st.sidebar.slider("Penalty Factor", 1, 20, 10)

st.sidebar.subheader("💰 Cost per Unit")

solar_cost = st.sidebar.number_input("Solar Cost", value=2)
wind_cost = st.sidebar.number_input("Wind Cost", value=3)
grid_cost = st.sidebar.number_input("Grid Cost", value=6)
battery_cost = st.sidebar.number_input("Battery Cost", value=4)

st.sidebar.subheader("🔋 Battery Settings")
battery_max = st.sidebar.slider("Battery Capacity (Max MW)", 10, 100, 50)

# -----------------------------
# Cost Function
# -----------------------------
def cost_function(solution):
    solar, wind, grid, battery = solution

    total = solar + wind + grid + battery
    penalty = abs(demand - total)

    cost = (
        solar_cost * solar +
        wind_cost * wind +
        grid_cost * grid +
        battery_cost * battery
    )

    return cost + penalty_factor * penalty


# -----------------------------
# Neighbor Function
# -----------------------------
def neighbor(sol):
    new = sol[:]

    i = random.randint(0, 3)

    change = random.uniform(-5, 5)
    new[i] = max(0, new[i] + change)

    # Apply battery constraint
    new[3] = min(new[3], battery_max)

    return new


# -----------------------------
# Simulated Annealing
# -----------------------------
def simulated_annealing():
    T = 100
    cooling = 0.95

    current = [random.uniform(10, 50) for _ in range(4)]
    best = current[:]

    history = []

    for _ in range(iterations):

        new = neighbor(current)

        delta = cost_function(new) - cost_function(current)

        if delta < 0 or random.random() < math.exp(-delta / T):
            current = new

        if cost_function(current) < cost_function(best):
            best = current

        history.append(cost_function(current))
        T *= cooling

    return best, history


# -----------------------------
# UI
# -----------------------------
st.title("🌱 Renewable Energy Grid Optimization")
st.subheader("Using Simulated Annealing")

if st.button("Run Optimization 🚀"):

    best, history = simulated_annealing()

    solar, wind, grid, battery = best
    total = solar + wind + grid + battery

    # -----------------------------
    # Pie Chart (Energy Share)
    # -----------------------------
    st.write("### 🔋 Energy Share")

    labels = ["Solar", "Wind", "Grid", "Battery"]
    values = [solar, wind, grid, battery]

    fig1, ax1 = plt.subplots()
    ax1.pie(values, labels=labels, autopct='%1.1f%%')
    st.pyplot(fig1)

    # -----------------------------
    # Cost Convergence Graph
    # -----------------------------
    st.write("### 📉 Cost Convergence")

    fig2, ax2 = plt.subplots()
    ax2.plot(history)
    ax2.set_xlabel("Iterations")
    ax2.set_ylabel("Cost")
    st.pyplot(fig2)

    # -----------------------------
    # Output Values
    # -----------------------------
    st.write("### ⚡ Optimized Energy Distribution")

    st.write(f"☀ Solar: {solar:.2f} MW")
    st.write(f"🌬 Wind: {wind:.2f} MW")
    st.write(f"🏭 Grid: {grid:.2f} MW")
    st.write(f"🔋 Battery: {battery:.2f} MW")
    st.write(f"⚡ Total Supply: {total:.2f} MW")

    # -----------------------------
    # Insights
    # -----------------------------
    st.write("### 💡 Insights")

    st.write("✔ Battery helps store excess energy and reduce cost")
    st.write("✔ Simulated Annealing finds near-optimal energy mix")
    st.write("✔ Grid usage reduces when renewables are sufficient")
    st.write("✔ Demand-supply mismatch is minimized")

    st.success("Optimization Completed 🚀")
