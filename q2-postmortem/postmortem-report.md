# Incident Post-mortem: API Service OOMKilled Outage

## 1. Summary
- **Date & Time:** [Insert Date]
- **Duration:** 45 minutes
- **Impact:** API service was completely unavailable for users, resulting in a 100% error rate (502 Bad Gateway / 503 Service Unavailable) during the incident window.
- **Root Cause:** Container memory limit was exceeded, causing the Kubernetes/Cloud orchestrator to continuously terminate the pod with an `OOMKilled` status.

## 2. Timeline (UTC)
- **10:00 AM:** Monitoring alerts triggered for high error rates on the `/health` endpoint.
- **10:05 AM:** On-call engineer acknowledged the alert and started investigation.
- **10:15 AM:** Engineer identified that the container was crash-looping with `OOMKilled` exit code 137.
- **10:25 AM:** A temporary mitigation was applied by manually increasing the container memory limit from 512MB to 1024MB.
- **10:35 AM:** Service stabilized. Containers remained running without restarts.
- **10:45 AM:** Incident marked resolved after 10 minutes of stable metrics.

## 3. Root Cause Analysis (The "5 Whys")
1. **Why did the service go down?** The container was repeatedly killed by the orchestrator.
2. **Why was it killed?** The orchestrator issued an `OOMKilled` (Out Of Memory) signal.
3. **Why did it run out of memory?** The application consumed more memory than its allocated limit (512MB).
4. **Why did it consume so much memory?** An unexpected spike in requests (or a memory leak in a newly deployed feature) caused the application stack to load massive objects into memory simultaneously.
5. **Why wasn't this caught or handled?** The auto-scaling policy was based solely on CPU, so it didn't spin up new instances to distribute the memory load.

## 4. Recommendations & Action Items
- **Immediate:** Keep the memory limit at 1024MB until a thorough memory profiling is completed.
- **Short-term:** Implement a memory-based auto-scaling rule (Scale out when Memory > 70%).
- **Medium-term:** Setup early-detection alerts for memory utilization reaching 80% to warn the team *before* an OOMKilled event occurs.
- **Long-term:** Profile the application to identify memory bottlenecks or leaks.

## 5. Auto-Scaling Policy
To prevent repeating this incident, the platform's auto-scaling group must be configured as follows:
- **Scale-Out Policy:** Add 1 container instance when Average Container Memory > 70% for 2 minutes.
- **Scale-In Policy:** Remove 1 container instance when Average Container Memory < 40% for 5 minutes.
- **CPU Backup Policy:** Scale out if Average CPU > 75% for 2 minutes.

## 6. Early Detection
To detect this issue before the container crashes:
- Configure alerts on the metric `container_memory_usage_bytes` (or equivalent).
- **Warning Alert:** Container Memory > 80% (Sustained for > 3 minutes) - triggers Slack/Teams notification.
- **Critical Alert:** Container Memory > 90% (Sustained for > 2 minutes) - triggers PagerDuty to wake up on-call engineer for immediate manual mitigation.
