# build-deploy.ps1

$VERSION = "v0.1.2"

Write-Host "`n>> Building Docker image..."
docker build --no-cache -t blackdranzer/data-sentinel:$VERSION .

if ($LASTEXITCODE -ne 0) {
    Write-Host "✘ Docker build failed. Exiting..."
    exit 1
}

Write-Host "`n>> Tagging image with version $VERSION..."
docker tag blackdranzer/data-sentinel:latest blackdranzer/data-sentinel:$VERSION

Write-Host "`n>> Pushing versioned tag..."
docker push blackdranzer/data-sentinel:$VERSION

if ($LASTEXITCODE -ne 0) {
    Write-Host "✘ Failed to push versioned image. Exiting..."
    exit 1
}

Write-Host "`n>> Pushing latest tag..."
docker push blackdranzer/data-sentinel:latest

if ($LASTEXITCODE -ne 0) {
    Write-Host "✘ Failed to push latest image. Exiting..."
    exit 1
}

Write-Host "`n>> Restarting Kubernetes deployment..."
kubectl rollout restart deployment data-sentinel-controller

Write-Host "`n>> Tailing logs from controller pod..."
kubectl logs -f deployment/data-sentinel-controller
