from typing import Dict, Any
from sqlalchemy.orm import Session
from api.services.recommendation_service import RecommendationService

class TrackingProcessor:
    def __init__(self, db: Session):
        self.db = db
        self.recommendation_service = RecommendationService(db)
    
    def process_tracking_events(self, events: list):
        """
        Process tracking events and extract interactions for recommendations
        """
        for event in events:
            if self._is_relevant_for_recommendations(event):
                self._extract_and_record_interaction(event)
    
    def _is_relevant_for_recommendations(self, event: Dict[str, Any]) -> bool:
        """
        Check if event is relevant for recommendation system
        """
        relevant_types = ['product_view', 'product_interest', 'click', 'time_spent']
        return event.get('type') in relevant_types and event.get('product', {}).get('id')
    
    def _extract_and_record_interaction(self, event: Dict[str, Any]):
        """
        Extract interaction data and record it
        """
        interaction_type = self._map_event_to_interaction(event)
        
        self.recommendation_service.record_interaction(
            user_id=event.get('userId'),
            fingerprint=event.get('fingerprint'),
            session_id=event.get('sessionId'),
            laptop_id=event.get('product', {}).get('id'),
            interaction_type=interaction_type
        )
    
    def _map_event_to_interaction(self, event: Dict[str, Any]) -> str:
        """
        Map tracking event types to interaction types
        """
        event_type = event.get('type')
        
        if event_type == 'product_view':
            return 'product_view'
        elif event_type == 'product_interest':
            return 'product_interest'
        elif event_type == 'click':
            action = event.get('action', '')
            if 'add_to_cart' in action:
                return 'add_to_cart'
            return 'click'
        elif event_type == 'time_spent':
            return 'time_spent'
        
        return 'view'  # default