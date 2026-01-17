# 🌀 Quantum Tech Trader 🌀

**⚠️ WARNING: USE AT YOUR OWN RISK! MAXIMUM CHAOS MODE! ⚠️**

A production-ready, quantum-inspired cryptocurrency trading simulator with multiple deployment modes: CLI, API service, web dashboard-ready, and scheduler support.

## 🚨 DISCLAIMER 🚨

**THIS IS NOT FINANCIAL ADVICE!** This is an experimental, educational, and entertainment project.
- All trades are **SIMULATED** (no real money)
- Extremely high volatility and chaos by design
- Use at your own risk - we warned you! 💀

## 🌟 Features

- **Quantum Superposition**: Multiple trading strategies evaluated simultaneously
- **Quantum Entanglement**: Correlated analysis across crypto pairs
- **Wave Function Collapse**: Probabilistic decision-making
- **Quantum Tunneling**: Breakthrough resistance levels unexpectedly
- **Deterministic Mode**: Reproducible simulations with seed support
- **Production Ready**: Structured logging, containerization, Kubernetes support
- **Four Working Modes**: CLI, API, Scheduler, and Dashboard-ready

## 📦 Multi-Crypto Support

BTC, ETH, DOGE, SHIB, ADA, SOL, MATIC, AVAX

## 🚀 Quick Start

### Prerequisites

- Python 3.11+ (3.9+ should work)
- Docker (optional, for containerized deployment)
- Kubernetes cluster (optional, for K8s deployment)

### Installation

```bash
# Clone the repository
git clone https://github.com/NaTo1000/Quantum-tech-trader.git
cd Quantum-tech-trader

# Install dependencies
pip install -r requirements.txt

# For development
pip install -r requirements-dev.txt
```

## 🔄 Migration from v1.x

**The original interactive script (`quantum_trader.py`) still works!** It has been preserved for backward compatibility.

```bash
# Old way (still works)
python quantum_trader.py

# New way (non-interactive, production-ready)
python -m src.quantum_trader.cli --chaos-level 0.8 --cycles 5
```

**Key differences:**
- ✅ Old script preserved as-is for compatibility
- ✅ New package structure under `src/quantum_trader/`
- ✅ Non-interactive CLI with argparse
- ✅ FastAPI service for programmatic access
- ✅ Docker and Kubernetes support
- ✅ All original functionality maintained

## 🎮 Four Working Modes

### 1. CLI Mode (Non-Interactive)

Deterministic command-line interface with full parameter control.

```bash
# Basic usage
python -m src.quantum_trader.cli

# Custom parameters
python -m src.quantum_trader.cli --chaos-level 0.5 --cycles 10

# Deterministic mode with seed
python -m src.quantum_trader.cli --seed 42 --cycles 5

# Silent mode with log file
python -m src.quantum_trader.cli --silent --log-file ./data/trader.log

# Custom data directory
python -m src.quantum_trader.cli --data-dir /mnt/trades --cycles 20
```

**CLI Options:**
- `--chaos-level`: Volatility level (0.0-1.0, default: 0.8)
- `--cycles`: Number of trading cycles (1-100, default: 5)
- `--seed`: Random seed for deterministic behavior (optional)
- `--data-dir`: Directory for trade history (default: ./data)
- `--log-file`: Optional log file path
- `--silent`: Suppress console output (logs only)

### 2. API Service Mode

FastAPI-based REST service for programmatic access.

```bash
# Start API server
python -m src.quantum_trader.service

# Custom host/port
python -m uvicorn src.quantum_trader.service:app --host 0.0.0.0 --port 8000
```

**API Endpoints:**

- `GET /` - API information
- `GET /healthz` - Health check (for orchestration)
- `POST /simulate?chaos_level=0.7&cycles=5&seed=42` - Run simulation
- `GET /info` - System information
- `GET /docs` - Interactive API documentation (Swagger UI)

**Example API Usage:**

```bash
# Health check
curl http://localhost:8000/healthz

# Run simulation
curl -X POST "http://localhost:8000/simulate?chaos_level=0.7&cycles=5&seed=42"

# With Python requests
import requests
response = requests.post("http://localhost:8000/simulate", params={
    "chaos_level": 0.7,
    "cycles": 5,
    "seed": 42
})
print(response.json())
```

### 3. Scheduler Mode

Automated periodic simulations (placeholder for cron/APScheduler).

```bash
# Run once
python -m src.quantum_trader.scheduler --run-once

# Run every hour
python -m src.quantum_trader.scheduler --interval 3600

# Run every 30 minutes with max 10 runs
python -m src.quantum_trader.scheduler --interval 1800 --max-runs 10

# Custom parameters
python -m src.quantum_trader.scheduler --chaos-level 0.6 --cycles 3 --interval 3600
```

### 4. Web Dashboard (API-Ready)

The API service is ready to integrate with web dashboards. Connect your frontend to the `/simulate` endpoint.

**Frontend Integration Example:**

```javascript
// React/Vue/Angular example
async function runSimulation() {
  const response = await fetch('http://localhost:8000/simulate?chaos_level=0.7&cycles=5');
  const data = await response.json();
  console.log('Portfolio:', data.final_portfolio);
  console.log('Trades:', data.trades);
}
```

## 🐳 Docker Deployment

### Build and Run

```bash
# Build image
docker build -t quantum-trader:latest .

# Run API server (default)
docker run -p 8000:8000 -v $(pwd)/data:/app/data quantum-trader:latest

# Run CLI mode
docker run -v $(pwd)/data:/app/data quantum-trader:latest \
  python -m src.quantum_trader.cli --chaos-level 0.7 --cycles 10

# Run scheduler
docker run -v $(pwd)/data:/app/data quantum-trader:latest \
  python -m src.quantum_trader.scheduler --interval 3600
```

### Docker Compose

```bash
# Start API service
docker-compose up -d

# View logs
docker-compose logs -f quantum-trader-api

# Run CLI (one-shot)
docker-compose run --rm quantum-trader-cli

# Start scheduler
docker-compose --profile scheduler up -d

# Stop all services
docker-compose down
```

**Multi-Stage Build Benefits:**
- Optimized image size (~150MB)
- Separate build and runtime stages
- Non-root user for security
- Health checks included

## ☸️ Kubernetes Deployment

### Deploy to Kubernetes

```bash
# Apply manifests
kubectl apply -f deploy/k8s/deployment.yaml
kubectl apply -f deploy/k8s/service.yaml

# Optional: Enable autoscaling
kubectl apply -f deploy/k8s/hpa.yaml

# Check status
kubectl get pods -l app=quantum-trader
kubectl get svc quantum-trader

# View logs
kubectl logs -l app=quantum-trader -f

# Port forward for local access
kubectl port-forward svc/quantum-trader 8000:80
```

### Cloud Platform Notes

#### GCP (GKE)

```bash
# Create GKE cluster
gcloud container clusters create quantum-trader-cluster \
  --num-nodes=3 --machine-type=e2-small --region=us-central1

# Get credentials
gcloud container clusters get-credentials quantum-trader-cluster --region=us-central1

# Deploy
kubectl apply -f deploy/k8s/

# Expose with Ingress (optional)
# Configure Cloud Load Balancer or use GKE Ingress
```

**Storage:** Use GCE Persistent Disk for PVC (default in GKE)

#### AWS (EKS)

```bash
# Create EKS cluster (using eksctl)
eksctl create cluster --name quantum-trader --region us-west-2 --nodes 3

# Deploy
kubectl apply -f deploy/k8s/

# Expose with LoadBalancer or ALB Ingress Controller
```

**Storage:** Use EBS volumes for PVC (configure StorageClass: gp3)

#### Azure (AKS)

```bash
# Create AKS cluster
az aks create --resource-group quantum-rg --name quantum-trader-cluster \
  --node-count 3 --enable-managed-identity

# Get credentials
az aks get-credentials --resource-group quantum-rg --name quantum-trader-cluster

# Deploy
kubectl apply -f deploy/k8s/
```

**Storage:** Use Azure Disk for PVC (default in AKS)

### Autoscaling

The HPA (Horizontal Pod Autoscaler) automatically scales pods based on CPU/memory:

- **Min replicas:** 2
- **Max replicas:** 10
- **CPU target:** 70%
- **Memory target:** 80%

**Prerequisites:**
- Metrics Server must be installed in the cluster
- Resource requests/limits defined in deployment

```bash
# Check HPA status
kubectl get hpa quantum-trader-hpa
kubectl describe hpa quantum-trader-hpa
```

### Ingress Configuration

For production HTTPS access:

```yaml
# Example Ingress (create as deploy/k8s/ingress.yaml)
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: quantum-trader-ingress
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod  # For TLS
spec:
  rules:
  - host: quantum-trader.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: quantum-trader
            port:
              number: 80
  tls:
  - hosts:
    - quantum-trader.yourdomain.com
    secretName: quantum-trader-tls
```

## 📱 Platform Support

### Linux / Debian / Ubuntu

```bash
# Fully supported - native execution
python -m src.quantum_trader.cli
```

### macOS

```bash
# Fully supported - native execution
python3 -m src.quantum_trader.cli

# Or via Docker
docker run -v $(pwd)/data:/app/data quantum-trader:latest
```

### Windows

```powershell
# Native execution (PowerShell/CMD)
python -m src.quantum_trader.cli

# Or via Docker
docker run -v ${PWD}/data:/app/data quantum-trader:latest
```

### Android / iOS

Use the API service and connect via HTTP client:

```bash
# Run API server (locally or cloud)
# Access from mobile app via REST API

# Example mobile app integration:
# - Deploy API to cloud (GCP/AWS/Azure)
# - Connect mobile app to https://your-api.com/simulate
# - Display results in mobile UI
```

**Recommended:** Deploy API to cloud and access via mobile HTTP client libraries.

## 🧪 Testing

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run with coverage
pytest --cov=src/quantum_trader --cov-report=html

# Run specific test file
pytest tests/test_core.py -v

# Test with different seeds
pytest tests/test_core.py -v -k deterministic
```

**Test Coverage:**
- ✅ Price oracle positivity (all prices > 0)
- ✅ Cash balance never negative
- ✅ Portfolio amounts never negative
- ✅ Valid trading actions
- ✅ Deterministic mode with seeds
- ✅ Parameter validation and clamping
- ✅ Trade history persistence

## 📊 Example Output

### CLI Mode

```
🌀 QUANTUM TRADING CYCLE | State: ENTANGLED 🌀

💰 BTC: $52341.23456789
   📊 Strategies in superposition: 4
   ⚡ Collapsed action: MOON_SHOT
🚀 QUANTUM BUY: 0.019234 BTC @ $52341.23

💰 ETH: $2847.91283746
   📊 Strategies in superposition: 4
   ⚡ Collapsed action: PANIC_SELL
📉 QUANTUM SELL: 0.582341 ETH @ $2847.91

📊 QUANTUM PORTFOLIO STATUS 📊
💵 Cash: $8234.56
   BTC: 0.019234 (≈$1006.78)
   ETH: 0.231876 (≈$660.23)
💎 Total Portfolio Value: $9901.57
📉 P/L: -$98.43 (-0.98%)
```

### API Response

```json
{
  "final_cash": 8234.56,
  "final_portfolio": {
    "BTC": 0.019234,
    "ETH": 0.231876,
    "DOGE": 0.0,
    "SHIB": 0.0,
    "ADA": 0.0,
    "SOL": 0.0,
    "MATIC": 0.0,
    "AVAX": 0.0
  },
  "trades": [
    {
      "timestamp": "2024-01-15T10:30:45.123456",
      "action": "BUY",
      "symbol": "BTC",
      "price": 52341.23,
      "amount": 0.019234,
      "cost": 1006.78,
      "quantum_state": "ENTANGLED"
    }
  ],
  "chaos_level": 0.8,
  "total_trades": 12,
  "message": "Simulation complete!"
}
```

## 🎲 Chaos Levels

- **0.0-0.3**: Mild chaos (boring! 😴)
- **0.4-0.6**: Moderate chaos (exciting! 🎢)
- **0.7-0.9**: HIGH CHAOS (wild ride! 🎪)
- **0.9-1.0**: MAXIMUM CHAOS (absolute mayhem! 🌪️💀)

## 🔒 Security Features

- ✅ Non-root Docker container execution
- ✅ No external network calls (simulated only)
- ✅ Input validation and parameter clamping
- ✅ Health checks for orchestration
- ✅ Structured logging for audit trails
- ✅ No secrets or credentials required

## 📁 Project Structure

```
Quantum-tech-trader/
├── src/quantum_trader/
│   ├── __init__.py          # Package initialization
│   ├── core.py              # Core trading logic
│   ├── cli.py               # CLI entry point
│   ├── service.py           # FastAPI service
│   └── scheduler.py         # Scheduler (cron/APS)
├── tests/
│   └── test_core.py         # Core logic tests
├── deploy/
│   └── k8s/
│       ├── deployment.yaml  # K8s Deployment
│       ├── service.yaml     # K8s Service
│       └── hpa.yaml         # Autoscaling config
├── data/                    # Trade history (gitignored)
├── Dockerfile               # Multi-stage Docker build
├── docker-compose.yaml      # Docker Compose config
├── requirements.txt         # Runtime dependencies
├── requirements-dev.txt     # Dev dependencies
└── README.md                # This file
```

## 🔧 Configuration

### Environment Variables

```bash
# Set data directory
export QUANTUM_DATA_DIR=/mnt/trades

# Enable verbose logging
export PYTHONUNBUFFERED=1

# For Docker/K8s
docker run -e QUANTUM_DATA_DIR=/data quantum-trader:latest
```

### Persistent Storage

Trade histories are saved to `./data` by default:

```bash
# Local
--data-dir /path/to/storage

# Docker
-v /host/path:/app/data

# Kubernetes
# Configure PVC in deployment.yaml
```

## 🤝 Contributing

Contributions welcome! Areas for enhancement:

- Advanced portfolio rebalancing
- Machine learning strategy models
- Real-time price feed integration (simulated)
- Enhanced web dashboard UI
- Advanced scheduling with APScheduler
- Prometheus metrics export
- Additional cloud platform optimizations

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📜 License

MIT License - Use at your own risk!

## 🎯 Educational Purpose

This project demonstrates:
- Microservices architecture
- REST API design with FastAPI
- Containerization with Docker
- Kubernetes orchestration
- Probabilistic trading strategies
- Portfolio management concepts
- Production-ready Python practices

## ⚡ Performance Notes

- **API latency**: ~50-200ms per simulation (depends on cycles)
- **Memory usage**: ~100MB per container
- **CPU usage**: Low (simulation is compute-light)
- **Storage**: ~1KB per trade history file

## 🆘 Troubleshooting

### Docker Issues

```bash
# Permission denied for data directory
chmod -R 777 ./data

# Container exits immediately
docker logs quantum-trader-api

# Health check failing
curl http://localhost:8000/healthz
```

### Kubernetes Issues

```bash
# Pods not starting
kubectl describe pod -l app=quantum-trader

# PVC not binding
kubectl get pvc
kubectl describe pvc quantum-trader-pvc

# Service not accessible
kubectl get svc
kubectl describe svc quantum-trader
```

### Python Issues

```bash
# Module not found
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python -m src.quantum_trader.cli

# Dependencies missing
pip install -r requirements.txt
```

## 🔥 Let It Rip!

Remember: **This is pure chaos by design!** Embrace the quantum uncertainty and enjoy the ride!

```
🌀🌀🌀 QUANTUM CHAOS AWAITS 🌀🌀🌀
```

---

**Made with ⚡ quantum chaos ⚡ and 💀 maximum risk 💀**

**⚠️ REMEMBER: ALL SIMULATED - NOT FINANCIAL ADVICE - ALWAYS DO YOUR OWN RESEARCH! ⚠️**
