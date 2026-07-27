# Environments: Staging vs Production

In our deployment pipeline, we utilize two main environments: **Staging** and **Production**. Understanding the differences between them is crucial for safe software delivery.

## 1. Staging Environment (`staging`)
- **Purpose:** A pre-production area for QA testing, integration testing, and final review by stakeholders before a release goes live.
- **Data:** Uses dummy, sanitized, or replicated data. NEVER connects to the live production database.
- **Access:** Restricted to internal team members, developers, and QA testers. Often protected by VPN, IP whitelisting, or Basic Auth.
- **Scale:** Typically scaled down (fewer containers, smaller database instances) to save costs, as it doesn't need to handle user traffic.
- **Deployment:** Automatic upon merging code to the `main` branch.

## 2. Production Environment (`production`)
- **Purpose:** The live environment that real users interact with.
- **Data:** Contains live, sensitive, real user data. Strict access controls and backups are enforced.
- **Access:** Publicly accessible (for web apps/APIs). Infrastructure access is strictly limited to authorized SREs/DevOps personnel.
- **Scale:** Scaled up to handle expected user load, with Auto-Scaling policies enabled to handle traffic spikes.
- **Deployment:** Requires a **Manual Approval** step in the CI/CD pipeline (e.g., in GitHub Actions) to ensure that the code deployed to staging has been properly vetted and approved for live release.
