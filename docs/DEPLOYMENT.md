# ANT AI Deployment Guide

## Overview

This document provides comprehensive instructions for deploying ANT AI in various environments: local development, staging, and production.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development](#local-development)
3. [Docker Deployment](#docker-deployment)
4. [Production Deployment](#production-deployment)
5. [Configuration](#configuration)
6. [Monitoring & Observability](#monitoring--observability)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### System Requirements

- **OS**: Linux (Ubuntu 20.04+), macOS, or Windows with WSL2
- **Docker**: 20.10+
- **Docker Compose**: 1.29+
- **Memory**: Minimum 8GB RAM (16GB+ recommended)
- **Storage**: 20GB+ available disk space
- **Python**: 3.11+ (for local development)
- **Node.js**: 18+ (for frontend development)

### Required Tools

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version
```

---

## Local Development

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/djny45/ANT-AI.git
   cd ANT-AI
   ```

2. **Create environment file**:
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   nano .env
   ```

3. **Install dependencies**:
   ```bash
   # Backend
   cd backend
   pip install -r requirements.txt
   cd ..

   # Frontend
   cd website
   npm install
   cd ..
   ```

4. **Start development servers**:
   ```bash
   # Backend (Terminal 1)
   python -m uvicorn ANT_X_OS.api.server:app --reload --host 0.0.0.0 --port 8000

   # Frontend (Terminal 2)
   cd website
   npm run dev

   # Nginx (Terminal 3 - optional)
   docker run --rm -v $(pwd)/devops/nginx:/etc/nginx:ro -p 80:80 nginx:latest
   ```

5. **Access services**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - Nginx: http://localhost:80

---

## Docker Deployment

### Quick Start

1. **Prepare configuration**:
   ```bash
   cp env.example .env
   # Edit .env with your values
   nano .env
   ```

2. **Build and start services**:
   ```bash
   docker-compose up -d
   ```

3. **Verify services**:
   ```bash
   docker-compose ps
   docker-compose logs -f
   ```

4. **Access services**:
   - Frontend: http://localhost
   - Backend API: http://localhost/api
   - Prometheus: http://localhost:9090
   - Grafana: http://localhost:3001

### Individual Service Commands

```bash
# Start specific service
docker-compose up -d frontend

# Stop services
docker-compose stop

# Stop and remove containers
docker-compose down

# Remove volumes (caution: deletes data)
docker-compose down -v

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Execute command in running container
docker-compose exec backend bash
docker-compose exec frontend npm list
```

### Health Checks

```bash
# Check all services
docker-compose ps

# Manual health checks
curl http://localhost/health
curl http://localhost/api/health
curl http://localhost:9090/-/healthy
curl http://localhost:3001/api/health
```

---

## Production Deployment

### Architecture

```
┌─────────────────────────────────────────────┐
│         Load Balancer (Optional)            │
└──────────────┬──────────────────────────────┘
               │
┌──────────────┴──────────────────────────────┐
│             Nginx Reverse Proxy             │
│    (SSL/TLS, Rate Limiting, Caching)       │
└──────────────┬──────────────────────────────┘
               │
       ┌───────┴────────┐
       │                │
   ┌───▼────┐      ┌────▼───┐
   │Frontend │      │Backend  │
   │ (Node.js)      │(FastAPI)│
   └────────┘      └────┬────┘
                        │
          ┌─────────────┼─────────────┐
          │             │             │
      ┌───▼──┐    ┌────▼────┐   ┌───▼──┐
      │Redis │    │Database │   │Files │
      └──────┘    └─────────┘   └──────┘
```

### Deployment Steps

#### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker and Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Install useful tools
sudo apt install -y git curl wget htop
```

#### 2. Repository Setup

```bash
# Clone repository
git clone https://github.com/djny45/ANT-AI.git
cd ANT-AI

# Create necessary directories
mkdir -p data/{knowledge_hive,postgres}
mkdir -p logs/{nginx,prometheus,grafana}
```

#### 3. Configuration

```bash
# Create production .env
cat > .env << EOF
ANT_API_KEY=$(openssl rand -hex 32)
ANT_ALLOWED_ORIGINS=https://yourdomain.com
ANT_MEMORY_DATABASE_URL=postgresql://user:password@postgres:5432/ant_ai
NODE_ENV=production
NEXT_PUBLIC_API_URL=https://yourdomain.com/api
GRAFANA_PASSWORD=$(openssl rand -base64 12)
JWT_SECRET_KEY=$(openssl rand -hex 32)
EOF

chmod 600 .env
```

#### 4. SSL/TLS Configuration

```bash
# Create SSL directory
mkdir -p devops/nginx/ssl

# Option A: Using Let's Encrypt (Recommended)
sudo apt install -y certbot python3-certbot-nginx

sudo certbot certonly --standalone \
  -d yourdomain.com \
  -d www.yourdomain.com \
  -m your-email@example.com \
  --agree-tos

# Copy certificates
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem devops/nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem devops/nginx/ssl/key.pem
sudo chown $USER:$USER devops/nginx/ssl/*

# Option B: Using self-signed certificate (Testing only)
openssl req -x509 -newkey rsa:4096 -keyout devops/nginx/ssl/key.pem \
  -out devops/nginx/ssl/cert.pem -days 365 -nodes
```

#### 5. Update Nginx Configuration

Enable HTTPS in `devops/nginx/conf.d/default.conf`:

```nginx
# Uncomment HTTPS block and update domain
server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    # ... rest of configuration
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}
```

#### 6. Start Services

```bash
# Pull latest images
docker-compose pull

# Start services in background
docker-compose up -d

# Watch logs
docker-compose logs -f

# Wait for services to be healthy
sleep 30
docker-compose ps
```

#### 7. Database Initialization (if using PostgreSQL)

```bash
# Add PostgreSQL to docker-compose.yml first, then:
docker-compose exec backend python -m alembic upgrade head
```

### Production Monitoring

#### Prometheus Setup

Create `devops/prometheus/prometheus.yml`:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'backend'
    static_configs:
      - targets: ['backend:8000']
    metrics_path: '/metrics'
```

#### Grafana Setup

1. Access Grafana: http://yourdomain.com/grafana/
2. Login with credentials from `.env`
3. Add Prometheus data source: `http://prometheus:9090`
4. Import dashboards from `devops/grafana/provisioning/dashboards/`

### Backup & Recovery

```bash
# Backup volumes
docker-compose exec -T backend tar czf - /app/data > backup-$(date +%Y%m%d).tar.gz

# Backup database
docker-compose exec -T postgres pg_dump -U postgres ant_ai > backup-db-$(date +%Y%m%d).sql

# Restore from backup
tar xzf backup-YYYYMMDD.tar.gz
docker-compose exec -T postgres psql -U postgres ant_ai < backup-db-YYYYMMDD.sql
```

---

## Configuration

### Environment Variables

See `env.example` for all available configuration options.

### Key Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ANT_API_KEY` | Required | API authentication key |
| `ANT_ALLOWED_ORIGINS` | localhost | CORS allowed origins |
| `ANT_MEMORY_DATABASE_URL` | sqlite | Database connection string |
| `NODE_ENV` | production | Node environment |
| `JWT_SECRET_KEY` | Required | JWT signing key |
| `GRAFANA_PASSWORD` | admin | Grafana admin password |

### Rate Limiting

Configure in `devops/nginx/nginx.conf`:

```nginx
limit_req_zone $binary_remote_addr zone=general_limit:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=100r/s;
```

---

## Monitoring & Observability

### Prometheus Metrics

Backend metrics available at: `http://localhost:8000/metrics`

Key metrics:
- `http_requests_total`
- `http_request_duration_seconds`
- `python_gc_collections_total`
- `process_resident_memory_bytes`

### Grafana Dashboards

Pre-built dashboards included for:
- System Resources
- API Performance
- Error Rates
- Request Latency

### Log Aggregation

View combined logs:
```bash
docker-compose logs -f --tail=100
```

---

## Troubleshooting

### Service Won't Start

```bash
# Check logs
docker-compose logs -f <service-name>

# Inspect container
docker-compose exec <service-name> bash

# Check port conflicts
sudo netstat -tulpn | grep LISTEN
```

### API Returns 502 Bad Gateway

```bash
# Check backend health
docker-compose exec backend curl http://localhost:8000/health

# Restart backend
docker-compose restart backend

# Check Nginx logs
docker-compose logs nginx
```

### Database Connection Errors

```bash
# Verify database is running
docker-compose ps postgres

# Check connection string in .env
docker-compose exec backend python -c "import os; print(os.getenv('ANT_MEMORY_DATABASE_URL'))"

# Test connection
docker-compose exec postgres psql -U postgres -c "SELECT version();"
```

### High Memory Usage

```bash
# Check Docker stats
docker stats

# Reduce container limits in docker-compose.yml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 2G
        reservations:
          memory: 1G
```

### Permission Issues

```bash
# Fix file permissions
sudo chown -R $USER:$USER data logs

# Fix docker socket permissions
sudo usermod -aG docker $USER
newgrp docker
```

---

## Security Checklist

- [ ] Change all default passwords
- [ ] Set strong `ANT_API_KEY`
- [ ] Enable SSL/TLS certificates
- [ ] Restrict `ANT_ALLOWED_ORIGINS`
- [ ] Configure firewall rules
- [ ] Enable authentication on Prometheus/Grafana
- [ ] Set up log rotation
- [ ] Regular backups enabled
- [ ] Update all base images monthly
- [ ] Review security audit logs

---

## Support & Documentation

- GitHub Issues: https://github.com/djny45/ANT-AI/issues
- Documentation: https://github.com/djny45/ANT-AI/docs
- Security Policy: See SECURITY.md

---

**Last Updated**: 2026-09-02
**Version**: 1.0
