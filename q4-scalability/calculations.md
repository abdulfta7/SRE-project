# Capacity Planning: Handling 15,000 req/s

To ensure high availability and responsiveness under a load of 15,000 requests per second, we must calculate the required number of container instances.

## Base Assumptions
- **Target Load:** 15,000 req/s
- **Max Capacity per Container:** 500 req/s
- **Safety Margin:** 30%

## Calculation
1. **Effective Capacity per Container:** 
   To maintain a 30% margin, we calculate the effective capacity each container should handle before we consider scaling out.
   `500 req/s * (1 - 0.30) = 350 req/s`

2. **Total Containers Required:**
   Divide the total expected load by the effective capacity per container.
   `15,000 req/s / 350 req/s per container ≈ 42.85`

3. **Rounding Up:**
   We cannot have a fraction of a container, so we always round up to the next whole number.
   `ceil(42.85) = 43 containers`

## Conclusion
To safely handle 15,000 req/s while maintaining a 30% safety margin (which helps absorb sudden traffic spikes or the failure of a few containers), the auto-scaling group should be configured to maintain a baseline of **43 containers** during peak load.
