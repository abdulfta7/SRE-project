# Deployment Instructions: Mithal Monitoring Dashboard

To serve the HTML dashboard and the collected `metrics.json` data, we will deploy a simple Nginx container to ghaymah.systems.

## 1. Directory Structure Setup
Move the dashboard HTML and the `metrics.json` file into a single directory to be served:
```bash
mkdir -p /Users/mac/a1/mithal_monitor/deploy/public
cp /Users/mac/a1/mithal_monitor/dashboard/index.html /Users/mac/a1/mithal_monitor/deploy/public/
# Note: The monitor.py script should be configured to write metrics.json to this 'public' folder.
```

## 2. Nginx Dockerfile
Create a `Dockerfile` in `/Users/mac/a1/mithal_monitor/deploy/`:
```dockerfile
FROM nginx:alpine
COPY public/ /usr/share/nginx/html/
EXPOSE 80
```

## 3. Deployment Steps
Using the `ghaymah` CLI:

```bash
cd /Users/mac/a1/mithal_monitor/deploy

# Build and Push
docker build -t registry.ghaymah.systems/my-org/mithal-dashboard:latest .
docker push registry.ghaymah.systems/my-org/mithal-dashboard:latest

# Deploy
ghaymah deploy \
  --name mithal-dashboard \
  --image registry.ghaymah.systems/my-org/mithal-dashboard:latest \
  --port 80 \
  --env production
```

The dashboard will now be accessible via the URL provided by ghaymah.systems, and it will serve `index.html` as well as `metrics.json` over HTTP(S).
