with open('backend/app/schemas/base.py', 'r') as f:
    content = f.read()

replacement = '''
class WorkflowMetadataResponse(BaseModel):
    current_state: str
    allowed_transitions: list[str]
'''

if 'WorkflowMetadataResponse' not in content:
    content += '\n' + replacement + '\n'
    with open('backend/app/schemas/base.py', 'w') as f:
        f.write(content)
