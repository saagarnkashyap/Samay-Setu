import random
from datetime import datetime
from typing import List, Dict, Any

class TrainController:
    """Handles train control operations and decision making"""
    
    def __init__(self):
        self.decision_history = []
    
    def calculate_metrics(self, trains: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate system performance metrics"""
        if not trains:
            return {'avg_delay': 0, 'throughput': 0, 'utilization': 0}
        
        # Calculate average delay
        total_delay = sum(train['delay_minutes'] for train in trains)
        avg_delay = total_delay / len(trains)
        
        # Calculate throughput (trains per hour - simulated)
        # In a real system, this would be based on actual throughput data
        throughput = random.uniform(15, 25)
        
        # Calculate utilization (percentage of track capacity used)
        on_time_trains = len([t for t in trains if t['status'] == 'On Time'])
        utilization = (len(trains) / 20) * 100  # Assuming max capacity of 20 trains
        
        return {
            'avg_delay': avg_delay,
            'throughput': throughput,
            'utilization': min(100, utilization)
        }
    
    def generate_recommendations(self, trains: List[Dict[str, Any]]) -> List[Dict[str, str]]:
        """Generate AI-powered recommendations for train management"""
        recommendations = []
        
        # Find problematic trains
        delayed_trains = [t for t in trains if t['status'] == 'Delayed']
        waiting_trains = [t for t in trains if t['status'] == 'Waiting']
        express_trains = [t for t in trains if t['type'] in ['Rajdhani Express', 'Shatabdi Express', 'Vande Bharat', 'Duronto Express']]
        
        # Generate recommendations based on current situation
        if delayed_trains:
            train = random.choice(delayed_trains)
            recommendations.append({
                'action': f'Reroute {train["train_id"]} via alternative track to reduce delay',
                'reason': f'Train is delayed by {train["delay_minutes"]} minutes',
                'priority': 'High' if train['type'] in ['Rajdhani Express', 'Shatabdi Express', 'Vande Bharat', 'Duronto Express'] else 'Medium'
            })
        
        if waiting_trains:
            train = random.choice(waiting_trains)
            recommendations.append({
                'action': f'Dispatch maintenance crew to {train["current_station"]} for {train["train_id"]}',
                'reason': 'Train is waiting due to technical issues',
                'priority': 'High'
            })
        
        if express_trains:
            train = random.choice(express_trains)
            recommendations.append({
                'action': f'Give priority clearance to {train["train_id"]} ({train.get("train_name", "Express")}) on congested route',
                'reason': 'Premium train approaching congested section',
                'priority': 'High'
            })
        
        # Always provide some general recommendations
        general_recommendations = [
            {
                'action': 'Reduce speed limit on Mumbai-Chennai route to 80 km/h',
                'reason': 'High traffic density detected in this section',
                'priority': 'Medium'
            },
            {
                'action': 'Prepare Platform 1 at Chennai Central for Rajdhani arrival',
                'reason': 'Multiple express trains scheduled within next hour',
                'priority': 'Low'
            },
            {
                'action': 'Alert passengers about potential delays on Freight routes',
                'reason': 'Monsoon conditions may affect freight operations',
                'priority': 'Low'
            },
            {
                'action': 'Clear Platform 3 at Vijayawada for MEMU arrival',
                'reason': 'Local train approaching with high passenger load',
                'priority': 'Medium'
            },
            {
                'action': 'Coordinate with Hyderabad station for Vande Bharat priority',
                'reason': 'Premium train requires special handling',
                'priority': 'High'
            }
        ]
        
        recommendations.extend(random.sample(general_recommendations, 2))
        
        return recommendations[:5]  # Return top 5 recommendations
    
    def inject_delay(self, trains: List[Dict[str, Any]]):
        """Inject random delay to a random train"""
        if trains:
            train = random.choice(trains)
            additional_delay = random.randint(10, 30)
            train['delay_minutes'] += additional_delay
            train['status'] = 'Delayed'
            
            self.decision_history.append({
                'timestamp': datetime.now(),
                'action': f'Delay injected to {train["train_id"]} (+{additional_delay} min)',
                'type': 'system_action'
            })
    
    def simulate_breakdown(self, trains: List[Dict[str, Any]]):
        """Simulate breakdown for a random train"""
        if trains:
            # Prefer trains that are currently moving
            moving_trains = [t for t in trains if t['status'] in ['On Time', 'Delayed']]
            target_trains = moving_trains if moving_trains else trains
            
            train = random.choice(target_trains)
            train['status'] = 'Waiting'
            train['speed'] = 0
            breakdown_delay = random.randint(20, 60)
            train['delay_minutes'] += breakdown_delay
            
            self.decision_history.append({
                'timestamp': datetime.now(),
                'action': f'Breakdown simulated for {train["train_id"]} (+{breakdown_delay} min)',
                'type': 'system_action'
            })
    
    def apply_recommendation(self, recommendation: Dict[str, str]):
        """Apply a recommended action"""
        self.decision_history.append({
            'timestamp': datetime.now(),
            'action': recommendation['action'],
            'type': 'recommendation_applied'
        })
    
    def get_decision_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent decision history"""
        return self.decision_history[-limit:] if self.decision_history else []
