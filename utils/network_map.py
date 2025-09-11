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
        """Define station positions"""
        return {
            'Station A': {'lat': 40.05, 'lon': -74.05},
            'Station B': {'lat': 40.08, 'lon': -74.02},
            'Station C': {'lat': 40.12, 'lon': -74.00},
            'Station D': {'lat': 40.15, 'lon': -73.97},
            'Station E': {'lat': 40.18, 'lon': -73.94},
            'Station F': {'lat': 40.21, 'lon': -73.91}
        }
    
    def _define_tracks(self) -> List[Dict[str, Any]]:
        """Define track segments between stations"""
        return [
            {'from': 'Station A', 'to': 'Station B', 'status': 'normal'},
            {'from': 'Station B', 'to': 'Station C', 'status': 'congested'},
            {'from': 'Station C', 'to': 'Station D', 'status': 'normal'},
            {'from': 'Station D', 'to': 'Station E', 'status': 'normal'},
            {'from': 'Station E', 'to': 'Station F', 'status': 'maintenance'},
            {'from': 'Station A', 'to': 'Station C', 'status': 'normal'},  # Alternative route
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
        
        # Configure layout
        fig.update_layout(
            title="Railway Network Status",
            showlegend=True,
            height=500,
            mapbox=dict(
                style="open-street-map",
                center=dict(lat=40.13, lon=-73.98),
                zoom=11
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
