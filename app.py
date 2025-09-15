# import streamlit as st
# import pandas as pd
# import plotly.graph_objects as go
# from datetime import datetime, timedelta
# from zoneinfo import ZoneInfo
# import time
# import random

# # Import your utils
# from utils.data_generator import TrainDataGenerator
# from utils.network_map import NetworkMap
# from utils.train_controller import TrainController

# # Page configuration
# st.set_page_config(
#     page_title="Indian Railway Traffic Controller Dashboard",
#     page_icon="🚆",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )

# # -------------------------------
# # Session State Initialization
# # -------------------------------
# if "train_generator" not in st.session_state:
#     st.session_state.train_generator = TrainDataGenerator()
# if "network_map" not in st.session_state:
#     st.session_state.network_map = NetworkMap()
# if "train_controller" not in st.session_state:
#     st.session_state.train_controller = TrainController()
# if "last_update" not in st.session_state:
#     st.session_state.last_update = datetime.now(ZoneInfo("Asia/Kolkata"))
# if "decisions_log" not in st.session_state:
#     st.session_state.decisions_log = []
# if "metrics_history" not in st.session_state:
#     st.session_state.metrics_history = []


# # -------------------------------
# # Update Real-Time Data
# def update_real_time_data():
#     """Update real-time data if enough time has passed"""
#     current_time = datetime.now(ZoneInfo("Asia/Kolkata"))

#     # Fix: Ensure last_update is datetime
#     if "last_update" not in st.session_state or st.session_state.last_update is None:
#         st.session_state.last_update = current_time
#     elif isinstance(st.session_state.last_update, str):
#         try:
#             st.session_state.last_update = datetime.fromisoformat(st.session_state.last_update)
#         except Exception:
#             st.session_state.last_update = current_time

#     # Now subtraction is always safe
#     if current_time - st.session_state.last_update > timedelta(seconds=3):
#         st.session_state.train_generator.update_trains()
#         st.session_state.last_update = current_time

#         # Update metrics history
#         metrics = st.session_state.train_controller.calculate_metrics(
#             st.session_state.train_generator.trains
#         )
#         st.session_state.metrics_history.append({
#             "timestamp": current_time,
#             "metrics": metrics
#         })

#         # Keep only last 20
#         if len(st.session_state.metrics_history) > 20:
#             st.session_state.metrics_history = st.session_state.metrics_history[-20:]


# # -------------------------------
# # Top Bar
# # -------------------------------
# def create_top_bar():
#     st.markdown("<h1 style='text-align: center; margin-bottom: 10px;'>🚆 Indian Railway Traffic Decision Support</h1>", unsafe_allow_html=True)

#     current_time = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
#     st.markdown(f"<h3 style='text-align: center; margin-bottom: 20px;'>🕐 {current_time}</h3>", unsafe_allow_html=True)

#     st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>🎛️ System Controls</h3>", unsafe_allow_html=True)

#     col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
#     with col2:
#         if st.button("🚧 Inject Delay", use_container_width=True):
#             st.session_state.train_controller.inject_delay(st.session_state.train_generator.trains)
#             st.success("Delay injected to random train!")
#     with col3:
#         if st.button("⚠️ Simulate Breakdown", use_container_width=True):
#             st.session_state.train_controller.simulate_breakdown(st.session_state.train_generator.trains)
#             st.error("Breakdown simulated!")
#     with col4:
#         if st.button("🔄 Reset System", type="primary", use_container_width=True):
#             st.session_state.train_generator = TrainDataGenerator()
#             st.session_state.decisions_log = []
#             st.session_state.metrics_history = []
#             st.success("System reset!")




# def create_train_list_panel():
#     """Create the left panel with train list"""
#     st.subheader("🚄 Active Trains")
    
#     # Get current trains data
#     trains_df = st.session_state.train_generator.get_trains_dataframe()
    
#     # Add filters
#     col1, col2 = st.columns(2)
#     with col1:
#         status_filter = st.selectbox("Filter by Status", 
#                                    ["All"] + trains_df['Status'].unique().tolist())
#     with col2:
#         type_filter = st.selectbox("Filter by Type", 
#                                  ["All"] + trains_df['Type'].unique().tolist())
    
#     # Apply filters
#     filtered_df = trains_df.copy()
#     if status_filter != "All":
#         filtered_df = filtered_df[filtered_df['Status'] == status_filter]
#     if type_filter != "All":
#         filtered_df = filtered_df[filtered_df['Type'] == type_filter]
    
#     # Display train table with color coding
#     def color_status(val):
#         color_map = {
#             'On Time': 'background-color: #d4edda',
#             'Delayed': 'background-color: #f8d7da',
#             'Waiting': 'background-color: #fff3cd',
#             'Rerouted': 'background-color: #cce5f0'
#         }
#         return color_map.get(val, '')
    
#     styled_df = filtered_df.style.map(color_status, subset=['Status'])
#     st.dataframe(styled_df, height=400)
    
#     # Train summary
#     st.markdown("### 📊 Summary")
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         st.metric("Total Trains", len(trains_df))
#     with col2:
#         delayed_count = len(trains_df[trains_df['Status'] == 'Delayed'])
#         st.metric("Delayed Trains", delayed_count)
#     with col3:
#         on_time_pct = len(trains_df[trains_df['Status'] == 'On Time']) / len(trains_df) * 100
#         st.metric("On Time %", f"{on_time_pct:.1f}%")

# def create_network_map_panel():
#     """Create the center panel with network map"""
#     st.subheader("🗺️ Network Map")
    
#     # Create the network visualization
#     network_fig = st.session_state.network_map.create_network_figure(
#         st.session_state.train_generator.trains
#     )
    
#     st.plotly_chart(network_fig, height=500)
    
#     # Network status indicators
#     st.markdown("### 🚦 Track Status")
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         st.markdown("🟢 **Normal Operations**")
#         st.text("Delhi-Mumbai, Chennai-Kolkata")
#     with col2:
#         st.markdown("🟡 **Congested**")
#         st.text("Mumbai-Chennai route")
#     with col3:
#         st.markdown("🔴 **Maintenance**")
#         st.text("Bangalore-Hyderabad route")

# def create_metrics_panel():
#     """Create the right panel with metrics and recommendations"""
#     st.subheader("📈 Performance Metrics")
    
#     # Calculate current metrics
#     current_metrics = st.session_state.train_controller.calculate_metrics(
#         st.session_state.train_generator.trains
#     )
    
#     # Display KPI cards
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         st.metric(
#             "Average Delay",
#             f"{current_metrics['avg_delay']:.1f} min",
#             delta=f"{random.uniform(-2, 2):.1f} min"
#         )
#     with col2:
#         st.metric(
#             "Throughput",
#             f"{current_metrics['throughput']:.1f} trains/hr",
#             delta=f"{random.uniform(-1, 3):.1f}"
#         )
#     with col3:
#         st.metric(
#             "Utilization",
#             f"{current_metrics['utilization']:.1f}%",
#             delta=f"{random.uniform(-5, 5):.1f}%"
#         )
    
#     # Metrics trend chart
#     if len(st.session_state.metrics_history) > 1:
#         st.markdown("### 📊 Trends")
        
#         # Create trend data
#         timestamps = [entry['timestamp'] for entry in st.session_state.metrics_history]
#         delays = [entry['metrics']['avg_delay'] for entry in st.session_state.metrics_history]
#         throughput = [entry['metrics']['throughput'] for entry in st.session_state.metrics_history]
        
#         fig = go.Figure()
#         fig.add_trace(go.Scatter(x=timestamps, y=delays, name="Avg Delay (min)", line=dict(color='red')))
#         fig.add_trace(go.Scatter(x=timestamps, y=throughput, name="Throughput (trains/hr)", 
#                                line=dict(color='blue'), yaxis='y2'))
        
#         fig.update_layout(
#             height=200,
#             yaxis=dict(title="Delay (min)", side="left"),
#             yaxis2=dict(title="Throughput", overlaying="y", side="right"),
#             margin=dict(l=0, r=0, t=0, b=0)
#         )
        
#         st.plotly_chart(fig)
    
#     # Decision log
#     st.markdown("### 📋 Recent Decisions")
#     if st.session_state.decisions_log:
#         recent_decisions = st.session_state.decisions_log[-5:]  # Last 5 decisions
#         for decision in reversed(recent_decisions):
#             status_color = "🟢" if decision['status'] == 'Applied' else "🔴"
#             st.markdown(f"{status_color} **{decision['timestamp'].strftime('%H:%M:%S')}** - {decision['action']}")
#     else:
#         st.info("No decisions recorded yet.")

# def main():
#     """Main application function"""
#     # Auto-refresh setup
#     placeholder = st.empty()
    
#     # Update real-time data
#     update_real_time_data()
    
#     # Create the dashboard layout
#     create_top_bar()
    
#     st.markdown("---")
    
#     # Main panels
#     col1, col2, col3 = st.columns([1, 2, 1.2])
    
#     with col1:
#         create_train_list_panel()
    
#     with col2:
#         create_network_map_panel()
    
#     with col3:
#         create_metrics_panel()
    
#     # Add spacing before AI recommendations
#     st.markdown("<br><br>", unsafe_allow_html=True)
    
#     # AI Recommendations spanning full width
#     st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>🤖 AI Recommendations</h2>", unsafe_allow_html=True)
    
#     recommendations = st.session_state.train_controller.generate_recommendations(
#         st.session_state.train_generator.trains
#     )
    
#     # Full-width 3-column layout for recommendations
#     rec_col1, rec_col2, rec_col3 = st.columns(3, gap="large")
    
#     with rec_col1:
#         if len(recommendations) > 0:
#             rec = recommendations[0]
#             st.markdown("""
#             <div style="
#                 background-color: #f8f9fa;
#                 padding: 25px;
#                 border-radius: 15px;
#                 border-left: 5px solid #007bff;
#                 box-shadow: 0 2px 10px rgba(0,0,0,0.1);
#                 margin-bottom: 20px;
#             ">
#             """, unsafe_allow_html=True)
            
#             st.markdown(f"<h4 style='color: #007bff; margin-bottom: 15px;'>🎯 Recommendation 1</h4>", unsafe_allow_html=True)
#             st.markdown(f"**Action:** {rec['action']}")
#             st.markdown(f"**Reason:** {rec['reason']}")
#             st.markdown(f"**Priority:** {rec['priority']}")
            
#             st.markdown("</div>", unsafe_allow_html=True)
            
#             if st.button("✅ Apply Recommendation", key="apply_1", use_container_width=True, type="primary"):
#                 st.session_state.decisions_log.append({
#                     'timestamp': datetime.now(),
#                     'action': rec['action'],
#                     'status': 'Applied'
#                 })
#                 st.success("Recommendation Applied!")
            
#             if st.button("❌ Dismiss", key="dismiss_1", use_container_width=True):
#                 st.session_state.decisions_log.append({
#                     'timestamp': datetime.now(),
#                     'action': rec['action'],
#                     'status': 'Dismissed'
#                 })
#                 st.info("Recommendation Dismissed!")
    
#     with rec_col2:
#         if len(recommendations) > 1:
#             rec = recommendations[1]
#             st.markdown("""
#             <div style="
#                 background-color: #f8f9fa;
#                 padding: 25px;
#                 border-radius: 15px;
#                 border-left: 5px solid #28a745;
#                 box-shadow: 0 2px 10px rgba(0,0,0,0.1);
#                 margin-bottom: 20px;
#             ">
#             """, unsafe_allow_html=True)
            
#             st.markdown(f"<h4 style='color: #28a745; margin-bottom: 15px;'>🎯 Recommendation 2</h4>", unsafe_allow_html=True)
#             st.markdown(f"**Action:** {rec['action']}")
#             st.markdown(f"**Reason:** {rec['reason']}")
#             st.markdown(f"**Priority:** {rec['priority']}")
            
#             st.markdown("</div>", unsafe_allow_html=True)
            
#             if st.button("✅ Apply Recommendation", key="apply_2", use_container_width=True, type="primary"):
#                 st.session_state.decisions_log.append({
#                     'timestamp': datetime.now(),
#                     'action': rec['action'],
#                     'status': 'Applied'
#                 })
#                 st.success("Recommendation Applied!")
            
#             if st.button("❌ Dismiss", key="dismiss_2", use_container_width=True):
#                 st.session_state.decisions_log.append({
#                     'timestamp': datetime.now(),
#                     'action': rec['action'],
#                     'status': 'Dismissed'
#                 })
#                 st.info("Recommendation Dismissed!")
    
#     with rec_col3:
#         if len(recommendations) > 2:
#             rec = recommendations[2]
#             st.markdown("""
#             <div style="
#                 background-color: #f8f9fa;
#                 padding: 25px;
#                 border-radius: 15px;
#                 border-left: 5px solid #ffc107;
#                 box-shadow: 0 2px 10px rgba(0,0,0,0.1);
#                 margin-bottom: 20px;
#             ">
#             """, unsafe_allow_html=True)
            
#             st.markdown(f"<h4 style='color: #ffc107; margin-bottom: 15px;'>🎯 Recommendation 3</h4>", unsafe_allow_html=True)
#             st.markdown(f"**Action:** {rec['action']}")
#             st.markdown(f"**Reason:** {rec['reason']}")
#             st.markdown(f"**Priority:** {rec['priority']}")
            
#             st.markdown("</div>", unsafe_allow_html=True)
            
#             if st.button("✅ Apply Recommendation", key="apply_3", use_container_width=True, type="primary"):
#                 st.session_state.decisions_log.append({
#                     'timestamp': datetime.now(),
#                     'action': rec['action'],
#                     'status': 'Applied'
#                 })
#                 st.success("Recommendation Applied!")
            
#             if st.button("❌ Dismiss", key="dismiss_3", use_container_width=True):
#                 st.session_state.decisions_log.append({
#                     'timestamp': datetime.now(),
#                     'action': rec['action'],
#                     'status': 'Dismissed'
#                 })
#                 st.info("Recommendation Dismissed!")
    
#     # Auto-refresh every 3 seconds
#     time.sleep(1)
#     st.rerun()

# if __name__ == "__main__":
#     main()






import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import time
import random

# Import your utils
from utils.data_generator import TrainDataGenerator
from utils.network_map import NetworkMap
from utils.train_controller import TrainController

# Page configuration
st.set_page_config(
    page_title="Indian Railway Traffic Controller Dashboard",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------------
# Session State Initialization
# -------------------------------
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


# -------------------------------
# Update Real-Time Data
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

    # Now subtraction is always safe
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


# -------------------------------
# Top Bar
# -------------------------------
def create_top_bar():
    st.markdown("<h1 style='text-align: center; margin-bottom: 10px;'>🚆 Indian Railway Traffic Decision Support</h1>", unsafe_allow_html=True)

    current_time = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
    st.markdown(f"<h3 style='text-align: center; margin-bottom: 20px;'>🕐 {current_time}</h3>", unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>🎛️ System Controls</h3>", unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    with col2:
        if st.button("🚧 Inject Delay", use_container_width=True):
            st.session_state.train_controller.inject_delay(st.session_state.train_generator.trains)
            st.success("Delay injected to random train!")
    with col3:
        if st.button("⚠️ Simulate Breakdown", use_container_width=True):
            st.session_state.train_controller.simulate_breakdown(st.session_state.train_generator.trains)
            st.error("Breakdown simulated!")
    with col4:
        if st.button("🔄 Reset System", type="primary", use_container_width=True):
            st.session_state.train_generator = TrainDataGenerator()
            st.session_state.decisions_log = []
            st.session_state.metrics_history = []
            st.success("System reset!")

def main():
    """Main application function"""
    # Auto-refresh setup
    placeholder = st.empty()
    
    # Update real-time data
    update_real_time_data()
    
    # Create the dashboard layout
    create_top_bar()
    
    st.markdown("---")
    
    # Main panels
    col1, col2, col3 = st.columns([1, 2, 1.2])
    
    with col1:
        create_train_list_panel()
    
    with col2:
        create_network_map_panel()
    
    with col3:
        create_metrics_panel()
    
    # Add spacing before AI recommendations
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # AI Recommendations spanning full width
    st.markdown("<h2 style='text-align: center; margin-bottom: 30px;'>🤖 AI Recommendations</h2>", unsafe_allow_html=True)
    
    recommendations = st.session_state.train_controller.generate_recommendations(
        st.session_state.train_generator.trains
    )
    
    # Full-width 3-column layout for recommendations
    rec_col1, rec_col2, rec_col3 = st.columns(3, gap="large")
    
    with rec_col1:
        if len(recommendations) > 0:
            rec = recommendations[0]
            st.markdown("""
            <div style="
                background-color: #f8f9fa;
                padding: 25px;
                border-radius: 15px;
                border-left: 5px solid #007bff;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            ">
            """, unsafe_allow_html=True)
            
            st.markdown(f"<h4 style='color: #007bff; margin-bottom: 15px;'>🎯 Recommendation 1</h4>", unsafe_allow_html=True)
            st.markdown(f"**Action:** {rec['action']}")
            st.markdown(f"**Reason:** {rec['reason']}")
            st.markdown(f"**Priority:** {rec['priority']}")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            if st.button("✅ Apply Recommendation", key="apply_1", use_container_width=True, type="primary"):
                st.session_state.decisions_log.append({
                    'timestamp': datetime.now(),
                    'action': rec['action'],
                    'status': 'Applied'
                })
                st.success("Recommendation Applied!")
            
            if st.button("❌ Dismiss", key="dismiss_1", use_container_width=True):
                st.session_state.decisions_log.append({
                    'timestamp': datetime.now(),
                    'action': rec['action'],
                    'status': 'Dismissed'
                })
                st.info("Recommendation Dismissed!")
    
    with rec_col2:
        if len(recommendations) > 1:
            rec = recommendations[1]
            st.markdown("""
            <div style="
                background-color: #f8f9fa;
                padding: 25px;
                border-radius: 15px;
                border-left: 5px solid #28a745;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            ">
            """, unsafe_allow_html=True)
            
            st.markdown(f"<h4 style='color: #28a745; margin-bottom: 15px;'>🎯 Recommendation 2</h4>", unsafe_allow_html=True)
            st.markdown(f"**Action:** {rec['action']}")
            st.markdown(f"**Reason:** {rec['reason']}")
            st.markdown(f"**Priority:** {rec['priority']}")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            if st.button("✅ Apply Recommendation", key="apply_2", use_container_width=True, type="primary"):
                st.session_state.decisions_log.append({
                    'timestamp': datetime.now(),
                    'action': rec['action'],
                    'status': 'Applied'
                })
                st.success("Recommendation Applied!")
            
            if st.button("❌ Dismiss", key="dismiss_2", use_container_width=True):
                st.session_state.decisions_log.append({
                    'timestamp': datetime.now(),
                    'action': rec['action'],
                    'status': 'Dismissed'
                })
                st.info("Recommendation Dismissed!")
    
    with rec_col3:
        if len(recommendations) > 2:
            rec = recommendations[2]
            st.markdown("""
            <div style="
                background-color: #f8f9fa;
                padding: 25px;
                border-radius: 15px;
                border-left: 5px solid #ffc107;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            ">
            """, unsafe_allow_html=True)
            
            st.markdown(f"<h4 style='color: #ffc107; margin-bottom: 15px;'>🎯 Recommendation 3</h4>", unsafe_allow_html=True)
            st.markdown(f"**Action:** {rec['action']}")
            st.markdown(f"**Reason:** {rec['reason']}")
            st.markdown(f"**Priority:** {rec['priority']}")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            if st.button("✅ Apply Recommendation", key="apply_3", use_container_width=True, type="primary"):
                st.session_state.decisions_log.append({
                    'timestamp': datetime.now(),
                    'action': rec['action'],
                    'status': 'Applied'
                })
                st.success("Recommendation Applied!")
            
            if st.button("❌ Dismiss", key="dismiss_3", use_container_width=True):
                st.session_state.decisions_log.append({
                    'timestamp': datetime.now(),
                    'action': rec['action'],
                    'status': 'Dismissed'
                })
                st.info("Recommendation Dismissed!")


def create_train_list_panel():
    """Create the left panel with train list"""
    st.subheader("🚄 Active Trains")
    
    # Get current trains data
    trains_df = st.session_state.train_generator.get_trains_dataframe()
    
    # Add filters
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.selectbox("Filter by Status", 
                                   ["All"] + trains_df['Status'].unique().tolist())
    with col2:
        type_filter = st.selectbox("Filter by Type", 
                                 ["All"] + trains_df['Type'].unique().tolist())
    
    # Apply filters
    filtered_df = trains_df.copy()
    if status_filter != "All":
        filtered_df = filtered_df[filtered_df['Status'] == status_filter]
    if type_filter != "All":
        filtered_df = filtered_df[filtered_df['Type'] == type_filter]
    
    # Display train table with color coding
    def color_status(val):
        color_map = {
            'On Time': 'background-color: #d4edda',
            'Delayed': 'background-color: #f8d7da',
            'Waiting': 'background-color: #fff3cd',
            'Rerouted': 'background-color: #cce5f0'
        }
        return color_map.get(val, '')
    
    styled_df = filtered_df.style.map(color_status, subset=['Status'])
    st.dataframe(styled_df, height=400)
    
    # Train summary
    st.markdown("### 📊 Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Trains", len(trains_df))
    with col2:
        delayed_count = len(trains_df[trains_df['Status'] == 'Delayed'])
        st.metric("Delayed Trains", delayed_count)
    with col3:
        on_time_pct = len(trains_df[trains_df['Status'] == 'On Time']) / len(trains_df) * 100
        st.metric("On Time %", f"{on_time_pct:.1f}%")

def create_network_map_panel():
    """Create the center panel with network map"""
    st.subheader("🗺️ Network Map")
    
    # Create the network visualization
    network_fig = st.session_state.network_map.create_network_figure(
        st.session_state.train_generator.trains
    )
    
    st.plotly_chart(network_fig, height=500)
    
    # Network status indicators
    st.markdown("### 🚦 Track Status")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("🟢 **Normal Operations**")
        st.text("Delhi-Mumbai, Chennai-Kolkata")
    with col2:
        st.markdown("🟡 **Congested**")
        st.text("Mumbai-Chennai route")
    with col3:
        st.markdown("🔴 **Maintenance**")
        st.text("Bangalore-Hyderabad route")

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
    if len(st.session_state.metrics_history) > 1:
        st.markdown("### 📊 Trends")
        
        # Create trend data
        timestamps = [entry['timestamp'] for entry in st.session_state.metrics_history]
        delays = [entry['metrics']['avg_delay'] for entry in st.session_state.metrics_history]
        throughput = [entry['metrics']['throughput'] for entry in st.session_state.metrics_history]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=timestamps, y=delays, name="Avg Delay (min)", line=dict(color='red')))
        fig.add_trace(go.Scatter(x=timestamps, y=throughput, name="Throughput (trains/hr)", 
                               line=dict(color='blue'), yaxis='y2'))
        
        fig.update_layout(
            height=200,
            yaxis=dict(title="Delay (min)", side="left"),
            yaxis2=dict(title="Throughput", overlaying="y", side="right"),
            margin=dict(l=0, r=0, t=0, b=0)
        )
        
        st.plotly_chart(fig)
    
    # Decision log
    st.markdown("### 📋 Recent Decisions")
    if st.session_state.decisions_log:
        recent_decisions = st.session_state.decisions_log[-5:]  # Last 5 decisions
        for decision in reversed(recent_decisions):
            status_color = "🟢" if decision['status'] == 'Applied' else "🔴"
            st.markdown(f"{status_color} **{decision['timestamp'].strftime('%H:%M:%S')}** - {decision['action']}")
    else:
        st.info("No decisions recorded yet.")


    
    # Auto-refresh every 3 seconds
    time.sleep(1)
    st.rerun()

if __name__ == "__main__":
    main()





