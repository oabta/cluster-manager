# Cluster Manager

`Cluster Manager` is a Python CLI designed to simplify the management of service clusters in production environments.

The CLI automates the process of `provisioning`, `scaling`, and `monitoring` clusters consisting of services
such as `PostgreSQL/MySQL` for databases and Redis for caching or queuing.

---

## Installation

### Prerequisites

Before using the `Cluster Manager` CLI, ensure the following dependencies are installed:

- **Docker**: To run the containers.
- **Python 3.7+**: To run the CLI tool.
- **pip**: To install Python packages.

### Install Cluster Manager CLI

To install the CLI tool, run:

```bash
git clone https://github.com/oabta/cluster-manager.git
cd cluster-manager
pip install .
```

## Usage

The `oabta-clusters` CLI tool provides several commands to manage clusters of services, such as PostgreSQL/MySQL
databases and Redis for caching or queuing.

Below is a list of available commands and their usage.

### 1. Create a Cluster

This command creates a new cluster with a specified database (PostgreSQL or MySQL) and Redis.

```bash
oabta-clusters create <cluster_name> --db <postgres|mysql> --redis
```

- `<cluster_name>`: The name of the cluster to create.
- `--db`: Choose between `postgres` or `mysql` for the database (defaults to postgres).
- `--redis`: Option to include Redis in the cluster (enabled by default).

#### Example:

```bash 
oabta-clusters create my-cluster --db postgres --redis
```

This will create a cluster named `my-cluster` with PostgreSQL and Redis.

### 2. Start a Cluster

Start the services in the specified cluster.

```bash
oabta-clusters start <cluster_name>
```

#### Example

```bash
oabta-clusters start my-cluster
```

### 3. Stop a Cluster

Stop the services in the specified cluster.

```bash
oabta-clusters stop <cluster_name>
```

#### Example

```bash
oabta-clusters stop my-cluster
```

### 4. Restart a Cluster

Stop and start the services to restart the cluster.

```bash
oabta-clusters restart <cluster_name>
```

### 5. Check the Status of a Cluster

Check whether the services in the cluster are up and running.

```bash
oabta-clusters status <cluster_name>
```

#### Example:

```bash 
oabta-clusters status my-cluster
```

### 6. View Logs for a Cluster

View the logs for the containers in the specified cluster.

```bash
oabta-clusters logs <cluster_name>
```

#### Example:

```
oabta-clusters logs my-cluster
```

### 7. Scale a Service in the Cluster

Scale a specific service (e.g., database or Redis) to a desired number of replicas.

```bash
oabta-clusters scale <cluster_name> <service_name> <replicas>
```

- `<service_name>`: Choose either `db` (for database) or `redis`.
- `<replicas>`: The number of replicas for the service.

#### Example:

```bash
oabta-clusters scale my-cluster db 3
```

This will scale the database service in `my-cluster` to 3 replicas.

### 8. Remove a Cluster

Stop the services and delete the associated containers and the docker-compose.yaml file.

```bash
oabta-clusters remove <cluster_name>
```

#### Example:

```bash
oabta-clusters remove my-cluster
```