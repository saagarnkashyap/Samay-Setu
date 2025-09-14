# Railway Traffic Controller Dashboard

## Overview

This is a real-time railway traffic control dashboard built with Streamlit that simulates train management operations. The application provides a comprehensive visualization and control interface for monitoring train movements, analyzing network performance, and making operational decisions. It features live train tracking, network status visualization, performance metrics, and AI-powered recommendations for traffic optimization.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
The application uses Streamlit as the primary web framework, providing a dashboard interface with real-time updates. The frontend is organized into modular components including a top navigation bar, network visualization maps, metrics displays, and control panels. The interface updates every 3 seconds to simulate real-time railway operations.

### Backend Architecture  
The system follows a modular Python architecture with three main utility classes:
- **TrainDataGenerator**: Manages train data simulation and real-time updates
- **NetworkMap**: Handles railway network visualization using Plotly
- **TrainController**: Provides control operations and decision-making algorithms

### Data Management
The application uses in-memory data structures stored in Streamlit's session state for:
- Train information (position, status, delays, priorities)
- Network topology (stations and track segments)
- Historical metrics and decision logs
- Real-time performance data

Data is simulated rather than connected to actual railway systems, with random updates to train positions, delays, and statuses to mimic real-world conditions.

### Visualization System
Plotly is used for creating interactive maps and charts, including:
- Network topology visualization with stations and tracks
- Real-time train position tracking
- Performance metrics graphs and dashboards
- Status indicators for track conditions

### Control Logic
The TrainController implements basic railway operations including:
- Performance metrics calculation (delays, throughput, utilization)
- AI-powered recommendation generation
- Priority-based decision making (Express > Local > Freight)
- Conflict resolution for track usage

## External Dependencies

### Core Libraries
- **Streamlit**: Web application framework for the dashboard interface
- **Pandas**: Data manipulation and analysis for train scheduling data
- **Plotly**: Interactive visualization library for maps and charts
- **NumPy**: Numerical computing support (implicit dependency)

### Simulation Framework
The application is designed as a standalone simulation system without external railway APIs or databases. All data is generated internally using Python's random module and datetime utilities for realistic train operation scenarios.

### Future Integration Points
The architecture supports future integration with:
- OR-Tools or Pyomo for optimization algorithms
- SimPy for advanced train simulation
- Real railway management systems via API connections
- Database systems for persistent data storage