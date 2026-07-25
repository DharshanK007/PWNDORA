import os
import re

endpoints_dir = "backend/app/api/v1/endpoints"
files = [f for f in os.listdir(endpoints_dir) if f.endswith(".py") and f != "__init__.py"]

for filename in files:
    filepath = os.path.join(endpoints_dir, filename)
    with open(filepath, "r") as f:
        content = f.read()
        
    if "from app.api.dependencies.query import QueryParameters, get_query_parameters" not in content:
        content = "from app.api.dependencies.query import QueryParameters, get_query_parameters\n" + content
        
    # Replace the parameters in the get/list functions
    # Generally looks like:
    # def read_employees(
    #     db: Session = Depends(deps.get_db),
    #     skip: int = 0,
    #     limit: int = 100,
    #     current_user = Depends(deps.get_current_user)
    # )
    
    # We will use regex to find skip: int = 0,\n    limit: int = 100, or similar
    pattern = re.compile(r'skip:\s*int\s*=\s*0,\s*limit:\s*int\s*=\s*100,?')
    content = pattern.sub('params: QueryParameters = Depends(get_query_parameters),', content)
    
    # Now we need to replace skip=skip, limit=limit with params=params
    # Also skip=0, limit=100 just in case
    # e.g., get_multi(db, skip=skip, limit=limit)
    call_pattern = re.compile(r'skip\s*=\s*skip\s*,\s*limit\s*=\s*limit')
    content = call_pattern.sub('params=params', content)
    
    call_pattern2 = re.compile(r'skip\s*=\s*0\s*,\s*limit\s*=\s*100')
    content = call_pattern2.sub('params=params', content)
    
    # Update the return statement for PagedResponse
    # return {"items": items, "total": total, "skip": skip, "limit": limit}
    # return {"items": items, "total": total, "skip": params.skip, "limit": params.limit}
    return_pattern = re.compile(r'"skip":\s*skip,\s*"limit":\s*limit')
    content = return_pattern.sub('"skip": params.skip, "limit": params.limit', content)
    
    # Also need to pass params=params to get_count(db) if it exists
    # total = x.get_count(db) -> total = x.get_count(db, params=params)
    count_pattern = re.compile(r'get_count\(db\)')
    content = count_pattern.sub('get_count(db, params=params)', content)

    with open(filepath, "w") as f:
        f.write(content)
        
print("Updated list endpoints")
