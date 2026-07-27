# Auto-Scaling Policy for ghaymah.systems

To prevent repeating the OOMKilled outage, the platform's auto-scaling group (ASG) must be configured to respond to memory pressure as well as CPU load.

## 1. Scale-Out Policy (Adding Instances)
- **Metric:** Average Container Memory Utilization
- **Threshold:** > 70%
- **Evaluation Period:** 2 minutes (2 consecutive data points of 1 minute each)
- **Action:** Add 1 container instance (Step scaling) or scale by 20% of current capacity.
- **Cooldown Period:** 3 minutes (allows the new container to boot and start serving traffic before evaluating again).

## 2. Scale-In Policy (Removing Instances)
- **Metric:** Average Container Memory Utilization
- **Threshold:** < 40%
- **Evaluation Period:** 5 minutes
- **Action:** Remove 1 container instance.
- **Cooldown Period:** 5 minutes (prevents aggressive scale-in which might cause immediate resource pressure).

## 3. CPU Backup Policy
*Maintain existing CPU policies as a secondary trigger:*
- Scale out if Average CPU > 75% for 2 minutes.

## 4. Minimum / Maximum Capacity
- **Min Containers:** 2 (for high availability across zones)
- **Max Containers:** 20 (to control billing, can be adjusted based on anticipated load)
