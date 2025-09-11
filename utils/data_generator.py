import pandas as pd
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

class TrainDataGenerator:
    """Generates and manages simulated train data"""
    
    def __init__(self):
        self.stations = ['Station A', 'Station B', 'Station C', 'Station D', 'Station E', 'Station F']
        self.trains = self._generate_initial_trains()
        
    def _generate_initial_trains(self) -> List[Dict[str, Any]]:
        """Generate initial set of trains"""
        train_types = ['Express', 'Freight', 'Local']
        statuses = ['On Time', 'Delayed', 'Waiting', 'Rerouted']
        priorities = ['High', 'Medium', 'Low']
        
        trains = []
        for i in range(12):  # Generate 12 trains
            train = {
                'train_id': f'T{1000 + i}',
                'type': random.choice(train_types),
                'priority': random.choice(priorities),
                'status': random.choice(statuses),
                'current_station': random.choice(self.stations),
                'destination': random.choice(self.stations),
                'delay_minutes': random.randint(0, 30) if random.random() > 0.6 else 0,
                'speed': random.uniform(40, 120),  # km/h
                'position': {
                    'lat': random.uniform(40.0, 40.2),
                    'lon': random.uniform(-74.1, -73.9)
                },
                'last_updated': datetime.now()
            }
            trains.append(train)
        
        return trains
    
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
                'Type': train['type'],
                'Priority': train['priority'],
                'Status': train['status'],
                'Current Station': train['current_station'],
                'Destination': train['destination'],
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
