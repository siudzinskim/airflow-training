provider "kubernetes" {
  config_path    = "~/.kube/config"
  config_context = "microk8s"
}

provider "helm" {
  kubernetes {
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
  version    = "1.15.0"
  namespace  = kubernetes_namespace.airflow.metadata[0].name
  # values     = [file("${path.root}/airflow-values.yaml")]
  values = [templatefile("${path.root}/airflow-values.yaml",
     {
       REPO_PATH = local.repo_path
     }
   )]
  # timeout    = "90"
  timeout    = "360"
}

data "external" "microk8s-web-token" {
  # program = ["bash", "-c", "echo {\\\"token\\\":\\\"`microk8s kubectl create token default`\\\"}"]
  program = ["bash", "-c", "echo {\\\"token\\\":\\\"`microk8s kubectl -n kube-system describe secret | grep token: | awk '{print $2}'`\\\"}"]
}

data "kubernetes_service_v1" "kubernetes-dashboard" {
  metadata {
    name = "kubernetes-dashboard"
    namespace = "kube-system"
  }
}

data "kubernetes_service_v1" "airflow-webserver" {
  metadata {
    name = "airflow-webserver"
    namespace = "airflow"
  }
}

locals {
  k8s_dashboard = data.kubernetes_service_v1.kubernetes-dashboard.spec != null ? "https://${data.kubernetes_service_v1.kubernetes-dashboard.spec[0].cluster_ip}:443" : ""
  airflow_webserver = data.kubernetes_service_v1.airflow-webserver.spec != null ? "http://${data.kubernetes_service_v1.airflow-webserver.spec[0].cluster_ip}:8080" : ""
}

output "kubernetes-dashboard" {
  # value = "https://${data.kubernetes_service_v1.kubernetes-dashboard.spec[0].cluster_ip}:443"
  value = local.k8s_dashboard
}

output "airflow-webserver" {
  # value = "http://${data.kubernetes_service_v1.airflow-webserver.spec[0].cluster_ip}:8080"
  value = local.airflow_webserver
}

output "kubernetes-dashboard-token" {
  value = data.external.microk8s-web-token.result["token"]
}