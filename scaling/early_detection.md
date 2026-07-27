# Early Detection of Memory Issues

Waiting for an application to crash (OOMKilled) is a reactive approach. To proactively detect memory issues, we must configure our monitoring tools (Prometheus, Datadog, or ghaymah metrics).

## 1. High-Watermark Alerting
Configure alerts on the metric `container_memory_usage_bytes` (or equivalent).

- **Warning Alert (Slack/Teams):**
  - Trigger: Container Memory > 80% of limit
  - Duration: Sustained for > 3 minutes.
  - Action: Alerts the engineering team during business hours to investigate potential memory leaks.

- **Critical Alert (PagerDuty/Phone Call):**
  - Trigger: Container Memory > 90% of limit
  - Duration: Sustained for > 2 minutes.
  - Action: Wakes up the on-call engineer to apply mitigations (e.g., manual scaling, restarting pods) before the crash happens.

## 2. Rate of Change Alerting (Anomaly Detection)
Sometimes memory doesn't hit a static threshold, but it grows unusually fast.
- Monitor the *derivative* (rate of change) of memory usage.
- If memory grows by more than 20% within 5 minutes (without a corresponding 20% spike in traffic), trigger an anomaly alert.

## 3. APM Profiling
- Integrate APM (Application Performance Monitoring) to track Garbage Collection (GC) pauses in languages like Java/Node.js, or memory footprint per request in Python/Go.
- A sudden increase in GC time is often a precursor to an OOM event.
