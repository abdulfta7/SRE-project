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

## 4. Cold Start Strategy
To minimize the delay when new containers are provisioned (cold start latency):
1. **Lightweight Base Images:** Use Alpine or distroless images (e.g., `python:3.11-alpine`) so they pull faster over the network.
2. **Pre-warming (Buffer Pool):** Maintain a buffer of idle containers (e.g., 10% of required capacity). For 43 containers, run ~47. The extra 4 handle sudden spikes instantly.
3. **Lazy Loading:** Defer non-critical initialization until after the container has started accepting requests.

## 5. Ghaymah Block Storage for Stateful Workloads
While the API is mostly stateless, Ghaymah Block Storage is used for:
- **Local Caching / ML Models:** Persistent storage for large datasets downloaded at startup.
- **Session Data / Logs:** Persisting complex audit logs before they are shipped to centralized logging.
- **Self-Managed Databases:** Ensuring data survives container restarts by mounting a volume like `/mnt/data`.
