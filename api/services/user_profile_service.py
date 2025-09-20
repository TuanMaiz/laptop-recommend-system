from typing import Dict, List, Optional
from neo4j import Driver, GraphDatabase
import hashlib
import datetime
from dataclasses import dataclass


@dataclass
class Preference:
    spec: str
    preference: float
    confidence: float
    updated_at: datetime.datetime


class UserProfileNeo4j:
    def __init__(self, driver: Driver):
        self.driver = driver
        self.specification_order = [
            "cpu", "ram", "screen_size", "refresh_rate", "resolution",
            "brightness", "storage", "weight", "battery", "brand", "price"
        ]
        self.functionality_order = ["graphic", "gaming", "office"]
        self.relationships = {
            "cpu": ["gaming", "performance"],
            "ram": ["gaming", "multitasking", "office"],
            "screen_size": ["portability", "viewing_experience"],
            "refresh_rate": ["gaming", "smoothness"],
            "battery": ["portability", "office_use"],
            "storage": ["multitasking", "content_creation"],
            "weight": ["portability"],
            "brand": ["reliability", "support"],
            "price": ["value", "budget"]
        }
    
    def _validate_fingerprint(self, fingerprint: str) -> str:
        """Validate and return the raw fingerprint"""
        if not fingerprint or not isinstance(fingerprint, str):
            raise ValueError("Fingerprint must be a non-empty string")
        return fingerprint.strip()
    
    def create_profile(self, fingerprint: str, main_use: Optional[str] = None, price_range: Optional[str] = None):
        """Create initial user profile with fingerprint identification"""
        validated_fingerprint = self._validate_fingerprint(fingerprint)
        
        with self.driver.session() as session:
            # Create user and profile nodes if they don't exist
            session.run("""
                MERGE (u:User {fingerprint: $fingerprint})
                ON CREATE SET u.created_at = datetime()
                CREATE (up:UserProfile {fingerprint: $fingerprint})
                CREATE (u)-[:HAS_PROFILE]->(up)
            """, fingerprint=validated_fingerprint)
            
            # Initialize all specifications with neutral values
            for spec in self.specification_order:
                session.run("""
                    MATCH (up:UserProfile {fingerprint: $fingerprint})
                    MERGE (p:Preference {spec: $spec})
                    ON CREATE SET p.preference = 0.5,
                               p.confidence = 0.2,
                               p.created_at = datetime(),
                               p.updated_at = datetime()
                    MERGE (up)-[:HAS_PREFERENCE]->(p)
                """, fingerprint=validated_fingerprint, spec=spec)
            
            # Set initial functionality preferences based on main use
            if main_use and main_use in self.functionality_order:
                session.run("""
                    MATCH (up:UserProfile {fingerprint: $fingerprint})
                    MERGE (p:Preference {spec: $spec})
                    ON CREATE SET p.preference = 0.8,
                               p.confidence = 1.0,
                               p.created_at = datetime(),
                               p.updated_at = datetime()
                    MERGE (up)-[:HAS_PREFERENCE]->(p)
                """, fingerprint=validated_fingerprint, spec=main_use)
            
            # Set price range preference
            if price_range:
                price_mapping = {
                    "budget": {"preference": 0.8, "confidence": 1.0},
                    "mid": {"preference": 0.5, "confidence": 1.0},
                    "premium": {"preference": 0.2, "confidence": 1.0}
                }
                if price_range in price_mapping:
                    session.run("""
                        MATCH (up:UserProfile {fingerprint: $fingerprint})
                        MERGE (p:Preference {spec: $spec})
                        ON CREATE SET p.preference = $preference,
                                   p.confidence = $confidence,
                                   p.created_at = datetime(),
                                   p.updated_at = datetime()
                        MERGE (up)-[:HAS_PREFERENCE]->(p)
                    """, fingerprint=validated_fingerprint, spec="price",
                         preference=price_mapping[price_range]["preference"],
                         confidence=price_mapping[price_range]["confidence"])
    
    def update_preference(self, fingerprint: str, spec_name: str, new_preference: float, confidence: float = 1.0):
        """Update a specific preference for a user"""
        validated_fingerprint = self._validate_fingerprint(fingerprint)
        
        with self.driver.session() as session:
            session.run("""
                MATCH (up:UserProfile {fingerprint: $fingerprint})
                MERGE (p:Preference {spec: $spec})
                ON CREATE SET p.preference = $preference,
                           p.confidence = $confidence,
                           p.created_at = datetime(),
                           p.updated_at = datetime()
                ON MATCH SET p.preference = $preference,
                           p.confidence = $confidence,
                           p.updated_at = datetime()
                MERGE (up)-[:HAS_PREFERENCE]->(p)
            """, fingerprint=validated_fingerprint, spec=spec_name,
                  preference=new_preference, confidence=confidence)
    
    def update_from_feedback(self, fingerprint: str, product_ratings: Dict[str, int]):
        """Update profile based on user ratings for products"""
        validated_fingerprint = self._validate_fingerprint(fingerprint)
        
        # This would require product specifications from your ontology/database
        # For now, let's create a simplified version that updates based on ratings
        with self.driver.session() as session:
            for product_id, rating in product_ratings.items():
                # Convert 1-5 rating to 0-1 scale
                normalized_rating = (rating - 1) / 4.0
                
                # Get product specifications (this would be connected to your laptop ontology)
                product_specs = self._get_product_specs(product_id)
                
                if product_specs:
                    # Update preferences based on product specs and rating
                    for spec_name, spec_value in product_specs.items():
                        if spec_name in self.specification_order:
                            self._update_spec_preference(
                                validated_fingerprint, spec_name, normalized_rating
                            )
    
    def _get_product_specs(self, product_id: str) -> Dict[str, any]:
        """Get product specifications - would be connected to your laptop ontology"""
        # This is a placeholder - in real implementation, you'd query your laptop database
        # For now, return some mock specs
        mock_specs = {
            "laptop_1": {"cpu": "high", "ram": "16gb", "price": "mid"},
            "laptop_2": {"cpu": "low", "ram": "8gb", "price": "budget"},
            "laptop_3": {"cpu": "high", "ram": "32gb", "price": "premium"}
        }
        return mock_specs.get(product_id, {})
    
    def _update_spec_preference(self, fingerprint: str, spec_name: str, rating: float):
        """Update a specific preference with learning parameters"""
        validated_fingerprint = self._validate_fingerprint(fingerprint)
        
        with self.driver.session() as session:
            session.run("""
                MATCH (up:UserProfile {fingerprint: $fingerprint})
                MATCH (up)-[:HAS_PREFERENCE]->(p:Preference {spec: $spec})
                
                // Learning parameters
                SET p.preference = 0.7 * p.preference + 0.3 * $rating
                SET p.confidence = min(1.0, p.confidence + 0.1)
                SET p.updated_at = datetime()
                
                // Ensure bounds
                SET p.preference = min(1.0, max(0.0, p.preference))
            """, fingerprint=validated_fingerprint, spec=spec_name, rating=rating)
    
    def spread_activation(self, fingerprint: str, max_depth: int = 2):
        """Apply spreading activation to propagate preferences through relationships"""
        validated_fingerprint = self._validate_fingerprint(fingerprint)
        
        with self.driver.session() as session:
            # Get all preferences for user
            result = session.run("""
                MATCH (up:UserProfile {fingerprint: $fingerprint})-[:HAS_PREFERENCE]->(p:Preference)
                RETURN p.spec as spec, p.preference as pref, p.confidence as conf
            """, fingerprint=validated_fingerprint)
            
            # For each preference, spread to related specifications
            for record in result:
                spec = record["spec"]
                pref = record["pref"]
                conf = record["conf"]
                
                if spec in self.relationships:
                    # Get related specifications and update them
                    for related_spec in self.relationships[spec]:
                        if related_spec in self.specification_order:
                            # Calculate propagation strength
                            propagation_strength = conf * pref * 0.1
                            
                            session.run("""
                                MATCH (up:UserProfile {fingerprint: $fingerprint})
                                MATCH (up)-[:HAS_PREFERENCE]->(p1:Preference {spec: $source})
                                MATCH (up)-[:HAS_PREFERENCE]->(p2:Preference {spec: $target})
                                
                                // Apply spreading activation
                                SET p2.preference = p2.preference + $strength
                                SET p2.confidence = min(1.0, p2.confidence + 0.05)
                                SET p2.updated_at = datetime()
                                
                                // Ensure bounds
                                SET p2.preference = min(1.0, max(0.0, p2.preference))
                            """, fingerprint=validated_fingerprint, source=spec, target=related_spec,
                                 strength=propagation_strength)
    
    def get_profile_vector(self, fingerprint: str) -> List[float]:
        """Get profile as vector for similarity calculations"""
        validated_fingerprint = self._validate_fingerprint(fingerprint)
        
        with self.driver.session() as session:
            result = session.run("""
                MATCH (up:UserProfile {fingerprint: $fingerprint})-[:HAS_PREFERENCE]->(p:Preference)
                RETURN p.spec as spec, p.preference as preference
                ORDER BY p.spec
            """, fingerprint=validated_fingerprint)
            
            # Create vector in consistent order
            vector = []
            for spec in self.specification_order + self.functionality_order:
                pref = 0.5  # Default neutral value
                for record in result:
                    if record["spec"] == spec:
                        pref = record["preference"]
                        break
                vector.append(pref)
            
            return vector
    
    def get_top_preferences(self, fingerprint: str, top_n: int = 5) -> List[Dict]:
        """Get user's top N preferences"""
        validated_fingerprint = self._validate_fingerprint(fingerprint)
        
        with self.driver.session() as session:
            result = session.run("""
                MATCH (up:UserProfile {fingerprint: $fingerprint})-[:HAS_PREFERENCE]->(p:Preference)
                RETURN p.spec as spec, p.preference as preference, p.confidence as confidence
                ORDER BY p.preference DESC
                LIMIT $top_n
            """, fingerprint=validated_fingerprint, top_n=top_n)
            
            return [dict(record) for record in result]
    
    def get_functionality_preferences(self, fingerprint: str) -> Dict[str, float]:
        """Get functionality-based preferences"""
        validated_fingerprint = self._validate_fingerprint(fingerprint)
        
        with self.driver.session() as session:
            result = session.run("""
                MATCH (up:UserProfile {fingerprint: $fingerprint})-[:HAS_PREFERENCE]->(p:Preference)
                WHERE p.spec IN $specs
                RETURN p.spec as spec, p.preference as preference
            """, fingerprint=validated_fingerprint, specs=self.functionality_order)
            
            return {record["spec"]: record["preference"] for record in result}
    
    def get_specification_preferences(self, fingerprint: str) -> Dict[str, float]:
        """Get specification-based preferences"""
        validated_fingerprint = self._validate_fingerprint(fingerprint)
        
        with self.driver.session() as session:
            result = session.run("""
                MATCH (up:UserProfile {fingerprint: $fingerprint})-[:HAS_PREFERENCE]->(p:Preference)
                WHERE p.spec IN $specs
                RETURN p.spec as spec, p.preference as preference
            """, fingerprint=validated_fingerprint, specs=self.specification_order)
            
            return {record["spec"]: record["preference"] for record in result}
    
    def profile_exists(self, fingerprint: str) -> bool:
        """Check if user profile exists"""
        validated_fingerprint = self._validate_fingerprint(fingerprint)
        
        with self.driver.session() as session:
            result = session.run("""
                MATCH (u:User {fingerprint: $fingerprint})
                RETURN count(u) > 0 as exists
            """, fingerprint=validated_fingerprint)
            
            return result.single()["exists"]
    
    def get_all_preferences(self, fingerprint: str) -> Dict[str, Dict]:
        """Get all preferences for user"""
        validated_fingerprint = self._validate_fingerprint(fingerprint)
        
        with self.driver.session() as session:
            result = session.run("""
                MATCH (up:UserProfile {fingerprint: $fingerprint})-[:HAS_PREFERENCE]->(p:Preference)
                RETURN p.spec as spec, p.preference as preference, p.confidence as confidence, p.updated_at as updated_at
            """, fingerprint=validated_fingerprint)
            
            preferences = {}
            for record in result:
                preferences[record["spec"]] = {
                    "preference": record["preference"],
                    "confidence": record["confidence"],
                    "updated_at": record["updated_at"]
                }
            
            return preferences