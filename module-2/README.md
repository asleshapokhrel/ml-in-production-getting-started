# Module 2 practice 

## MinIO deployment
### Local
``` 
curl -O https://dl.min.io/server/minio/release/linux-amd64/minio

chmod +x minio

./minio server /path_to_data```
```

To access minio UI locally vsit `http://127.0.0.1:9000 (Username: minioadmin, Password: minioadmin`


### Docker
```
cd minio-docker

docker build . -t asleshapokhrel/minio-docker:latest 

docker run -p 9001:9001 asleshapokhrel/minio-docker:latest

```
To access minio UI vsit `http://127.0.0.1:9000 (Username: minioadmin, Password: minioadmin`

### Kubernetes
```
cd minio-k8s

kind create cluster --name minio

kubectl create -f minio-k8s/minio-standalone.yaml

kubectl port-forward --address=0.0.0.0 pod/minio 9000:9000
kubectl port-forward --address=0.0.0.0 pod/minio 9001:9001
```
To access minio UI vsit `http://127.0.0.1:9000`

