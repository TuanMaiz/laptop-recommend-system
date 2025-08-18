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
        
    def get_hybrid_recommendations(
        self, 
        user_identifier: str, 
        limit: int = 10,
        collaborative_weight: float = 0.6,
        content_weight: float = 0.4
    ) -> List[Dict[str, Any]]:
        """
        Hybrid recommendation combining collaborative and content-based filtering
        """
        # Get collaborative filtering recommendations
        collaborative_scores = self._get_collaborative_recommendations(user_identifier)
        
        # Get content-based recommendations
        content_scores = self._get_content_based_recommendations(user_identifier)
        
        # Combine scores
        hybrid_scores = self._combine_scores(
            collaborative_scores, 
            content_scores, 
            collaborative_weight, 
            content_weight
        )
        
        # Get top recommendations
        top_laptop_ids = sorted(hybrid_scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        
        # Fetch laptop details
        laptop_ids = [laptop_id for laptop_id, _ in top_laptop_ids]
        laptops = self.db.query(Laptop).filter(Laptop.id.in_(laptop_ids)).all()
        
        # Create response with scores
        recommendations = []
        for laptop in laptops:
            score = hybrid_scores.get(laptop.id, 0)
            recommendations.append({
                "laptop": laptop,
                "recommendation_score": round(score, 3),
                "reason": self._get_recommendation_reason(laptop.id, collaborative_scores, content_scores)
            })
        
        return sorted(recommendations, key=lambda x: x["recommendation_score"], reverse=True)
    
    def _get_collaborative_recommendations(self, user_identifier: str) -> Dict[str, float]:
        """
        Collaborative filtering based on user interactions
        """
        # Define interaction weights
        interaction_weights = {
            'product_view': 1.0,
            'click': 1.5,
            'add_to_cart': 3.0,
            'time_spent': 2.0,
            'product_interest': 2.5
        }
        
        # Get user's interaction history
        user_interactions = self.db.execute(text("""
            SELECT laptop_id, interaction_type, COUNT(*) as frequency
            FROM user_interactions 
            WHERE user_id = :user_id OR fingerprint = :fingerprint
            GROUP BY laptop_id, interaction_type
        """), {"user_id": user_identifier, "fingerprint": user_identifier}).fetchall()
        
        if not user_interactions:
            return {}
        
        # Build user profile
        user_laptop_scores = defaultdict(float)
        for interaction in user_interactions:
            weight = interaction_weights.get(interaction.interaction_type, 1.0)
            user_laptop_scores[interaction.laptop_id] += weight * interaction.frequency
        
        # Find similar users
        similar_users = self._find_similar_users(user_identifier, user_laptop_scores)
        
        # Generate recommendations based on similar users
        recommendations = defaultdict(float)
        for similar_user, similarity in similar_users:
            similar_user_interactions = self.db.execute(text("""
                SELECT laptop_id, interaction_type, COUNT(*) as frequency
                FROM user_interactions 
                WHERE (user_id = :similar_user OR fingerprint = :similar_user)
                AND laptop_id NOT IN :user_laptops
                GROUP BY laptop_id, interaction_type
            """), {
                "similar_user": similar_user,
                "user_laptops": tuple(user_laptop_scores.keys()) if user_laptop_scores else ('',)
            }).fetchall()
            
            for interaction in similar_user_interactions:
                weight = interaction_weights.get(interaction.interaction_type, 1.0)
                recommendations[interaction.laptop_id] += similarity * weight * interaction.frequency
        
        return dict(recommendations)
    
    def _get_content_based_recommendations(self, user_identifier: str) -> Dict[str, float]:
        """
        Content-based filtering using laptop features and user preferences
        """
        # Get user preferences from interaction history
        user_prefs = self._extract_user_preferences(user_identifier)
        
        if not user_prefs:
            return {}
        
        # Get all laptops
        laptops = self.db.query(Laptop).all()
        
        recommendations = {}
        for laptop in laptops:
            score = self._calculate_content_similarity(laptop, user_prefs)
            if score > 0:
                recommendations[laptop.id] = score
        
        return recommendations
    
    def _extract_user_preferences(self, user_identifier: str) -> Dict[str, Any]:
        """
        Extract user preferences from interaction history
        """
        # Get laptops user has interacted with
        interacted_laptops = self.db.execute(text("""
            SELECT l.*, ui.interaction_type, COUNT(*) as frequency
            FROM laptops l
            JOIN user_interactions ui ON l.id = ui.laptop_id
            WHERE ui.user_id = :user_id OR ui.fingerprint = :fingerprint
            GROUP BY l.id, ui.interaction_type
            ORDER BY frequency DESC
        """), {"user_id": user_identifier, "fingerprint": user_identifier}).fetchall()
        
        if not interacted_laptops:
            return {}
        
        # Extract preferences
        brands = Counter()
        price_ranges = []
        categories = Counter()
        
        for laptop in interacted_laptops:
            brands[laptop.brand] += laptop.frequency
            price_ranges.append(float(laptop.price))
            if hasattr(laptop, 'category') and laptop.category:
                categories[laptop.category] += laptop.frequency
        
        return {
            "preferred_brands": dict(brands.most_common(3)),
            "price_range": {
                "min": min(price_ranges) * 0.8 if price_ranges else 0,
                "max": max(price_ranges) * 1.2 if price_ranges else float('inf')
            },
            "preferred_categories": dict(categories.most_common(2))
        }
    
    def _calculate_content_similarity(self, laptop: Laptop, user_prefs: Dict[str, Any]) -> float:
        """
        Calculate content-based similarity score
        """
        score = 0.0
        
        # Brand preference
        if laptop.brand in user_prefs.get("preferred_brands", {}):
            brand_score = user_prefs["preferred_brands"][laptop.brand]
            score += brand_score * 0.3
        
        # Price range preference
        price_range = user_prefs.get("price_range", {})
        laptop_price = float(laptop.price)
        if price_range.get("min", 0) <= laptop_price <= price_range.get("max", float('inf')):
            score += 2.0
        
        # Category preference (if available)
        if hasattr(laptop, 'category') and laptop.category:
            if laptop.category in user_prefs.get("preferred_categories", {}):
                category_score = user_prefs["preferred_categories"][laptop.category]
                score += category_score * 0.2
        
        return score
    
    def _find_similar_users(self, user_identifier: str, user_scores: Dict[str, float]) -> List[Tuple[str, float]]:
        """
        Find users with similar interaction patterns
        """
        # Get all other users and their interactions
        other_users = self.db.execute(text("""
            SELECT COALESCE(user_id, fingerprint) as user_id, laptop_id, 
                   SUM(CASE 
                       WHEN interaction_type = 'add_to_cart' THEN 3.0
                       WHEN interaction_type = 'product_interest' THEN 2.5
                       WHEN interaction_type = 'time_spent' THEN 2.0
                       WHEN interaction_type = 'click' THEN 1.5
                       ELSE 1.0
                   END) as score
            FROM user_interactions
            WHERE COALESCE(user_id, fingerprint) != :user_id
            GROUP BY COALESCE(user_id, fingerprint), laptop_id
        """), {"user_id": user_identifier}).fetchall()
        
        # Group by user
        user_profiles = defaultdict(dict)
        for row in other_users:
            user_profiles[row.user_id][row.laptop_id] = row.score
        
        # Calculate similarity using cosine similarity
        similarities = []
        for other_user, other_scores in user_profiles.items():
            similarity = self._cosine_similarity(user_scores, other_scores)
            if similarity > 0.1:  # Minimum similarity threshold
                similarities.append((other_user, similarity))
        
        return sorted(similarities, key=lambda x: x[1], reverse=True)[:10]
    
    def _cosine_similarity(self, scores1: Dict[str, float], scores2: Dict[str, float]) -> float:
        """
        Calculate cosine similarity between two score dictionaries
        """
        common_items = set(scores1.keys()) & set(scores2.keys())
        if not common_items:
            return 0.0
        
        sum_xx = sum(scores1[item] ** 2 for item in common_items)
        sum_yy = sum(scores2[item] ** 2 for item in common_items)
        sum_xy = sum(scores1[item] * scores2[item] for item in common_items)
        
        if sum_xx == 0 or sum_yy == 0:
            return 0.0
        
        return sum_xy / (sum_xx ** 0.5 * sum_yy ** 0.5)
    
    def _combine_scores(
        self, 
        collaborative: Dict[str, float], 
        content: Dict[str, float], 
        collab_weight: float, 
        content_weight: float
    ) -> Dict[str, float]:
        """
        Combine collaborative and content-based scores
        """
        all_laptops = set(collaborative.keys()) | set(content.keys())
        combined = {}
        
        for laptop_id in all_laptops:
            collab_score = collaborative.get(laptop_id, 0)
            content_score = content.get(laptop_id, 0)
            
            # Normalize scores (simple min-max normalization)
            if collaborative:
                max_collab = max(collaborative.values())
                collab_score = collab_score / max_collab if max_collab > 0 else 0
            
            if content:
                max_content = max(content.values())
                content_score = content_score / max_content if max_content > 0 else 0
            
            combined[laptop_id] = (collab_score * collab_weight) + (content_score * content_weight)
        
        return combined
    
    def _get_recommendation_reason(
        self, 
        laptop_id: str, 
        collaborative: Dict[str, float], 
        content: Dict[str, float]
    ) -> str:
        """
        Generate explanation for recommendation
        """
        reasons = []
        
        if laptop_id in collaborative and collaborative[laptop_id] > 0:
            reasons.append("Users with similar preferences also liked this")
        
        if laptop_id in content and content[laptop_id] > 0:
            reasons.append("Matches your browsing preferences")
        
        return "; ".join(reasons) if reasons else "Popular choice"

    def record_interaction(
        self,
        timestamp: str,
        url: str,
        user_id: Optional[str],
        session_id: str,
        fingerprint: str,
        event_type: str,
        data: Dict[str, Any]
    ):
        """
        Record user interaction for future recommendations
        """

        # Insert to track_events table
        self.db.execute(text("""
            INSERT INTO public.track_events (id, timestamp, url, user_id, session_id, fingerprint, event_type, data)
            VALUES (:id, :timestamp, :url, :user_id, :session_id, :fingerprint, :event_type, :data)
        """), {
            "id": str(uuid.uuid4()),
            "timestamp": timestamp,
            "url": url,
            "user_id": user_id,
            "session_id": session_id,
            "fingerprint": fingerprint,
            "event_type": event_type,
            "data": str(data)
        })
        self.db.commit()