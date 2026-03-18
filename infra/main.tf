provider "kubernetes" {
  config_path    = "~/.kube/config"
  config_context = "microk8s"
}

provider "helm" {
  kubernetes = {
    config_path = "~/.kube/config"
  }
}

resource "kubernetes_namespace" "airflow" {
  metadata {
    name = "airflow"
  }
}

resource "helm_release" "airflow" {
  repository = "https://airflow.apache.org"
  chart      = "airflow"
  name       = "airflow"
  version    = "1.19.0"
  namespace  = kubernetes_namespace.airflow.metadata[0].name
  values = [templatefile("${path.root}/airflow-values.yaml",
     {
       REPO_PATH = local.repo_path
     }
   )]
  # timeout    = "90"
  timeout    = "900"
}

data "external" "microk8s-web-token" {
  program = ["bash", "-c", "echo {\\\"token\\\":\\\"`microk8s kubectl -n kube-system describe secret | grep token: | awk '{print $2}'`\\\"}"]
}

data "external" "microk8s-web-token-web" {
  program = ["bash", "-c", "echo {\\\"token\\\":\\\"`microk8s kubectl -n kubernetes-dashboard create token default`\\\"}"]
}

data "kubernetes_service_v1" "kubernetes-dashboard" {
  metadata {
    name = "kubernetes-dashboard"
    namespace = "kube-system"
  }
}

data "kubernetes_service_v1" "kubernetes-dashboard-web" {
  metadata {
    name = "kubernetes-dashboard-kong-proxy"
    namespace = "kubernetes-dashboard"
  }
}

data "kubernetes_service_v1" "airflow-api-server" {
  metadata {
    name = "airflow-api-server"
    namespace = "airflow"
  }
}

locals {
  k8s_dashboard = data.kubernetes_service_v1.kubernetes-dashboard.spec != null ? "https://${data.kubernetes_service_v1.kubernetes-dashboard.spec[0].cluster_ip}:443" : ""
  k8s_dashboard_new = "https://${data.kubernetes_service_v1.kubernetes-dashboard-web.spec[0].cluster_ip}:443"
  airflow_api_server = data.kubernetes_service_v1.airflow-api-server.spec != null ? "http://${data.kubernetes_service_v1.airflow-api-server.spec[0].cluster_ip}:8080" : ""
}

output "kubernetes-dashboard" {
  value = local.k8s_dashboard != "" ? local.k8s_dashboard : local.k8s_dashboard_new
}

output "airflow-ui" {
  value = local.airflow_api_server
}

output "kubernetes-dashboard-token" {
  value = local.k8s_dashboard != "" ? data.external.microk8s-web-token.result["token"] : data.external.microk8s-web-token-web.result["token"]
}