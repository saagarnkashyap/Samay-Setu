import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import time
import random
import threading
from simulation import run_simulation, state

# utils import karne ka
from utils.data_generator import TrainDataGenerator
from utils.network_map import NetworkMap
from utils.train_controller import TrainController

# Page configuration karne ka
st.set_page_config(
    page_title="Indian Railway Traffic Controller Dashboard",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Run the backend in a separate thread
if "sim_started" not in st.session_state:
    threading.Thread(target=run_simulation, daemon=True).start()
    st.session_state.sim_started = True


# Session State initilise karne ka
if "train_generator" not in st.session_state:
    st.session_state.train_generator = TrainDataGenerator()
if "network_map" not in st.session_state:
    st.session_state.network_map = NetworkMap()
if "train_controller" not in st.session_state:
    st.session_state.train_controller = TrainController()
if "last_update" not in st.session_state:
    st.session_state.last_update = datetime.now(ZoneInfo("Asia/Kolkata"))
if "decisions_log" not in st.session_state:
    st.session_state.decisions_log = []
if "metrics_history" not in st.session_state:
    st.session_state.metrics_history = []

# real time data update karne ka re
def update_real_time_data():
    """Update real-time data if enough time has passed"""
    current_time = datetime.now(ZoneInfo("Asia/Kolkata"))

    # Fix: Ensure last_update is datetime
    if "last_update" not in st.session_state or st.session_state.last_update is None:
        st.session_state.last_update = current_time
    elif isinstance(st.session_state.last_update, str):
        try:
            st.session_state.last_update = datetime.fromisoformat(st.session_state.last_update)
        except Exception:
            st.session_state.last_update = current_time

    if current_time - st.session_state.last_update > timedelta(seconds=3):
        st.session_state.train_generator.update_trains()
        st.session_state.last_update = current_time

        # Update metrics history
        metrics = st.session_state.train_controller.calculate_metrics(
            st.session_state.train_generator.trains
        )
        st.session_state.metrics_history.append({
            "timestamp": current_time,
            "metrics": metrics
        })

        # Keep only last 20
        if len(st.session_state.metrics_history) > 20:
            st.session_state.metrics_history = st.session_state.metrics_history[-20:]

# Top Bar type shi
def create_top_bar():
    st.markdown("<h1 style='text-align: center; margin-bottom: 10px;'>🚆 Indian Railway Traffic Decision Support</h1>", unsafe_allow_html=True)

    current_time = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
    st.markdown(f"<h3 style='text-align: center; margin-bottom: 20px;'>🕐 {current_time}</h3>", unsafe_allow_html=True)

    # st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>🎛️ System Controls</h3>", unsafe_allow_html=True)

    # col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    # with col2:
    #     if st.button("🚧 Inject Delay", use_container_width=True):
    #         st.session_state.train_controller.inject_delay(st.session_state.train_generator.trains)
    #         st.success("Delay injected to random train!")
    # with col3:
    #     if st.button("⚠️ Simulate Breakdown", use_container_width=True):
    #         st.session_state.train_controller.simulate_breakdown(st.session_state.train_generator.trains)
    #         st.error("Breakdown simulated!")
    # with col4:
    #     if st.button("🔄 Reset System", type="primary", use_container_width=True):
    #         st.session_state.train_generator = TrainDataGenerator()
    #         st.session_state.decisions_log = []
    #         st.session_state.metrics_history = []
    #         st.success("System reset!")


def create_train_list_panel():
    """Create the left panel with train list"""
    st.subheader("🟢 Active Trains")
    for train in state["active_trains"]:
        st.write(f"{train['name']} ({train['type']}) on {train['route']}")

def create_network_map_panel():
    """Create the center panel with network map"""
    st.subheader("🗺️ Network Map")
    
    # Create the network visualization
    network_fig = st.session_state.network_map.create_network_figure(
        st.session_state.train_generator.trains
    )
    
    st.plotly_chart(network_fig, height=500)
    
    # Network status indicators
    st.subheader("📊 Track Status")
    for train, status in state["track_status"].items():
        st.write(f"{train} → {status}")

def create_metrics_panel():
    """Create the right panel with metrics and recommendations"""
    st.subheader("📈 Performance Metrics")
    
    # Calculate current metrics
    current_metrics = st.session_state.train_controller.calculate_metrics(
        st.session_state.train_generator.trains
    )
    
    # Display KPI cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Average Delay",
            f"{current_metrics['avg_delay']:.1f} min",
            delta=f"{random.uniform(-2, 2):.1f} min"
        )
    with col2:
        st.metric(
            "Throughput",
            f"{current_metrics['throughput']:.1f} trains/hr",
            delta=f"{random.uniform(-1, 3):.1f}"
        )
    with col3:
        st.metric(
            "Utilization",
            f"{current_metrics['utilization']:.1f}%",
            delta=f"{random.uniform(-5, 5):.1f}%"
        )
    
    # Metrics trend chart
    # if len(st.session_state.metrics_history) > 1:
    #     st.markdown("### 📊 Trends")
        
    #     # Create trend data
    #     timestamps = [entry['timestamp'] for entry in st.session_state.metrics_history]
    #     delays = [entry['metrics']['avg_delay'] for entry in st.session_state.metrics_history]
    #     throughput = [entry['metrics']['throughput'] for entry in st.session_state.metrics_history]
        
    #     fig = go.Figure()
    #     fig.add_trace(go.Scatter(x=timestamps, y=delays, name="Avg Delay (min)", line=dict(color='red')))
    #     fig.add_trace(go.Scatter(x=timestamps, y=throughput, name="Throughput (trains/hr)", 
    #                            line=dict(color='blue'), yaxis='y2'))
        
    #     fig.update_layout(
    #         height=200,
    #         yaxis=dict(title="Delay (min)", side="left"),
    #         yaxis2=dict(title="Throughput", overlaying="y", side="right"),
    #         margin=dict(l=0, r=0, t=0, b=0)
    #     )
        
    #     st.plotly_chart(fig)
    
    # Decision log
    st.markdown("### 📋 Recent Decisions")
    if st.session_state.decisions_log:
        recent_decisions = st.session_state.decisions_log[-5:]  # Last 5 decisions
        for decision in reversed(recent_decisions):
            status_color = "🟢" if decision['status'] == 'Applied' else "🔴"
            st.markdown(f"{status_color} **{decision['timestamp'].strftime('%H:%M:%S')}** - {decision['action']}")
    else:
        st.info("No decisions recorded yet.")

    # Manual Log Entry
    st.markdown("### 📝 Manual Log Entry")
    manual_action = st.text_input("Enter manual action or recommendation:")
    if st.button("Log Manual Entry", key="manual_log"):
        if manual_action:
            st.session_state.decisions_log.append({
                'timestamp': datetime.now(ZoneInfo("Asia/Kolkata")),
                'action': manual_action,
                'status': 'Applied'  # Assuming manual entries are always applied
            })
            st.success("Manual entry logged!")
            st.rerun()
        else:
            st.warning("Please enter an action to log.")

def main():
    """Main application function"""
    # Auto-refresh setup
    placeholder = st.empty()
    
    # Update real-time data
    update_real_time_data()
    
    # Create the dashboard layout
    create_top_bar()
    
    st.markdown("---")
    
    # 🚀 AI Recommendations FIRST
    st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>🤖 AI Recommendations</h2>", unsafe_allow_html=True)

    # Sort recommendations by the 'priority' field, treating it as a number.
    # The lowest number (e.g., 1) is the highest priority.
    recommendations = sorted(state["recommendations"], key=lambda x: x.get('priority', float('inf')))

    rec_col1, rec_col2, rec_col3 = st.columns(3, gap="large")

    # Define colors for each recommendation
    colors = ["#007bff", "#28a745", "#ffc107"]

    for i, rec_col in enumerate([rec_col1, rec_col2, rec_col3]):
        if i < len(recommendations):
            rec = recommendations[i]
            with rec_col:
                st.markdown(f"""
                <div style="
                    background-color: #1a1a1a;
                    padding: 25px;
                    border-radius: 15px;
                    border-left: 5px solid {colors[i]};
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    margin-bottom: 20px;
                    color: white;
                ">
                    <h4 style='color: {colors[i]}; margin-bottom: 15px;'>🎯 Recommendation {i+1}</h4>
                    <p><strong>Action:</strong> {rec.get('name', 'N/A')} via alternative track to reduce delay</p>
                    <p><strong>Reason:</strong> Train is delayed by {rec.get('delay', 0)} minutes</p>
                    <p><strong>Priority:</strong> {rec.get('priority', 'N/A')}</p>
                </div>
                """, unsafe_allow_html=True)

                if st.button("✅ Apply Recommendation", key=f"apply_{i+1}", use_container_width=True, type="primary"):
                    st.session_state.decisions_log.append({
                        'timestamp': datetime.now(),
                        'action': f"Applied: {rec.get('name', 'N/A')}",
                        'status': 'Applied'
                    })
                    st.success("Recommendation Applied!")

                if st.button("❌ Dismiss", key=f"dismiss_{i+1}", use_container_width=True):
                    st.session_state.decisions_log.append({
                        'timestamp': datetime.now(),
                        'action': f"Dismissed: {rec.get('name', 'N/A')}",
                        'status': 'Dismissed'
                    })
                    st.info("Recommendation Dismissed!")
    
    st.markdown("---")  # separator between recs and main panels

    # Main panels BELOW recommendations
    col1, col2, col3 = st.columns([1, 2, 1.2])
    
    with col1:
        create_train_list_panel()
    
    with col2:
        create_network_map_panel()
    
    with col3:
        create_metrics_panel()
    
    # Auto-refresh every 3 seconds
    time.sleep(5)
    st.rerun()


if __name__ == "__main__":
    main()
