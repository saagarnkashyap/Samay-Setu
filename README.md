# Indian Railway Traffic Control Dashboard 🚆

A comprehensive real-time railway traffic management system built with Streamlit, featuring AI-powered decision support for Indian railway operations.

## Features

### 🎛️ System Controls
- **Real-time Monitoring**: Live updates every 3 seconds
- **Delay Injection**: Simulate train delays for testing
- **Breakdown Simulation**: Test system response to train failures
- **System Reset**: Clear all data and restart

### 🚄 Train Management
- **Active Train Tracking**: Monitor all trains in the network
- **Status Filtering**: Filter by train status (On Time, Delayed, Waiting, Rerouted)
- **Type Filtering**: Filter by train type (Express, Passenger, Freight, etc.)
- **Real-time Updates**: Live position and status updates

### 🗺️ Network Visualization
- **Interactive Map**: Visual representation of Indian railway network
- **Track Status**: Real-time track condition monitoring
- **Station Markers**: Key railway stations across India
- **Train Positions**: Live train location tracking

### 📈 Performance Metrics
- **Average Delay Tracking**: Monitor system-wide delays
- **Throughput Analysis**: Trains per hour metrics
- **Utilization Monitoring**: Track capacity usage
- **Trend Analysis**: Historical performance charts

### 🤖 AI Recommendations
- **Smart Routing**: Automatic rerouting suggestions for delayed trains
- **Maintenance Alerts**: Proactive maintenance recommendations
- **Priority Management**: Express train priority handling
- **Capacity Optimization**: Track utilization improvements

## Railway Network Coverage

### Major Stations
- **Delhi**: New Delhi Railway Station
- **Mumbai**: Mumbai Central
- **Chennai**: Chennai Central
- **Kolkata**: Howrah/Kolkata
- **Bangalore**: Bangalore City Junction
- **Hyderabad**: Secunderabad/Hyderabad

### Andhra Pradesh Network
- **Vijayawada**: Major junction connecting North and South
- **Visakhapatnam**: Coastal railway hub
- **Tirupati**: Pilgrimage destination
- **Guntur**: Agricultural region connectivity
- **Rajahmundry**: Godavari region hub
- **Kurnool**: Rayalaseema connectivity

### South India Connections
- **Nellore**: Coastal Andhra connectivity
- **Kadapa**: Rayalaseema region
- **Anantapur**: Border connectivity

## Train Types Supported

### Premium Services
- **Rajdhani Express**: Long-distance premium trains
- **Shatabdi Express**: Day-time intercity trains
- **Vande Bharat**: Modern semi-high speed trains
- **Duronto Express**: Non-stop long distance

### Regular Services
- **Mail Express**: Long-distance passenger trains
- **Superfast Express**: Fast passenger services
- **Intercity Express**: Medium distance services
- **Jan Shatabdi**: Affordable day trains
- **Garib Rath**: Budget air-conditioned trains

### Local Services
- **Passenger Trains**: Local passenger services
- **MEMU/DEMU**: Electric/Diesel multiple units
- **Suburban**: Short distance commuter trains
- **Local Passenger**: Basic passenger services

### Freight Services
- **Freight Trains**: Goods transportation
- **Special Trains**: Festival and seasonal services

## Technology Stack

- **Frontend**: Streamlit
- **Visualization**: Plotly
- **Data Processing**: Pandas
- **Real-time Updates**: Python threading
- **Mapping**: OpenStreetMap integration

## Installation

1. Clone the repository:
```bash
git clone https://github.com/saagarnkashyap/traintypeshi.git
cd traintypeshi
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## Usage

1. **Launch the Dashboard**: Run `streamlit run app.py`
2. **Monitor Trains**: View active trains in the left panel
3. **Check Network**: Monitor track conditions on the map
4. **Review Metrics**: Analyze performance in the right panel
5. **Apply Recommendations**: Use AI suggestions for optimization

## System Architecture

### Core Components

1. **TrainDataGenerator**: Manages train data and real-time updates
2. **NetworkMap**: Handles railway network visualization
3. **TrainController**: Provides AI recommendations and metrics

### Data Flow

1. **Data Generation**: Simulated train data with realistic parameters
2. **Real-time Updates**: Continuous position and status updates
3. **AI Analysis**: Intelligent recommendations based on current state
4. **Visualization**: Interactive dashboard with multiple views

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.

## Contact

For questions or support, please open an issue on GitHub.

---

**Note**: This is a simulation system for educational and demonstration purposes. It does not connect to real railway systems or control actual train operations.
