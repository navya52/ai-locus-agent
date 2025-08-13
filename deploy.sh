#!/bin/bash

# AI Locus Agent Deployment Script
# Version: 1.0.0
# Purpose: Deploy and manage different versions of the AI Locus Agent

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="ai-locus-agent"
BACKUP_DIR="./backups"
LOG_FILE="./deploy.log"

# Function to log messages
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}" | tee -a "$LOG_FILE"
    exit 1
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}" | tee -a "$LOG_FILE"
}

info() {
    echo -e "${BLUE}[INFO] $1${NC}" | tee -a "$LOG_FILE"
}

# Function to check if Git is available
check_git() {
    if ! command -v git &> /dev/null; then
        error "Git is not installed. Please install Git first."
    fi
}

# Function to check current version
get_current_version() {
    if git describe --tags --exact-match 2>/dev/null; then
        return 0
    else
        echo "development"
        return 1
    fi
}

# Function to list available versions
list_versions() {
    log "Available versions:"
    git tag --sort=-version:refname | head -10
    echo ""
    log "Current version: $(get_current_version)"
}

# Function to create backup
create_backup() {
    local version=$1
    local backup_path="$BACKUP_DIR/backup_${version}_$(date +%Y%m%d_%H%M%S)"
    
    log "Creating backup: $backup_path"
    mkdir -p "$BACKUP_DIR"
    
    # Create backup of current state
    tar -czf "${backup_path}.tar.gz" \
        --exclude='.git' \
        --exclude='node_modules' \
        --exclude='venv' \
        --exclude='__pycache__' \
        --exclude='*.log' \
        .
    
    log "Backup created: ${backup_path}.tar.gz"
}

# Function to deploy specific version
deploy_version() {
    local version=$1
    
    log "Deploying version: $version"
    
    # Check if version exists
    if ! git tag | grep -q "^$version$"; then
        error "Version $version does not exist. Use 'list' to see available versions."
    fi
    
    # Create backup of current state
    create_backup "$(get_current_version)"
    
    # Checkout the specific version
    log "Checking out version: $version"
    git checkout "$version" || error "Failed to checkout version $version"
    
    # Update dependencies
    log "Updating dependencies..."
    
    # Backend dependencies
    if [ -f "backend/requirements.txt" ]; then
        log "Installing Python dependencies..."
        cd backend
        pip install -r requirements.txt || warning "Failed to install some Python dependencies"
        cd ..
    fi
    
    # Frontend dependencies
    if [ -f "frontend/package.json" ]; then
        log "Installing Node.js dependencies..."
        cd frontend
        npm install || warning "Failed to install some Node.js dependencies"
        cd ..
    fi
    
    log "Version $version deployed successfully!"
    log "To start the application:"
    echo "  Backend: cd backend && python3 app.py"
    echo "  Frontend: cd frontend && npm start"
}

# Function to rollback to previous version
rollback() {
    local target_version=$1
    
    if [ -z "$target_version" ]; then
        # Get the previous version
        target_version=$(git tag --sort=-version:refname | head -2 | tail -1)
        if [ -z "$target_version" ]; then
            error "No previous version found for rollback."
        fi
    fi
    
    log "Rolling back to version: $target_version"
    deploy_version "$target_version"
}

# Function to show deployment status
status() {
    log "=== AI Locus Agent Deployment Status ==="
    echo "Current Version: $(get_current_version)"
    echo "Git Branch: $(git branch --show-current)"
    echo "Last Commit: $(git log -1 --oneline)"
    echo "Working Directory: $(pwd)"
    echo ""
    
    # Check if services are running
    log "Service Status:"
    
    # Check backend
    if pgrep -f "python3 app.py" > /dev/null; then
        echo -e "${GREEN}✓ Backend (Flask): Running${NC}"
    else
        echo -e "${RED}✗ Backend (Flask): Not running${NC}"
    fi
    
    # Check frontend
    if pgrep -f "npm start" > /dev/null; then
        echo -e "${GREEN}✓ Frontend (React): Running${NC}"
    else
        echo -e "${RED}✗ Frontend (React): Not running${NC}"
    fi
    
    # Check gateway
    if pgrep -f "node server.js" > /dev/null; then
        echo -e "${GREEN}✓ Gateway (Node.js): Running${NC}"
    else
        echo -e "${YELLOW}⚠ Gateway (Node.js): Not running (optional)${NC}"
    fi
}

# Function to start services
start_services() {
    log "Starting AI Locus Agent services..."
    
    # Start backend
    log "Starting backend..."
    cd backend
    nohup python3 app.py > ../backend.log 2>&1 &
    cd ..
    
    # Start frontend
    log "Starting frontend..."
    cd frontend
    nohup npm start > ../frontend.log 2>&1 &
    cd ..
    
    # Optional: Start gateway
    if [ -f "gateway/package.json" ]; then
        log "Starting gateway..."
        cd gateway
        nohup npm start > ../gateway.log 2>&1 &
        cd ..
    fi
    
    sleep 3
    status
}

# Function to stop services
stop_services() {
    log "Stopping AI Locus Agent services..."
    
    pkill -f "python3 app.py" || true
    pkill -f "npm start" || true
    pkill -f "node server.js" || true
    
    log "Services stopped."
}

# Function to show help
show_help() {
    echo "AI Locus Agent Deployment Script"
    echo ""
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  deploy <version>    Deploy a specific version"
    echo "  rollback [version]  Rollback to previous version (or specific version)"
    echo "  list               List available versions"
    echo "  status             Show current deployment status"
    echo "  start              Start all services"
    echo "  stop               Stop all services"
    echo "  restart            Restart all services"
    echo "  backup             Create backup of current version"
    echo "  help               Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 deploy v1.0.0"
    echo "  $0 rollback"
    echo "  $0 status"
    echo "  $0 start"
}

# Main script logic
main() {
    # Check if we're in the right directory
    if [ ! -f "README.md" ] || [ ! -d "backend" ] || [ ! -d "frontend" ]; then
        error "Please run this script from the AI Locus Agent project root directory."
    fi
    
    # Check Git
    check_git
    
    # Parse command
    case "${1:-help}" in
        "deploy")
            if [ -z "$2" ]; then
                error "Please specify a version to deploy. Use 'list' to see available versions."
            fi
            deploy_version "$2"
            ;;
        "rollback")
            rollback "$2"
            ;;
        "list")
            list_versions
            ;;
        "status")
            status
            ;;
        "start")
            start_services
            ;;
        "stop")
            stop_services
            ;;
        "restart")
            stop_services
            sleep 2
            start_services
            ;;
        "backup")
            create_backup "$(get_current_version)"
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# Run main function
main "$@"
