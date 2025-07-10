kubectl port-forward --address=0.0.0.0 svc/two-tier-app-service 5000:80

kubectl port-forward svc/prometheus-grafana -n monitoring 3000:80

kubectl get secret --namespace monitoring prometheus-grafana -o jsonpath="{.data.admin-password}" | base64 -d

kubectl port-forward svc/prometheus-kube-prometheus-prometheus -n monitoring 9090:9090

kubectl port-forward svc/kube-prometheus-stack-grafana -n monitoring --address 0.0.0.0 3000:80

kubectl port-forward --address=0.0.0.0 svc/two-tier-app-service 5000:80


scrape_configs:
  - job_name: 'flask-app'
    static_configs:
      - targets: ['<flask-app-ip>:5000']  # Replace <flask-app-ip> with your Flask app's IP
    metrics_path: '/metrics'


