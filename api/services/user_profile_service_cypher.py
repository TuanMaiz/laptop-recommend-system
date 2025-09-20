"""
Cypher queries for setting up the Neo4j user profile database
Run these scripts to initialize the database structure
"""

# 1. Create constraints for data integrity
"""
CREATE CONSTRAINT IF NOT EXISTS FOR (u:User) REQUIRE u.fingerprint IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (up:UserProfile) REQUIRE up.fingerprint IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (p:Preference) REQUIRE p.spec IS UNIQUE;
"""

# 2. Create example relationships between specifications
"""
// CPU relationships
MATCH (p1:Preference {spec: 'cpu'})
MATCH (p2:Preference {spec: 'gaming'})
MERGE (p1)-[:RELATED_TO {weight: 0.7, relationship_type: 'performance_impact'}]->(p2)

MATCH (p1:Preference {spec: 'cpu'})
MATCH (p3:Preference {spec: 'ram'})
MERGE (p1)-[:RELATED_TO {weight: 0.5, relationship_type: 'performance_synergy'}]->(p3)

// RAM relationships
MATCH (p3:Preference {spec: 'ram'})
MATCH (p2:Preference {spec: 'gaming'})
MERGE (p3)-[:RELATED_TO {weight: 0.6, relationship_type: 'multitasking_support'}]->(p2)

MATCH (p3:Preference {spec: 'ram'})
MATCH (p4:Preference {spec: 'office'})
MERGE (p3)-[:RELATED_TO {weight: 0.4, relationship_type: 'productivity_boost'}]->(p4)

// Screen relationships
MATCH (p5:Preference {spec: 'screen_size'})
MATCH (p6:Preference {spec: 'portability'})
MERGE (p5)-[:RELATED_TO {weight: 0.8, relationship_type: 'size_tradeoff'}]->(p6)

MATCH (p5:Preference {spec: 'screen_size'})
MATCH (p7:Preference {spec: 'viewing_experience'})
MERGE (p5)-[:RELATED_TO {weight: 0.9, relationship_type: 'quality_enhancement'}]->(p7)

// Battery relationships
MATCH (p8:Preference {spec: 'battery'})
MATCH (p6:Preference {spec: 'portability'})
MERGE (p8)-[:RELATED_TO {weight: 0.9, relationship_type: 'mobility_factor'}]->(p6)

MATCH (p8:Preference {spec: 'battery'})
MATCH (p4:Preference {spec: 'office'})
MERGE (p8)-[:RELATED_TO {weight: 0.7, relationship_type: 'productivity_duration'}]->(p4)

// Storage relationships
MATCH (p9:Preference {spec: 'storage'})
MATCH (p2:Preference {spec: 'gaming'})
MERGE (p9)-[:RELATED_TO {weight: 0.6, relationship_type: 'game_load_time'}]->(p2)

MATCH (p9:Preference {spec: 'storage'})
MATCH (p4:Preference {spec: 'multitasking'})
MERGE (p9)-[:RELATED_TO {weight: 0.5, relationship_type: 'file_management'}]->(p4)

// Weight relationships
MATCH (p10:Preference {spec: 'weight'})
MATCH (p6:Preference {spec: 'portability'})
MERGE (p10)-[:RELATED_TO {weight: 1.0, relationship_type: 'direct_impact'}]->(p6)

// Brand relationships
MATCH (p11:Preference {spec: 'brand'})
MATCH (p12:Preference {spec: 'reliability'})
MERGE (p11)-[:RELATED_TO {weight: 0.8, relationship_type: 'quality_indicator'}]->(p12)

MATCH (p11:Preference {spec: 'brand'})
MATCH (p13:Preference {spec: 'support'})
MERGE (p11)-[:RELATED_TO {weight: 0.6, relationship_type: 'service_quality'}]->(p13)

// Price relationships
MATCH (p14:Preference {spec: 'price'})
MATCH (p15:Preference {spec: 'value'})
MERGE (p14)-[:RELATED_TO {weight: 0.9, relationship_type: 'cost_benefit'}]->(p15)

MATCH (p14:Preference {spec: 'price'})
MATCH (p16:Preference {spec: 'budget'})
MERGE (p14)-[:RELATED_TO {weight: 1.0, relationship_type: 'budget_constraint'}]->(p16)
"""

# 3. Example queries to analyze user profiles
"""
// Get all users and their top preferences
MATCH (u:User)-[:HAS_PROFILE]->(up:UserProfile)-[:HAS_PREFERENCE]->(p:Preference)
RETURN u.fingerprint, p.spec, p.preference, p.confidence
ORDER BY u.fingerprint, p.preference DESC

// Get spreading activation paths for a specific user
MATCH (up:UserProfile {fingerprint: $fingerprint})-[:HAS_PREFERENCE]->(p1:Preference)
MATCH (p1)-[:RELATED_TO*1..3]->(p2:Preference)
WHERE NOT (up)-[:HAS_PREFERENCE]->(p2)
RETURN p1.spec as source, p2.spec as target, 
       [r in relationships(p1)-[:RELATED_TO*1..3]->(p2) | r.weight] as weights,
       [r in relationships(p1)-[:RELATED_TO*1..3]->(p2) | r.relationship_type] as relationship_types

// Get relationship statistics
MATCH ()-[:RELATED_TO]->(r)
RETURN r.relationship_type, count(r) as relationship_count,
       avg(r.weight) as avg_weight,
       min(r.weight) as min_weight,
       max(r.weight) as max_weight

// Find users with similar preferences (collaborative filtering)
MATCH (u1:User)-[:HAS_PROFILE]->(up1:UserProfile)-[:HAS_PREFERENCE]->(p1:Preference)
MATCH (u2:User)-[:HAS_PROFILE]->(up2:UserProfile)-[:HAS_PREFERENCE]->(p2:Preference)
WHERE u1.fingerprint < u2.fingerprint AND p1.spec = p2.spec
RETURN u1.fingerprint, u2.fingerprint, p1.spec,
       p1.preference as pref1, p2.preference as pref2,
       abs(p1.preference - p2.preference) as preference_diff
ORDER BY preference_diff
LIMIT 10
"""

# 4. Maintenance queries
"""
// Clean up old preferences (older than 6 months)
MATCH (up:UserProfile)-[:HAS_PREFERENCE]->(p:Preference)
WHERE p.updated_at < datetime('now') - duration({months: 6})
DETACH DELETE p

// Update relationship weights based on user feedback patterns
MATCH (p1:Preference)-[r:RELATED_TO]->(p2:Preference)
// Add some logic to adjust weights based on successful recommendations
// This is a placeholder for your business logic
SET r.weight = r.weight * 1.01  // Slight increase over time
WHERE r.weight < 1.0

// Find orphaned preference nodes
MATCH (p:Preference)
WHERE NOT (:UserProfile)-[:HAS_PREFERENCE]->(p)
DETACH DELETE p
"""

# 5. Create example user profiles for testing
"""
// Example: Gaming enthusiast profile
MERGE (u:User {fingerprint: 'gaming_user_123'})
CREATE (up:UserProfile {fingerprint: 'gaming_user_123'})
CREATE (u)-[:HAS_PROFILE]->(up)

// Set high preference for gaming with high confidence
CREATE (p_gaming:Preference {
    spec: 'gaming', 
    preference: 0.9, 
    confidence: 1.0,
    created_at: datetime(),
    updated_at: datetime()
})
CREATE (up)-[:HAS_PREFERENCE]->(p_gaming)

// Set preferences for gaming-related specs
WITH up
CREATE (p_cpu:Preference {
    spec: 'cpu', 
    preference: 0.8, 
    confidence: 0.8,
    created_at: datetime(),
    updated_at: datetime()
})
CREATE (up)-[:HAS_PREFERENCE]->(p_cpu)

CREATE (p_ram:Preference {
    spec: 'ram', 
    preference: 0.7, 
    confidence: 0.7,
    created_at: datetime(),
    updated_at: datetime()
})
CREATE (up)-[:HAS_PREFERENCE]->(p_ram)

CREATE (p_screen:Preference {
    spec: 'refresh_rate', 
    preference: 0.9, 
    confidence: 0.8,
    created_at: datetime(),
    updated_at: datetime()
})
CREATE (up)-[:HAS_PREFERENCE]->(p_screen)

// Example: Office user profile
MERGE (u2:User {fingerprint: 'office_user_456'})
CREATE (up2:UserProfile {fingerprint: 'office_user_456'})
CREATE (u2)-[:HAS_PROFILE]->(up2)

// Set high preference for office with high confidence
CREATE (p_office:Preference {
    spec: 'office', 
    preference: 0.9, 
    confidence: 1.0,
    created_at: datetime(),
    updated_at: datetime()
})
CREATE (up2)-[:HAS_PREFERENCE]->(p_office)

// Set preferences for office-related specs
WITH up2
CREATE (p_battery:Preference {
    spec: 'battery', 
    preference: 0.8, 
    confidence: 0.8,
    created_at: datetime(),
    updated_at: datetime()
})
CREATE (up2)-[:HAS_PREFERENCE]->(p_battery)

CREATE (p_weight:Preference {
    spec: 'weight', 
    preference: 0.7, 
    confidence: 0.7,
    created_at: datetime(),
    updated_at: datetime()
})
CREATE (up2)-[:HAS_PREFERENCE]->(p_weight)

CREATE (p_price:Preference {
    spec: 'price', 
    preference: 0.7, 
    confidence: 0.8,
    created_at: datetime(),
    updated_at: datetime()
})
CREATE (up2)-[:HAS_PREFERENCE]->(p_price)
"""