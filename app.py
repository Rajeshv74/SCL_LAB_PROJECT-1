import streamlit as st
import random
import math
import matplotlib.pyplot as plt

st.title("⚡ Renewable Energy Optimization using Simulated Annealing")

# -----------------------------
# User Inputs
# -----------------------------
st.sidebar.header("Input Parameters")

solar_max = st.sidebar.slider("Solar Max Capacity", 0, 100, 50)
wind_max = st.sidebar.slider("Wind Max Capacity", 0, 100, 60)
grid_max = st.sidebar.slider("Grid Max Capacity", 0, 150, 100)

demand = st.sidebar.slider("Energy Demand", 50, 200, 120)

cost_solar = st.sidebar.number_input("Solar Cost", value=2)
cost_wind = st.sidebar.number_input("Wind Cost", value=3)
cost_grid = st.sidebar.number_input("Grid Cost", value=6)

penalty = st.sidebar.number_input("Penalty Factor", value=10)

MAX_CAP = [solar_max, wind_max, grid_max]
COST = [cost_solar, cost_wind, cost_grid]


# -----------------------------
# Cost Function
# -----------------------------
def cost_function(solution):
    total_energy = sum(solution)

    gen_cost = sum(solution[i] * COST[i] for i in range(3))

    mismatch = abs(demand - total_energy)
    penalty_cost = penalty * mismatch

    return gen_cost + penalty_cost


# -----------------------------
# Initial Solution
# -----------------------------
def initial_solution():
    return [random.uniform(0, MAX_CAP[i]) for i in range(3)]


# -----------------------------
# Neighbor Function
# -----------------------------
def neighbor(solution):
    new_solution = solution[:]
    i = random.randint(0, 2)

    change = random.uniform(-5, 5)
    new_solution[i] = max(0, min(MAX_CAP[i], new_solution[i] + change))

    return new_solution


# -----------------------------
# Simulated Annealing
# -----------------------------
def simulated_annealing():
    current = initial_solution()
    best = current[:]

    T = 1000
    T_min = 1
    alpha = 0.95

    cost_history = []

    while T > T_min:
        new = neighbor(current)

        delta = cost_function(new) - cost_function(current)

        if delta < 0 or random.random() < math.exp(-delta / T):
            current = new

        if cost_function(current) < cost_function(best):
            best = current

        cost_history.append(cost_function(current))

        T *= alpha

    return best, cost_history


# -----------------------------
# Run Button
# -----------------------------
if st.button("Run Optimization"):
    best_solution, cost_history = simulated_annealing()

    st.subheader("Optimal Energy Distribution")

    st.write(f"☀️ Solar: {best_solution[0]:.2f}")
    st.write(f"🌬️ Wind: {best_solution[1]:.2f}")
    st.write(f"🔌 Grid: {best_solution[2]:.2f}")

    st.write(f"⚡ Total Energy: {sum(best_solution):.2f}")
    st.write(f"💰 Total Cost: {cost_function(best_solution):.2f}")

    # Plot graph
    fig = plt.figure()
    plt.plot(cost_history)
    plt.xlabel("Iterations")
    plt.ylabel("Cost")
    plt.title("Cost vs Iterations")
    plt.grid()

    st.pyplot(fig)
