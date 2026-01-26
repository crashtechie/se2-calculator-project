# PreDeployment validation steps for ENH-0000007: additional instructions
    - validate database structure to ensure all fields are present

# deployment steps
    - apply migrations
    - configure templates, forms, views, and urls in that order to prevent incorrect errors
    - save validation till end of deployment steps when all components are in place