export const REMEDIATION_CHIPS: Record<string, string[]> = {
  informational: [
    "Implement automated patch management",
    "Establish routine asset discovery scans",
    "Update firmware to latest vendor release"
  ],
  authorization: [
    "Enforce server-side ownership validation",
    "Implement strict Role-Based Access Control (RBAC)",
    "Use indirect object references instead of direct IDs",
    "Verify user clearance level on every request"
  ],
  injection: [
    "Use parameterized queries for all database access",
    "Implement strict input validation and sanitization",
    "Adopt an ORM to prevent SQL injection",
    "Enforce least privilege on database accounts"
  ],
  authentication: [
    "Do not trust client-supplied session metadata (e.g., headers)",
    "Re-verify user role server-side against secure session store",
    "Implement secure, signed, and encrypted JWTs",
    "Enforce re-authentication for critical actions"
  ],
  default: [
    "Enforce principle of least privilege",
    "Conduct regular security awareness training",
    "Implement comprehensive audit logging"
  ]
};
