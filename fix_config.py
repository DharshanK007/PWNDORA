import os

filepath = "backend/app/core/config.py"
with open(filepath, "r") as f:
    content = f.read()

# Add feature flags
feature_flags = '''
    # Feature Flags
    ENABLE_AI: bool = False
    ENABLE_ATTACK_ENGINE: bool = False
    ENABLE_REPLAY: bool = False
    ENABLE_ANALYTICS: bool = False
    ENABLE_CYBER_RANGE: bool = False
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 100
'''

if "ENABLE_AI" not in content:
    content = content.replace("class Config:", feature_flags + "\n    class Config:")

with open(filepath, "w") as f:
    f.write(content)

print("Updated config.py")
