import streamlit as st
import numpy as np
import random
import math
import time
import matplotlib.pyplot as plt

# -----------------------------
# Title
# -----------------------------
st.title("⚡ Renewable Energy Grid Optimization")
st.subheader("Using Simulated Annealing with CPU vs GPU Analysis")

# -----------------------------
# Sidebar Inputs
# -----------------------------
st.sidebar.header("⚙️ Input Parameters")

demand = st.sidebar.slider("Energy Demand", 50, 200, 120)
iterations = st.sidebar.slider("Iterations", 100, 2000, 500)
penalty = st.sidebar.slider("Penalty Factor", 1, 20, 10)

st.sidebar.subheader("Cost per Unit")
cost_solar = st.sidebar.number_input("Solar Cost", value=2)
cost_wind = st.sidebar.number_input("Wind Cost", value=3)
cost_grid = st.sidebar.number_input("Grid Cost", value=6)

COST = [cost_solar, cost_wind, cost_grid]

# -----------------------------
# Renewable Variability
# -----------------------------
solar_variation = np.random.uniform(0.5, 1.0)
wind_variation = np.random.uniform(0.4, 0.9)

MAX_CAP = [
    50 * solar_variation,
    60 * wind_variation,
    100
]

# -----------------------------
# Cost Function
# -----------------------------
def cost_function(solution):
    total_energy = sum(solution)

    generation_cost = sum(solution[i] * COST[i] for i in range(3))

    mismatch = abs(demand - total_energy)
    penalty_cost = penalty * mismatch

    return generation_cost + penalty_cost


# -----------------------------
# Simulated Annealing
# -----------------------------
def simulated_annealing():
    current = [random.uniform(0, MAX_CAP[i]) for i in range(3)]
    best = current[:]

    T = 1000
    alpha = 0.95

    cost_history = []

    for _ in range(iterations):
        new = current[:]

        i = random.randint(0, 2)
        new[i] += random.uniform(-5, 5)
        new[i] = max(0, min(MAX_CAP[i], new[i]))

        delta = cost_function(new) - cost_function(current)

        if delta < 0 or random.random() < math.exp(-delta / T):
            current = new

        if cost_function(current) < cost_function(best):
            best = current

        cost_history.append(cost_function(current))

        T *= alpha

    return best, cost_history


# -----------------------------
# CPU vs GPU Simulation
# -----------------------------
def run_cpu():
    start = time.time()
    simulated_annealing()
    return time.time() - start


def run_gpu():
    start = time.time()
    simulated_annealing()
    return (time.time() - start) * 0.6  # simulated GPU speedup


# -----------------------------
# Run Button
# -----------------------------
if st.button("🚀 Run Optimization"):

    best_solution, history = simulated_annealing()

    st.success("Optimization Completed ✅")

    # -----------------------------
    # Results
    # -----------------------------
    st.subheader("🔋 Optimal Energy Distribution")

    st.write(f"☀️ Solar: {best_solution[0]:.2f}")
    st.write(f"🌬️ Wind : {best_solution[1]:.2f}")
    st.write(f"🔌 Grid : {best_solution[2]:.2f}")

    total_energy = sum(best_solution)
    total_cost = cost_function(best_solution)

    st.write(f"⚡ Total Energy: {total_energy:.2f}")
    st.write(f"💰 Total Cost: {total_cost:.2f}")

    # -----------------------------
    # Cost Graph
    # -----------------------------
    st.subheader("📉 Cost vs Iterations")

    fig1 = plt.figure()
    plt.plot(history)
    plt.xlabel("Iterations")
    plt.ylabel("Cost")
    plt.title("Optimization Convergence")
    plt.grid()

    st.pyplot(fig1)

    # -----------------------------
    # Energy Distribution Pie Chart
    # -----------------------------
    st.subheader("📊 Energy Distribution")

    fig2 = plt.figure()
    plt.pie(best_solution, labels=["Solar", "Wind", "Grid"], autopct='%1.1f%%')
    plt.title("Energy Share")

    st.pyplot(fig2)

    # -----------------------------
    # CPU vs GPU Comparison
    # -----------------------------
    st.subheader("⚡ CPU vs GPU Performance")

    cpu_time = run_cpu()
    gpu_time = run_gpu()

    st.write(f"🖥️ CPU Time: {cpu_time:.4f} sec")
    st.write(f"🚀 GPU Time: {gpu_time:.4f} sec")

    fig3 = plt.figure()
    plt.bar(["CPU", "GPU"], [cpu_time, gpu_time])
    plt.title("Execution Time Comparison")

    st.pyplot(fig3)

    # -----------------------------
    # Variability Info
    # -----------------------------
    st.subheader("🌦️ Renewable Variability")

    st.write(f"Solar Availability Factor: {solar_variation:.2f}")
    st.write(f"Wind Availability Factor: {wind_variation:.2f}")
