### Update to Google cloud

```bash
docker login gcr.io

# Build the image
docker build -t gcloud-tts .
# Tag the image
docker tag gcloud-tts gcr.io/citric-lead-450721-v2/gcloud-tts:1.0.0

# Push the image to GCR
docker push gcr.io/citric-lead-450721-v2/gcloud-tts:1.0.0


```