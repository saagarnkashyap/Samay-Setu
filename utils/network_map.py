import plotly.graph_objects as go
import plotly.express as px
import random
from typing import List, Dict, Any

class NetworkMap:
    """Creates and manages the railway network visualization"""
    
    def __init__(self):
        self.stations = self._define_stations()
        self.tracks = self._define_tracks()
    
    def _define_stations(self) -> Dict[str, Dict[str, float]]:
        """Define Indian railway station positions with focus on South India"""
        return {
            'New Delhi': {'lat': 28.6139, 'lon': 77.2090},
            'Mumbai Central': {'lat': 19.0176, 'lon': 72.8562},
            'Chennai Central': {'lat': 13.0827, 'lon': 80.2707},
            'Kolkata': {'lat': 22.5726, 'lon': 88.3639},
            'Bangalore City': {'lat': 12.9716, 'lon': 77.5946},
            'Hyderabad': {'lat': 17.3850, 'lon': 78.4867},
            'Vijayawada': {'lat': 16.5062, 'lon': 80.6480},
            'Visakhapatnam': {'lat': 17.6868, 'lon': 83.2185},
            'Tirupati': {'lat': 13.6288, 'lon': 79.4192},
            'Guntur': {'lat': 16.3067, 'lon': 80.4365},
            'Rajahmundry': {'lat': 17.0005, 'lon': 81.8044},
            'Kurnool': {'lat': 15.8309, 'lon': 78.0422},
            'Nellore': {'lat': 14.4426, 'lon': 79.9864},
            'Kadapa': {'lat': 14.4753, 'lon': 78.8252},
            'Anantapur': {'lat': 14.6819, 'lon': 77.6006}
        }
    
    def _define_tracks(self) -> List[Dict[str, Any]]:
        """Define track segments between Indian railway stations"""
        return [
            # Major routes
            {'from': 'New Delhi', 'to': 'Mumbai Central', 'status': 'normal'},
            {'from': 'Mumbai Central', 'to': 'Chennai Central', 'status': 'congested'},
            {'from': 'Chennai Central', 'to': 'Kolkata', 'status': 'normal'},
            {'from': 'Kolkata', 'to': 'Bangalore City', 'status': 'normal'},
            {'from': 'Bangalore City', 'to': 'Hyderabad', 'status': 'maintenance'},
            
            # Andhra Pradesh network
            {'from': 'Hyderabad', 'to': 'Vijayawada', 'status': 'normal'},
            {'from': 'Vijayawada', 'to': 'Visakhapatnam', 'status': 'normal'},
            {'from': 'Vijayawada', 'to': 'Guntur', 'status': 'normal'},
            {'from': 'Guntur', 'to': 'Rajahmundry', 'status': 'normal'},
            {'from': 'Rajahmundry', 'to': 'Visakhapatnam', 'status': 'normal'},
            
            # South India connections
            {'from': 'Bangalore City', 'to': 'Tirupati', 'status': 'normal'},
            {'from': 'Tirupati', 'to': 'Chennai Central', 'status': 'normal'},
            {'from': 'Tirupati', 'to': 'Nellore', 'status': 'normal'},
            {'from': 'Nellore', 'to': 'Chennai Central', 'status': 'normal'},
            
            # Rayalaseema region
            {'from': 'Bangalore City', 'to': 'Kurnool', 'status': 'normal'},
            {'from': 'Kurnool', 'to': 'Anantapur', 'status': 'normal'},
            {'from': 'Anantapur', 'to': 'Kadapa', 'status': 'normal'},
            {'from': 'Kadapa', 'to': 'Tirupati', 'status': 'normal'},
            
            # Alternative routes
            {'from': 'New Delhi', 'to': 'Chennai Central', 'status': 'normal'},
            {'from': 'Hyderabad', 'to': 'Bangalore City', 'status': 'normal'},
        ]
    
    def create_network_figure(self, trains: List[Dict[str, Any]]) -> go.Figure:
        """Create the network visualization figure"""
        fig = go.Figure()
        
        # Add track lines
        self._add_tracks_to_figure(fig)
        
        # Add stations
        self._add_stations_to_figure(fig)
        
        # Add trains
        self._add_trains_to_figure(fig, trains)
        
        # Configure layout for India
        fig.update_layout(
            title="Indian Railway Network Status",
            showlegend=True,
            height=500,
            mapbox=dict(
                style="open-street-map",
                center=dict(lat=20.0, lon=77.0),  # Center of India
                zoom=5
            ),
            margin=dict(l=0, r=0, t=30, b=0)
        )
        
        return fig
    
    def _add_tracks_to_figure(self, fig: go.Figure):
        """Add track segments to the figure"""
        for track in self.tracks:
            from_station = self.stations[track['from']]
            to_station = self.stations[track['to']]
            
            # Color based on track status
            color_map = {
                'normal': 'green',
                'congested': 'orange',
                'maintenance': 'red'
            }
            color = color_map.get(track['status'], 'gray')
            width = 4 if track['status'] == 'congested' else 2
            
            fig.add_trace(go.Scattermapbox(
                lat=[from_station['lat'], to_station['lat']],
                lon=[from_station['lon'], to_station['lon']],
                mode='lines',
                line=dict(color=color, width=width),
                name=f"Track {track['from']}-{track['to']}",
                hovertext=f"Status: {track['status'].title()}",
                showlegend=False
            ))
    
    def _add_stations_to_figure(self, fig: go.Figure):
        """Add station markers to the figure"""
        station_names = list(self.stations.keys())
        station_lats = [self.stations[name]['lat'] for name in station_names]
        station_lons = [self.stations[name]['lon'] for name in station_names]
        
        fig.add_trace(go.Scattermapbox(
            lat=station_lats,
            lon=station_lons,
            mode='markers+text',
            marker=dict(
                size=15,
                color='blue',
                symbol='rail'
            ),
            text=station_names,
            textposition='top center',
            textfont=dict(size=10, color='black'),
            name='Stations',
            hovertext=[f"Station: {name}" for name in station_names]
        ))
    
    def _add_trains_to_figure(self, fig: go.Figure, trains: List[Dict[str, Any]]):
        """Add train markers to the figure"""
        # Group trains by status for better visualization
        status_groups = {}
        for train in trains:
            status = train['status']
            if status not in status_groups:
                status_groups[status] = {'lats': [], 'lons': [], 'texts': [], 'ids': []}
            
            status_groups[status]['lats'].append(train['position']['lat'])
            status_groups[status]['lons'].append(train['position']['lon'])
            status_groups[status]['texts'].append(train['train_id'])
            status_groups[status]['ids'].append(train['train_id'])
        
        # Color mapping for train status
        status_colors = {
            'On Time': 'green',
            'Delayed': 'red',
            'Waiting': 'orange',
            'Rerouted': 'purple'
        }
        
        # Add train markers by status
        for status, data in status_groups.items():
            fig.add_trace(go.Scattermapbox(
                lat=data['lats'],
                lon=data['lons'],
                mode='markers+text',
                marker=dict(
                    size=12,
                    color=status_colors.get(status, 'gray'),
                    symbol='circle'
                ),
                text=data['texts'],
                textposition='top center',
                textfont=dict(size=8, color='white'),
                name=f'Trains ({status})',
                hovertext=[f"Train {tid} - {status}" for tid in data['ids']]
            ))
