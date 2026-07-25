with open('backend/alembic/versions/921409651aaa_add_workflow_enums.py', 'r') as f:
    content = f.read()

content = content.replace(
    "op.add_column('employees', sa.Column('status', sa.Enum('PENDING', 'ACTIVE', 'SUSPENDED', 'TERMINATED', name='employeestatusenum'), nullable=False))",
    "op.add_column('employees', sa.Column('status', sa.Enum('PENDING', 'ACTIVE', 'SUSPENDED', 'TERMINATED', name='employeestatusenum'), nullable=False, server_default='PENDING'))"
)
content = content.replace(
    "op.add_column('firmwares', sa.Column('status', sa.Enum('DRAFT', 'PENDING_APPROVAL', 'APPROVED', 'DEPLOYED', 'RETIRED', name='firmwarestatusenum'), nullable=False))",
    "op.add_column('firmwares', sa.Column('status', sa.Enum('DRAFT', 'PENDING_APPROVAL', 'APPROVED', 'DEPLOYED', 'RETIRED', name='firmwarestatusenum'), nullable=False, server_default='DRAFT'))"
)
content = content.replace(
    "op.add_column('inventory', sa.Column('status', sa.Enum('CREATED', 'AVAILABLE', 'ALLOCATED', 'CONSUMED', 'RESTOCKED', name='inventorystatusenum'), nullable=False))",
    "op.add_column('inventory', sa.Column('status', sa.Enum('CREATED', 'AVAILABLE', 'ALLOCATED', 'CONSUMED', 'RESTOCKED', name='inventorystatusenum'), nullable=False, server_default='CREATED'))"
)
content = content.replace(
    "op.add_column('reports', sa.Column('status', sa.Enum('DRAFT', 'UNDER_REVIEW', 'APPROVED', 'PUBLISHED', 'ARCHIVED', name='reportstatusenum'), nullable=False))",
    "op.add_column('reports', sa.Column('status', sa.Enum('DRAFT', 'UNDER_REVIEW', 'APPROVED', 'PUBLISHED', 'ARCHIVED', name='reportstatusenum'), nullable=False, server_default='DRAFT'))"
)

with open('backend/alembic/versions/921409651aaa_add_workflow_enums.py', 'w') as f:
    f.write(content)
