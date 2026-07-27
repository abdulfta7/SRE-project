# Integrating with the ghaymah CLI

To manage and deploy applications to ghaymah.systems from your local machine or CI/CD pipeline, you need to use the `ghaymah` CLI.

## 1. Installation
Depending on your OS, install the CLI (example for macOS/Linux):
```bash
curl -sL https://cli.ghaymah.systems/install.sh | bash
```

## 2. Authentication
Log in to your ghaymah account:
```bash
ghaymah login
```
This will open a browser window to authenticate. If you are in a CI/CD environment (headless), use a token:
```bash
ghaymah login --token $GHAYMAH_TOKEN
```

## 3. Pushing Images to ghaymah Container Registry
Authenticate Docker with the ghaymah registry:
```bash
docker login registry.ghaymah.systems -u $GHAYMAH_USERNAME -p $GHAYMAH_TOKEN
```
Build and push your image:
```bash
docker build -t registry.ghaymah.systems/my-org/myapp-api:v1 .
docker push registry.ghaymah.systems/my-org/myapp-api:v1
```

## 4. Deploying the Application
Once the image is in the registry, deploy it using the CLI:
```bash
ghaymah deploy \
  --name myapp-api \
  --image registry.ghaymah.systems/my-org/myapp-api:v1 \
  --port 8080 \
  --env production
```
You can also monitor logs in real-time:
```bash
ghaymah logs myapp-api --follow
```
