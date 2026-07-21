export interface Role {
  id: string
  name: string
  permissions: string[]
  member_count: number
}

// Mock service since there's no dedicated roles endpoint yet
export const rolesService = {
  getRoles: async (): Promise<Role[]> => {
    // Simulate network delay
    await new Promise(resolve => setTimeout(resolve, 600))
    
    return [
      {
        id: '1',
        name: 'Administrator',
        permissions: ['all'],
        member_count: 3
      },
      {
        id: '2',
        name: 'Operator',
        permissions: ['read:devices', 'write:tickets'],
        member_count: 12
      },
      {
        id: '3',
        name: 'Engineer',
        permissions: ['read:devices', 'write:devices', 'read:tickets', 'write:tickets'],
        member_count: 8
      },
      {
        id: '4',
        name: 'Viewer',
        permissions: ['read:dashboard', 'read:devices'],
        member_count: 24
      }
    ]
  }
}
