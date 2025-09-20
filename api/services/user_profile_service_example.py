"""
Example usage of the UserProfileNeo4j service
This demonstrates how to use the user profile system in practice
"""

from neo4j import GraphDatabase
from api.services.user_profile_service import UserProfileNeo4j
from api.services.fingerprint_utils import FingerprintManager


class UserProfileService:
    """Wrapper service that integrates with your existing FastAPI application"""
    
    def __init__(self, neo4j_driver: GraphDatabase.driver):
        self.profile_service = UserProfileNeo4j(neo4j_driver)
    
    def get_or_create_profile(self, fingerprint: str, main_use: str = None, price_range: str = None):
        """Get existing profile or create new one"""
        if not self.profile_service.profile_exists(fingerprint):
            self.profile_service.create_profile(fingerprint, main_use, price_range)
        
        return self.profile_service.get_all_preferences(fingerprint)
    
    def process_user_feedback(self, fingerprint: str, product_ratings: Dict[str, int]):
        """Process user ratings and update profile"""
        # Update profile with feedback
        self.profile_service.update_from_feedback(fingerprint, product_ratings)
        
        # Apply spreading activation to propagate preferences
        self.profile_service.spread_activation(fingerprint)
        
        # Get updated profile
        return self.profile_service.get_all_preferences(fingerprint)
    
    def get_recommendation_profile(self, fingerprint: str):
        """Get profile in vector format for recommendation generation"""
        return self.profile_service.get_profile_vector(fingerprint)
    
    def get_user_preferences_summary(self, fingerprint: str):
        """Get user preferences in a human-readable format"""
        top_prefs = self.profile_service.get_top_preferences(fingerprint, top_n=5)
        functionality_prefs = self.profile_service.get_functionality_preferences(fingerprint)
        spec_prefs = self.profile_service.get_specification_preferences(fingerprint)
        
        return {
            "top_preferences": top_prefs,
            "functionality_preferences": functionality_prefs,
            "specification_preferences": spec_prefs,
            "profile_vector": self.profile_service.get_profile_vector(fingerprint)
        }


# Example usage:
if __name__ == "__main__":
    # Initialize Neo4j driver (you should configure this in your settings)
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
    
    # Create profile service
    user_service = UserProfileService(driver)
    
    # Example: External fingerprint would come from your application (e.g., browser fingerprint, device ID)
    external_fingerprint = "browser_fingerprint_xyz_123"  # This comes from outside the system
    
    # Example: Create or get user profile using external fingerprint
    profile = user_service.get_or_create_profile(
        external_fingerprint, 
        main_use="gaming", 
        price_range="mid"
    )
    
    print("Initial profile created:", profile)
    
    # Example: Process user feedback with external fingerprint
    ratings = {
        "laptop_1": 5,  # User loves this gaming laptop
        "laptop_2": 2,  # User dislikes this laptop
        "laptop_3": 4   # User likes this laptop
    }
    
    updated_profile = user_service.process_user_feedback(external_fingerprint, ratings)
    print("Profile after feedback:", updated_profile)
    
    # Example: Get profile for recommendations using external fingerprint
    recommendation_vector = user_service.get_recommendation_profile(external_fingerprint)
    print("Profile vector for recommendations:", recommendation_vector)
    
    # Example: Get user preferences summary using external fingerprint
    preferences_summary = user_service.get_user_preferences_summary(external_fingerprint)
    print("User preferences summary:", preferences_summary)
    
    # Close driver
    driver.close()


# Example: Integration with FastAPI endpoints
def fastapi_integration_example():
    """Example of how to integrate with FastAPI endpoints"""
    
    def create_profile_endpoint(request_data: Dict):
        """Example FastAPI endpoint for creating user profile"""
        # External fingerprint comes from request header or cookies
        external_fingerprint = request_data.get("fingerprint")
        main_use = request_data.get("main_use")
        price_range = request_data.get("price_range")
        
        try:
            profile = user_service.get_or_create_profile(
                external_fingerprint, 
                main_use, 
                price_range
            )
            return {"success": True, "profile": profile}
        except ValueError as e:
            return {"success": False, "error": str(e)}
    
    def feedback_endpoint(request_data: Dict):
        """Example FastAPI endpoint for processing user feedback"""
        # External fingerprint comes from request header or cookies
        external_fingerprint = request_data.get("fingerprint")
        ratings = request_data.get("ratings", {})
        
        try:
            updated_profile = user_service.process_user_feedback(
                external_fingerprint, 
                ratings
            )
            return {"success": True, "profile": updated_profile}
        except ValueError as e:
            return {"success": False, "error": str(e)}
    
    def get_recommendation_profile_endpoint(request_data: Dict):
        """Example FastAPI endpoint for getting recommendation profile"""
        # External fingerprint comes from request header or cookies
        external_fingerprint = request_data.get("fingerprint")
        
        try:
            profile_vector = user_service.get_recommendation_profile(
                external_fingerprint
            )
            return {"success": True, "profile_vector": profile_vector}
        except ValueError as e:
            return {"success": False, "error": str(e)}
    
    return {
        "create_profile": create_profile_endpoint,
        "process_feedback": feedback_endpoint,
        "get_recommendation_profile": get_recommendation_profile_endpoint
    }