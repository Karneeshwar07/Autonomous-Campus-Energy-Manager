import streamlit as st
import pandas as pd
import re

# Function to highlight ON/OFF decisions
def highlight_decision(val):
    if val == "ON":
        return "background-color: lightgreen; color: black"
    elif val == "OFF":
        return "background-color: lightcoral; color: black"
    else:
        return ""

st.title("Autonomous Campus Energy Manager Dashboard")
st.markdown("""
This dashboard demonstrates how our AI agent manages classroom energy usage.
- **ON/OFF decisions** are highlighted in green/red.
- **Usage charts** show per-classroom trends.
- **Threshold updates** track system adaptation.
- **Interactive slider** lets you test decisions live.
""")
# Read logs.txt file
with open("logs.txt", "r") as f:
    logs = f.readlines()

# Show raw logs
st.write("### Raw Logs")
st.text("".join(logs))

# Parse logs into structured data
data = []
day = None
for line in logs:
    line = line.strip()
    if line.startswith("--- Day"):
        # Example: --- Day 9 ---
        try:
            day = int(line.split()[2])
        except:
            day = None
    elif line.startswith("[Execute]") and day is not None:
        # Example: [Execute] Classroom A: Turn OFF devices
        parts = line.split(":")
        if len(parts) > 1:
            classroom = parts[0].replace("[Execute]", "").strip()
            decision_text = parts[1].strip()
            if "Turn OFF" in decision_text:
                decision = "OFF"
            elif "Keep devices ON" in decision_text or "Turn ON" in decision_text:
                decision = "ON"
            else:
                decision = "UNKNOWN"
            data.append({"Day": day, "Classroom": classroom, "Decision": decision})

# Display parsed data
if data:
    df = pd.DataFrame(data)

    # Summary panel
    total_on = (df["Decision"] == "ON").sum()
    total_off = (df["Decision"] == "OFF").sum()
    st.write("### Summary Panel")
    st.metric("Total ON Decisions", total_on)
    st.metric("Total OFF Decisions", total_off)

    # Normal table
    st.write("### Parsed Decisions")
    st.table(df)

    # Color highlight ON/OFF
    def highlight_decision(val):
        color = "green" if val == "ON" else "red" if val == "OFF" else "gray"
        return f"color: {color}; font-weight: bold"

    st.write("### Decisions Highlighted")
    st.write(df.style.applymap(highlight_decision, subset=["Decision"]))
    import re
import pandas as pd

# Extract usage values from logs
usage_data = []
with open("logs.txt", "r") as f:
    lines = f.readlines()
    day = None
    for line in lines:
        if "--- Day" in line:
            day = int(re.search(r"Day (\d+)", line).group(1))
        if "[Think] Current usage:" in line:
            match = re.search(r"Classroom A': (\d+), 'Classroom B': (\d+)", line)
            if match:
                usage_a = int(match.group(1))
                usage_b = int(match.group(2))
                usage_data.append({"Day": day, "Classroom": "A", "Usage": usage_a})
                usage_data.append({"Day": day, "Classroom": "B", "Usage": usage_b})

usage_df = pd.DataFrame(usage_data)

# Show charts
st.subheader("Classroom Usage Trends")
classroom_a = usage_df[usage_df["Classroom"] == "A"]
classroom_b = usage_df[usage_df["Classroom"] == "B"]

st.line_chart(classroom_a.set_index("Day")["Usage"])
st.line_chart(classroom_b.set_index("Day")["Usage"])
threshold_data = []
with open("logs.txt", "r") as f:
    lines = f.readlines()
    day = None
    for line in lines:
        if "--- Day" in line:
            day = int(re.search(r"Day (\d+)", line).group(1))
        if "[Update] New threshold:" in line:
            match = re.search(r"New threshold: (\d+)", line)
            if match:
                threshold = int(match.group(1))
                threshold_data.append({"Day": day, "Threshold": threshold})

threshold_df = pd.DataFrame(threshold_data)

st.subheader("Threshold Updates Over Days")
st.line_chart(threshold_df.set_index("Day")["Threshold"])
# --- Step 4: Interactive Threshold Slider ---
st.sidebar.subheader("Interactive Controls")
threshold_value = st.sidebar.slider(
    "Set Threshold", min_value=10, max_value=100, value=50, step=5
)

# Apply slider threshold to usage data
usage_df["Decision (Interactive)"] = usage_df["Usage"].apply(
    lambda x: "ON" if x > threshold_value else "OFF"
)

# Show interactive decisions table
st.subheader("Interactive Decisions Based on Slider")
st.write(usage_df.style.applymap(highlight_decision, subset=["Decision (Interactive)"]))
with open("logs.txt", "r") as f:
    log_content = f.read()

st.download_button(
    label="Download Logs",
    data=log_content,
    file_name="logs.txt",
    mime="text/plain"
)