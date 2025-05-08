### Update to Google cloud

```bash
docker login gcr.io

# Build the image
docker build -t silk-vertex .
# Tag the image
docker tag silk-vertex gcr.io/citric-lead-450721-v2/silk-vertex:1.0.0

# Push the image to GCR
docker push gcr.io/citric-lead-450721-v2/silk-vertex:1.0.0


```