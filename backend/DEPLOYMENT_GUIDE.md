# AI Locus Agent - Production Deployment Guide

This guide provides step-by-step instructions for deploying the AI Locus Agent backend in a production environment with proper security, compliance, and monitoring.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Security Configuration](#security-configuration)
4. [Deployment Options](#deployment-options)
5. [Monitoring and Logging](#monitoring-and-logging)
6. [Backup and Recovery](#backup-and-recovery)
7. [Maintenance and Updates](#maintenance-and-updates)
8. [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements

- **CPU**: 4+ cores (8+ recommended for high load)
- **RAM**: 8GB+ (16GB+ recommended)
- **Storage**: 100GB+ SSD storage
- **Network**: High-speed internet connection
- **OS**: Ubuntu 20.04+ or CentOS 8+

### Software Requirements

- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **Python**: 3.11+
- **Redis**: 7.0+
- **Nginx**: 1.20+
- **SSL Certificate**: Valid SSL certificate

### Security Requirements

- **Firewall**: Configured firewall rules
- **VPN**: Secure remote access
- **Monitoring**: Security monitoring tools
- **Backup**: Automated backup system

## Environment Setup

### 1. Create Environment File

Create `.env` file with production settings:

```bash
# Application Configuration
FLASK_ENV=production
FLASK_DEBUG=False
API_VERSION=1.0.0

# Security Keys (Generate secure keys)
SECRET_KEY=your-very-secure-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
ENCRYPTION_KEY=your-encryption-key-here

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/ai_locus_agent

# Redis Configuration
REDIS_URL=redis://:password@localhost:6379/0
REDIS_PASSWORD=your-redis-password

# CORS Configuration
ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com

# Compliance Settings
GDPR_ENABLED=True
HIPAA_ENABLED=True
AUDIT_LOGGING_ENABLED=True
PHI_DETECTION_ENABLED=True

# Data Retention
DATA_RETENTION_DAYS=30
AUDIT_LOG_RETENTION_DAYS=90

# Rate Limiting
RATE_LIMIT_ENABLED=True
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60

# Monitoring
PROMETHEUS_ENABLED=True
GRAFANA_PASSWORD=your-grafana-password

# SSL Configuration
SSL_CERT_PATH=/etc/ssl/certs/yourdomain.crt
SSL_KEY_PATH=/etc/ssl/private/yourdomain.key
```

### 2. Generate Secure Keys

```bash
# Generate secret keys
python -c "import secrets; print(secrets.token_urlsafe(32))"
python -c "import secrets; print(secrets.token_hex(32))"

# Generate encryption key
openssl rand -hex 32
```

### 3. SSL Certificate Setup

```bash
# Using Let's Encrypt (recommended)
sudo apt-get install certbot
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Or use your own certificate
sudo cp your-certificate.crt /etc/ssl/certs/
sudo cp your-private-key.key /etc/ssl/private/
```

## Security Configuration

### 1. Firewall Configuration

```bash
# UFW Firewall Setup
sudo ufw enable
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH
sudo ufw allow ssh

# Allow HTTP/HTTPS
sudo ufw allow 80
sudo ufw allow 443

# Allow application ports
sudo ufw allow 5000  # Only if needed externally
sudo ufw allow 6379  # Redis (internal only)

# Deny other ports
sudo ufw deny 22  # If using different SSH port
```

### 2. Nginx Configuration

Create `/etc/nginx/sites-available/ai-locus-agent`:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security Headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';";

    # Rate Limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req zone=api burst=20 nodelay;

    # Proxy Configuration
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Health Check
    location /health {
        proxy_pass http://localhost:5000/api/v1/health;
        access_log off;
    }

    # Static Files (if any)
    location /static/ {
        alias /var/www/ai-locus-agent/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### 3. Application Security

```bash
# Create application user
sudo useradd -r -s /bin/false ai-locus-agent

# Set proper permissions
sudo chown -R ai-locus-agent:ai-locus-agent /opt/ai-locus-agent
sudo chmod -R 750 /opt/ai-locus-agent

# Configure log rotation
sudo tee /etc/logrotate.d/ai-locus-agent << EOF
/opt/ai-locus-agent/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 ai-locus-agent ai-locus-agent
    postrotate
        systemctl reload ai-locus-agent
    endscript
}
EOF
```

## Deployment Options

### Option 1: Docker Compose (Recommended)

```bash
# Clone repository
git clone https://github.com/your-org/ai-locus-agent.git
cd ai-locus-agent

# Create production environment file
cp .env.example .env
# Edit .env with production values

# Build and start services
docker-compose -f docker-compose.yml up -d

# Check status
docker-compose ps
docker-compose logs -f ai-locus-agent
```

### Option 2: Manual Deployment

```bash
# Install dependencies
sudo apt-get update
sudo apt-get install python3.11 python3.11-venv python3-pip nginx redis-server

# Create virtual environment
python3.11 -m venv /opt/ai-locus-agent/venv
source /opt/ai-locus-agent/venv/bin/activate

# Install Python packages
pip install -r requirements.txt

# Create systemd service
sudo tee /etc/systemd/system/ai-locus-agent.service << EOF
[Unit]
Description=AI Locus Agent Backend
After=network.target redis.service

[Service]
Type=exec
User=ai-locus-agent
Group=ai-locus-agent
WorkingDirectory=/opt/ai-locus-agent
Environment=PATH=/opt/ai-locus-agent/venv/bin
ExecStart=/opt/ai-locus-agent/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Start services
sudo systemctl daemon-reload
sudo systemctl enable ai-locus-agent
sudo systemctl start ai-locus-agent
```

### Option 3: Kubernetes Deployment

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-locus-agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-locus-agent
  template:
    metadata:
      labels:
        app: ai-locus-agent
    spec:
      containers:
      - name: ai-locus-agent
        image: your-registry/ai-locus-agent:latest
        ports:
        - containerPort: 5000
        env:
        - name: FLASK_ENV
          value: "production"
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: ai-locus-agent-secrets
              key: secret-key
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /api/v1/health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /api/v1/health
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5
```

## Monitoring and Logging

### 1. Application Monitoring

```bash
# Install monitoring tools
sudo apt-get install prometheus node-exporter grafana

# Configure Prometheus
sudo tee /etc/prometheus/prometheus.yml << EOF
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'ai-locus-agent'
    static_configs:
      - targets: ['localhost:5000']
    metrics_path: '/metrics'
    scrape_interval: 5s

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['localhost:9100']
EOF

# Start monitoring services
sudo systemctl enable prometheus node-exporter grafana-server
sudo systemctl start prometheus node-exporter grafana-server
```

### 2. Log Management

```bash
# Configure log aggregation
sudo apt-get install filebeat

# Configure Filebeat
sudo tee /etc/filebeat/filebeat.yml << EOF
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /opt/ai-locus-agent/logs/*.log
  fields:
    service: ai-locus-agent
  fields_under_root: true

output.elasticsearch:
  hosts: ["localhost:9200"]
  index: "ai-locus-agent-%{+yyyy.MM.dd}"

setup.kibana:
  host: "localhost:5601"
EOF

sudo systemctl enable filebeat
sudo systemctl start filebeat
```

### 3. Alerting Configuration

```bash
# Configure alerting rules
sudo tee /etc/prometheus/alerts.yml << EOF
groups:
- name: ai-locus-agent
  rules:
  - alert: HighErrorRate
    expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High error rate detected"
      description: "Error rate is {{ $value }}"

  - alert: ServiceDown
    expr: up{job="ai-locus-agent"} == 0
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "AI Locus Agent is down"
EOF
```

## Backup and Recovery

### 1. Database Backup

```bash
# Create backup script
sudo tee /opt/ai-locus-agent/scripts/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/backups/ai-locus-agent"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup application data
tar -czf $BACKUP_DIR/app_$DATE.tar.gz /opt/ai-locus-agent/

# Backup logs
tar -czf $BACKUP_DIR/logs_$DATE.tar.gz /opt/ai-locus-agent/logs/

# Backup configuration
cp /etc/nginx/sites-available/ai-locus-agent $BACKUP_DIR/nginx_$DATE.conf
cp /opt/ai-locus-agent/.env $BACKUP_DIR/env_$DATE

# Clean old backups (keep 30 days)
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
find $BACKUP_DIR -name "*.conf" -mtime +30 -delete
find $BACKUP_DIR -name "env_*" -mtime +30 -delete

echo "Backup completed: $DATE"
EOF

# Make executable and schedule
chmod +x /opt/ai-locus-agent/scripts/backup.sh
sudo crontab -e
# Add: 0 2 * * * /opt/ai-locus-agent/scripts/backup.sh
```

### 2. Recovery Procedures

```bash
# Recovery script
sudo tee /opt/ai-locus-agent/scripts/recover.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/backups/ai-locus-agent"
BACKUP_DATE=$1

if [ -z "$BACKUP_DATE" ]; then
    echo "Usage: $0 YYYYMMDD_HHMMSS"
    exit 1
fi

# Stop services
sudo systemctl stop ai-locus-agent nginx

# Restore application
tar -xzf $BACKUP_DIR/app_$BACKUP_DATE.tar.gz -C /

# Restore configuration
cp $BACKUP_DIR/nginx_$BACKUP_DATE.conf /etc/nginx/sites-available/ai-locus-agent
cp $BACKUP_DIR/env_$BACKUP_DATE /opt/ai-locus-agent/.env

# Restart services
sudo systemctl start ai-locus-agent nginx
sudo systemctl reload nginx

echo "Recovery completed for backup: $BACKUP_DATE"
EOF
```

## Maintenance and Updates

### 1. Update Procedures

```bash
# Update script
sudo tee /opt/ai-locus-agent/scripts/update.sh << 'EOF'
#!/bin/bash
set -e

echo "Starting AI Locus Agent update..."

# Backup current version
/opt/ai-locus-agent/scripts/backup.sh

# Pull latest code
cd /opt/ai-locus-agent
git pull origin main

# Update dependencies
source venv/bin/activate
pip install -r requirements.txt

# Run migrations (if any)
# python manage.py migrate

# Restart services
sudo systemctl restart ai-locus-agent
sudo systemctl reload nginx

echo "Update completed successfully"
EOF
```

### 2. Health Checks

```bash
# Health check script
sudo tee /opt/ai-locus-agent/scripts/health-check.sh << 'EOF'
#!/bin/bash

# Check application health
HEALTH_STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/api/v1/health)

if [ "$HEALTH_STATUS" != "200" ]; then
    echo "ERROR: Application health check failed (Status: $HEALTH_STATUS)"
    exit 1
fi

# Check disk space
DISK_USAGE=$(df / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 90 ]; then
    echo "WARNING: Disk usage is high ($DISK_USAGE%)"
fi

# Check memory usage
MEMORY_USAGE=$(free | awk 'NR==2{printf "%.2f", $3*100/$2}')
if (( $(echo "$MEMORY_USAGE > 90" | bc -l) )); then
    echo "WARNING: Memory usage is high ($MEMORY_USAGE%)"
fi

echo "Health check passed"
EOF
```

## Troubleshooting

### Common Issues

#### 1. Application Won't Start

```bash
# Check logs
sudo journalctl -u ai-locus-agent -f

# Check configuration
python -c "import app; print('Configuration OK')"

# Check dependencies
pip list | grep -E "(Flask|gunicorn)"
```

#### 2. High Memory Usage

```bash
# Check memory usage
ps aux | grep python
free -h

# Restart with fewer workers
# Edit gunicorn command to use fewer workers
```

#### 3. SSL Certificate Issues

```bash
# Check certificate validity
openssl x509 -in /etc/ssl/certs/yourdomain.crt -text -noout

# Renew Let's Encrypt certificate
sudo certbot renew

# Test SSL configuration
curl -I https://yourdomain.com
```

#### 4. Database Connection Issues

```bash
# Test database connection
python -c "import psycopg2; psycopg2.connect('your-connection-string')"

# Check Redis connection
redis-cli ping
```

### Performance Optimization

```bash
# Monitor performance
htop
iotop
netstat -tulpn

# Optimize nginx
sudo nano /etc/nginx/nginx.conf
# Add: worker_processes auto; worker_connections 1024;

# Optimize gunicorn
# Use more workers: --workers $(2 * num_cores + 1)
```

## Security Checklist

- [ ] Firewall configured and enabled
- [ ] SSL certificate installed and valid
- [ ] Security headers configured
- [ ] Rate limiting enabled
- [ ] Access logs enabled
- [ ] Regular security updates scheduled
- [ ] Backup system tested
- [ ] Monitoring and alerting configured
- [ ] Compliance logging enabled
- [ ] Incident response plan ready

## Conclusion

This deployment guide provides a comprehensive approach to deploying the AI Locus Agent in a production environment. Regular maintenance, monitoring, and updates are essential for maintaining security and compliance.

### Next Steps

1. Review and customize the configuration for your environment
2. Test the deployment in a staging environment
3. Implement monitoring and alerting
4. Schedule regular maintenance tasks
5. Document any environment-specific procedures
6. Train operations team on maintenance procedures
