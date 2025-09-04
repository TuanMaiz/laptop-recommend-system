import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import text, func, and_
from api.db.models.laptop_model import Laptop
import json
from collections import defaultdict, Counter
import uuid

class RecommendationService:
    def __init__(self, db: Session):
        self.db = db

    def initialize_fingerprint(self, fingerprint: str, user_id: Optional[str] = None) -> bool:
        """
        Initialize a fingerprint (and optionally user) in Neo4j.
        If new, attach ontology-based neutral profile (weight=0.0, confidence=0.0).
        Returns True if fingerprint already existed, False if newly created.
        """
        # Create Fingerprint (and User if provided)
        if user_id:
            query = """
            MERGE (f:Fingerprint {id:$fingerprint})
            MERGE (u:User {id:$user_id})
            MERGE (u)-[:IDENTIFIED_BY]->(f)
            ON CREATE SET f.created_at = timestamp()
            ON MATCH SET f.last_seen = timestamp()
            RETURN f
            """
            record = self.db.run(query, fingerprint=fingerprint, user_id=user_id).single()
        else:
            query = """
            MERGE (f:Fingerprint {id:$fingerprint})
            ON CREATE SET f.created_at = timestamp()
            ON MATCH SET f.last_seen = timestamp()
            RETURN f
            """
            record = self.db.run(query, fingerprint=fingerprint).single()

        created = record is not None and "created_at" in record.get("f", {})

        # Attach ontology-based neutral prefs if new
        if not created:
            return True  # fingerprint already existed

        # Example: only initializing Functionality prefs here
        query_prefs = """
        MERGE (f:Fingerprint {id:$fingerprint})
        WITH f
        UNWIND ["Gaming", "Office", "Graphic"] AS func
        MERGE (ff:Functionality {name:func})
        MERGE (f)-[r:PREFERS]->(ff)
        ON CREATE SET r.weight = 0.0, r.confidence = 0.0
        """
        self.db.run(query_prefs, fingerprint=fingerprint)
        return False  # fingerprint initialized fresh 
    
    def update_tracking_graph_by_fingerprint(self, fingerprint: str, interactions: List[Dict[str, Any]]) -> None:
        """
        Update the tracking graph in Neo4j with user interactions based on the fingerprint.
        Each interaction is represented as a relationship with relevant properties.
        """
        pass

    def record_interaction_to_sql(
        self,
        timestamp: str,
        url: str,
        user_id: Optional[str],
        session_id: str,
        fingerprint: str,
        event_type: str,
        ip_address: str,
        user_agent: str,
        device_info: Dict[str, Any],
        data: Dict[str, Any]
    ):
        """
        Record user interaction for future recommendations
        """

        # Insert to track_events table
        self.db.execute(text("""
            INSERT INTO public.tracking_events (id, timestamp, page_url, user_id, session_id, fingerprint, event_type, event_data, ip_address, user_agent, device_info)
            VALUES (:id, :timestamp, :page_url, :user_id, :session_id, :fingerprint, :event_type, :event_data, :ip_address, :user_agent, :device_info)
        """), {
            "id": str(uuid.uuid4()),
            "timestamp": timestamp,
            "page_url": url,
            "user_id": user_id,
            "session_id": session_id,
            "fingerprint": fingerprint,
            "event_type": event_type,
            "event_data": json.dumps(data) if data else None,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "device_info": json.dumps(device_info) if device_info else None
        })
        self.db.commit()