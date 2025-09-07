# Google Cloud Platform Deployment Guide

This guide will help you deploy your Stock Sentiment Analysis Flask app to Google Cloud Platform using multiple deployment options.

## Prerequisites

1. **Google Cloud Account**: Sign up at [Google Cloud Console](https://console.cloud.google.com/)
2. **Google Cloud SDK**: Install the [gcloud CLI](https://cloud.google.com/sdk/docs/install)
3. **Docker** (for containerized deployments): Install [Docker Desktop](https://www.docker.com/products/docker-desktop)

## Setup

1. **Create a new project** in Google Cloud Console
2. **Enable required APIs**:
   ```bash
   gcloud services enable appengine.googleapis.com
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable run.googleapis.com
   gcloud services enable containerregistry.googleapis.com
   ```

3. **Set your project ID**:
   ```bash
   gcloud config set project YOUR_PROJECT_ID
   ```

## Deployment Options

### Option 1: Google App Engine (Recommended for beginners)

App Engine is the easiest way to deploy your Flask app with minimal configuration.

1. **Deploy to App Engine**:
   ```bash
   gcloud app deploy
   ```

2. **View your app**:
   ```bash
   gcloud app browse
   ```

3. **Check logs**:
   ```bash
   gcloud app logs tail -s default
   ```

### Option 2: Cloud Run (Containerized deployment)

Cloud Run provides more control and better scaling options.

1. **Build and deploy using Cloud Build**:
   ```bash
   gcloud builds submit --config cloudbuild.yaml
   ```

2. **Or build and deploy manually**:
   ```bash
   # Build the container
   docker build -t gcr.io/YOUR_PROJECT_ID/stock-sentiment-analysis .
   
   # Push to Container Registry
   docker push gcr.io/YOUR_PROJECT_ID/stock-sentiment-analysis
   
   # Deploy to Cloud Run
   gcloud run deploy stock-sentiment-analysis \
     --image gcr.io/YOUR_PROJECT_ID/stock-sentiment-analysis \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --port 8080
   ```

### Option 3: Compute Engine (VM deployment)

For more control over the environment:

1. **Create a VM instance**:
   ```bash
   gcloud compute instances create stock-sentiment-vm \
     --image-family=ubuntu-2004-lts \
     --image-project=ubuntu-os-cloud \
     --machine-type=e2-micro \
     --zone=us-central1-a
   ```

2. **SSH into the VM and set up the app**:
   ```bash
   gcloud compute ssh stock-sentiment-vm --zone=us-central1-a
   ```

3. **Install dependencies and run the app** (inside the VM):
   ```bash
   sudo apt update
   sudo apt install python3-pip nginx
   pip3 install -r requirements.txt
   python3 app.py
   ```

## Configuration Files

### app.yaml
- Configures App Engine deployment
- Sets up health checks and scaling
- Defines environment variables

### cloudbuild.yaml
- Configures Cloud Build for automated deployments
- Builds Docker container and deploys to Cloud Run
- Includes build optimization settings

### Dockerfile
- Updated to work with GCP (removed Railway-specific configurations)
- Uses port 8080 (GCP standard)
- Optimized for production deployment

## Environment Variables

The app uses the following environment variables:
- `PORT`: Port number (defaults to 8080)
- `FLASK_ENV`: Set to 'production' for GCP deployment

## Health Checks

The app includes health check endpoints:
- `/health`: Returns app status and timestamp
- `/ping`: Simple ping endpoint

## Monitoring and Logging

1. **View logs in Cloud Console**:
   - App Engine: Go to App Engine > Services > Logs
   - Cloud Run: Go to Cloud Run > Select service > Logs
   - Compute Engine: Go to Compute Engine > VM instances > View logs

2. **Set up monitoring**:
   - Enable Cloud Monitoring for detailed metrics
   - Set up alerts for errors and performance issues

## Cost Optimization

1. **App Engine**: Pay only for what you use (good for low traffic)
2. **Cloud Run**: Pay per request (good for variable traffic)
3. **Compute Engine**: Fixed cost (good for consistent high traffic)

## Security Considerations

1. **Enable HTTPS**: All GCP services provide HTTPS by default
2. **Set up IAM**: Configure proper access controls
3. **Use secrets**: Store sensitive data in Secret Manager
4. **Enable VPC**: For additional network security

## Troubleshooting

### Common Issues:

1. **Port binding errors**: Ensure the app uses port 8080
2. **Memory issues**: Increase memory allocation in app.yaml
3. **Timeout errors**: Adjust timeout settings in gunicorn configuration
4. **Build failures**: Check Dockerfile and requirements.txt

### Useful Commands:

```bash
# Check deployment status
gcloud app versions list

# View detailed logs
gcloud app logs tail -s default --log-level=debug

# Test locally with App Engine
dev_appserver.py app.yaml

# Update deployment
gcloud app deploy --version=VERSION_ID
```

## Next Steps

1. Set up a custom domain
2. Configure SSL certificates
3. Set up CI/CD pipeline
4. Add monitoring and alerting
5. Implement proper logging and error handling

For more information, visit the [Google Cloud documentation](https://cloud.google.com/docs).
