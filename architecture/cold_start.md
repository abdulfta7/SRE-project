# Cold Start Strategy

When auto-scaling responds to a traffic spike, new containers must be initialized. The time it takes from the scaling decision to the container actually serving requests is the "cold start" latency.

To minimize this delay and prevent dropped requests, we implement the following strategy:

## 1. Lightweight Base Images
- Use Alpine or distroless base images (e.g., `python:3.11-alpine`).
- Smaller images pull faster from the Container Registry over the network.

## 2. Pre-warming (Buffer Pool)
- Configure the Auto-Scaling Group to always maintain a "buffer" of idle containers (e.g., 10% of the current required capacity).
- If we need 43 containers for active load, we run ~47 containers. When traffic spikes, these 4 idle containers can serve requests instantly while the ASG provisions new ones.

## 3. Lazy Loading & Readiness Probes
- Defer non-critical initialization (like building large in-memory caches) until *after* the container has started accepting requests.
- Configure Kubernetes/ghaymah readiness probes to accurately reflect when the app is ready to serve traffic, ensuring the load balancer doesn't route traffic to a container that is still booting.

## 4. Keep-Alive & Connection Pooling
- Ensure idle containers aren't prematurely terminated. Keep database connections alive in a connection pool to avoid the latency of establishing new TCP handshakes during a sudden burst.
