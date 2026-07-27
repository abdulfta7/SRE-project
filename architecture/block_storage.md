# Using ghaymah Block Storage for Stateful Workloads

Containers are inherently stateless; they lose their local filesystem data when they are destroyed or rescheduled. For applications that require persistent data (Stateful Workloads), we utilize **ghaymah Block Storage**.

## 1. What is Block Storage?
Block Storage provides persistent, highly available disk volumes that can be attached to containers. Unlike object storage (S3), it behaves like a physical hard drive mounted to the OS.

## 2. Use Cases in our Architecture
While our API application is mostly stateless, certain workloads require persistence:
- **Local Caching:** If a container downloads large datasets or machine learning models upon startup, these can be stored on Block Storage so subsequent container restarts are faster.
- **Session Data / Logs:** If we are writing complex audit logs that haven't yet been shipped to a centralized logging service.
- **Databases:** If running a self-managed database (e.g., PostgreSQL or Redis) within a container, Block Storage is mandatory to prevent data loss.

## 3. Configuration & Mounting
When deploying via the `ghaymah deploy` CLI or dashboard, we specify a volume mount:
```yaml
volumes:
  - name: my-persistent-data
    size: 50GB
    mountPath: /mnt/data
```
Inside the container, the application can simply read/write files to `/mnt/data/` knowing the data will survive container restarts.
