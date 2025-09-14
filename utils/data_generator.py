import pandas as pd
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

class TrainDataGenerator:
    """Generates and manages simulated train data"""
    
    def __init__(self):
        self.stations = [
            'New Delhi', 'Mumbai Central', 'Chennai Central', 'Kolkata', 'Bangalore City', 'Hyderabad',
            'Vijayawada', 'Visakhapatnam', 'Tirupati', 'Guntur', 'Rajahmundry', 'Kurnool', 
            'Nellore', 'Kadapa', 'Anantapur'
        ]
        self.trains = self._generate_initial_trains()
        
    def _generate_initial_trains(self) -> List[Dict[str, Any]]:
        """Generate initial set of trains"""
        train_types = [
            'Rajdhani Express', 'Shatabdi Express', 'Mail Express', 'Passenger', 'Freight', 'Suburban',
            'Local Passenger', 'MEMU', 'DEMU', 'Intercity Express', 'Superfast Express', 'Garib Rath',
            'Duronto Express', 'Jan Shatabdi', 'Vande Bharat', 'Special Train'
        ]
        statuses = ['On Time', 'Delayed', 'Waiting', 'Rerouted']
        priorities = ['High', 'Medium', 'Low']
        
        # Define specific train routes for Andhra Pradesh and South India
        train_routes = [
            {'name': 'Visakhapatnam-Hyderabad Express', 'from': 'Visakhapatnam', 'to': 'Hyderabad', 'type': 'Mail Express'},
            {'name': 'Bangalore-Vijayawada Express', 'from': 'Bangalore City', 'to': 'Vijayawada', 'type': 'Intercity Express'},
            {'name': 'Chennai-Visakhapatnam Express', 'from': 'Chennai Central', 'to': 'Visakhapatnam', 'type': 'Superfast Express'},
            {'name': 'Hyderabad-Tirupati Passenger', 'from': 'Hyderabad', 'to': 'Tirupati', 'type': 'Passenger'},
            {'name': 'Vijayawada-Guntur Local', 'from': 'Vijayawada', 'to': 'Guntur', 'type': 'Local Passenger'},
            {'name': 'Bangalore-Kurnool MEMU', 'from': 'Bangalore City', 'to': 'Kurnool', 'type': 'MEMU'},
            {'name': 'Chennai-Nellore DEMU', 'from': 'Chennai Central', 'to': 'Nellore', 'type': 'DEMU'},
            {'name': 'Hyderabad-Rajahmundry Express', 'from': 'Hyderabad', 'to': 'Rajahmundry', 'type': 'Mail Express'},
            {'name': 'Tirupati-Kadapa Passenger', 'from': 'Tirupati', 'to': 'Kadapa', 'type': 'Passenger'},
            {'name': 'Anantapur-Bangalore Local', 'from': 'Anantapur', 'to': 'Bangalore City', 'type': 'Local Passenger'},
            {'name': 'Delhi-Chennai Rajdhani', 'from': 'New Delhi', 'to': 'Chennai Central', 'type': 'Rajdhani Express'},
            {'name': 'Mumbai-Hyderabad Express', 'from': 'Mumbai Central', 'to': 'Hyderabad', 'type': 'Superfast Express'},
            {'name': 'Kolkata-Visakhapatnam Express', 'from': 'Kolkata', 'to': 'Visakhapatnam', 'type': 'Mail Express'},
            {'name': 'Bangalore-Chennai Shatabdi', 'from': 'Bangalore City', 'to': 'Chennai Central', 'type': 'Shatabdi Express'},
            {'name': 'Hyderabad-Bangalore Vande Bharat', 'from': 'Hyderabad', 'to': 'Bangalore City', 'type': 'Vande Bharat'},
            {'name': 'Vijayawada-Visakhapatnam Garib Rath', 'from': 'Vijayawada', 'to': 'Visakhapatnam', 'type': 'Garib Rath'},
            {'name': 'Chennai-Tirupati Duronto', 'from': 'Chennai Central', 'to': 'Tirupati', 'type': 'Duronto Express'},
            {'name': 'Bangalore-Hyderabad Jan Shatabdi', 'from': 'Bangalore City', 'to': 'Hyderabad', 'type': 'Jan Shatabdi'},
            {'name': 'Guntur-Vijayawada Suburban', 'from': 'Guntur', 'to': 'Vijayawada', 'type': 'Suburban'},
            {'name': 'Nellore-Chennai Local', 'from': 'Nellore', 'to': 'Chennai Central', 'type': 'Local Passenger'},
            {'name': 'Kadapa-Tirupati MEMU', 'from': 'Kadapa', 'to': 'Tirupati', 'type': 'MEMU'},
            {'name': 'Kurnool-Anantapur DEMU', 'from': 'Kurnool', 'to': 'Anantapur', 'type': 'DEMU'},
            {'name': 'Rajahmundry-Visakhapatnam Express', 'from': 'Rajahmundry', 'to': 'Visakhapatnam', 'type': 'Mail Express'},
            {'name': 'Freight Train AP-001', 'from': 'Vijayawada', 'to': 'Hyderabad', 'type': 'Freight'},
            {'name': 'Special Train Festival', 'from': 'Tirupati', 'to': 'Chennai Central', 'type': 'Special Train'}
        ]
        
        trains = []
        for i, route in enumerate(train_routes):
            # Generate realistic positions based on route
            from_station = route['from']
            to_station = route['to']
            
            # Get station coordinates (simplified)
            station_coords = {
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
            
            from_coords = station_coords.get(from_station, {'lat': 16.0, 'lon': 80.0})
            to_coords = station_coords.get(to_station, {'lat': 16.0, 'lon': 80.0})
            
            # Position train somewhere between stations
            progress = random.uniform(0.1, 0.9)
            current_lat = from_coords['lat'] + (to_coords['lat'] - from_coords['lat']) * progress
            current_lon = from_coords['lon'] + (to_coords['lon'] - from_coords['lon']) * progress
            
            # Determine priority based on train type
            if route['type'] in ['Rajdhani Express', 'Shatabdi Express', 'Vande Bharat']:
                priority = 'High'
            elif route['type'] in ['Mail Express', 'Superfast Express', 'Intercity Express']:
                priority = 'Medium'
            else:
                priority = 'Low'
            
            # Determine speed based on train type
            if route['type'] in ['Rajdhani Express', 'Shatabdi Express', 'Vande Bharat']:
                speed = random.uniform(100, 130)
            elif route['type'] in ['Mail Express', 'Superfast Express']:
                speed = random.uniform(80, 110)
            elif route['type'] in ['Local Passenger', 'MEMU', 'DEMU', 'Suburban']:
                speed = random.uniform(30, 60)
            else:
                speed = random.uniform(50, 90)
            
            train = {
                'train_id': f'T{1000 + i}',
                'train_name': route['name'],
                'type': route['type'],
                'priority': priority,
                'status': random.choice(statuses),
                'current_station': from_station,
                'destination': to_station,
                'route': f"{from_station} → {to_station}",
                'delay_minutes': random.randint(0, 45) if random.random() > 0.7 else 0,
                'speed': speed,
                'coach_types': self._get_coach_types(route['type']),
                'platform': random.randint(1, 8),
                'position': {
                    'lat': current_lat,
                    'lon': current_lon
                },
                'last_updated': datetime.now()
            }
            trains.append(train)
        
        return trains
    
    def _get_coach_types(self, train_type: str) -> str:
        """Get coach types based on train type"""
        coach_mapping = {
            'Rajdhani Express': 'AC1, AC2, AC3',
            'Shatabdi Express': 'AC Chair Car, Executive Class',
            'Vande Bharat': 'AC Chair Car, Executive Class',
            'Mail Express': 'AC1, AC2, AC3, Sleeper, General',
            'Superfast Express': 'AC2, AC3, Sleeper, General',
            'Intercity Express': 'AC Chair Car, General',
            'Garib Rath': 'AC3, Sleeper',
            'Duronto Express': 'AC1, AC2, AC3, Sleeper',
            'Jan Shatabdi': 'AC Chair Car, General',
            'Passenger': 'Sleeper, General',
            'Local Passenger': 'General',
            'MEMU': 'General',
            'DEMU': 'General',
            'Suburban': 'General',
            'Freight': 'Goods',
            'Special Train': 'AC2, AC3, Sleeper, General'
        }
        return coach_mapping.get(train_type, 'General')
    
    def update_trains(self):
        """Update train positions and statuses"""
        for train in self.trains:
            # Randomly update some train properties
            if random.random() < 0.3:  # 30% chance to update status
                if train['status'] == 'Delayed' and random.random() < 0.4:
                    train['status'] = 'On Time'
                elif train['status'] == 'On Time' and random.random() < 0.1:
                    train['status'] = 'Delayed'
                    train['delay_minutes'] = random.randint(5, 20)
            
            # Update position slightly (simulate movement)
            train['position']['lat'] += random.uniform(-0.001, 0.001)
            train['position']['lon'] += random.uniform(-0.001, 0.001)
            
            # Update speed
            train['speed'] = max(20, min(120, train['speed'] + random.uniform(-5, 5)))
            
            train['last_updated'] = datetime.now()
    
    def get_trains_dataframe(self) -> pd.DataFrame:
        """Convert trains data to pandas DataFrame"""
        df_data = []
        for train in self.trains:
            df_data.append({
                'Train ID': train['train_id'],
                'Train Name': train.get('train_name', 'N/A'),
                'Type': train['type'],
                'Priority': train['priority'],
                'Status': train['status'],
                'Route': train.get('route', f"{train['current_station']} → {train['destination']}"),
                'Current Station': train['current_station'],
                'Destination': train['destination'],
                'Platform': train.get('platform', 'N/A'),
                'Coach Types': train.get('coach_types', 'General'),
                'Delay (min)': train['delay_minutes'],
                'Speed (km/h)': f"{train['speed']:.1f}",
                'Last Updated': train['last_updated'].strftime('%H:%M:%S')
            })
        
        return pd.DataFrame(df_data)
    
    def get_train_by_id(self, train_id: str) -> Dict[str, Any] | None:
        """Get specific train by ID"""
        for train in self.trains:
            if train['train_id'] == train_id:
                return train
        return None
    
    def inject_delay(self, train_id: str, delay_minutes: int):
        """Inject delay to a specific train"""
        train = self.get_train_by_id(train_id)
        if train:
            train['delay_minutes'] += delay_minutes
            train['status'] = 'Delayed'
    
    def simulate_breakdown(self, train_id: str):
        """Simulate breakdown for a specific train"""
        train = self.get_train_by_id(train_id)
        if train:
            train['status'] = 'Waiting'
            train['speed'] = 0
            train['delay_minutes'] += random.randint(15, 45)
