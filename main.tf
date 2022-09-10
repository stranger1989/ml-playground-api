terraform {
  required_providers {
    google = {
      version = "~> 4.0.0"
    }
    google-beta = {
      version = "~> 4.0.0"
    }
  }
}

provider "google" {
  credentials = file("./keyfile.json")

  project = var.project
  region  = var.region
  zone    = var.zone
}

provider "google-beta" {
  credentials = file("./keyfile.json")

  project = var.project
  region  = var.region
  zone    = var.zone
}

resource "google_artifact_registry_repository" "ml_playground_api" {
  provider      = google-beta
  location      = var.region
  repository_id = "ml-playground-api"
  description   = "ml playground api docker repository"
  format        = "DOCKER"
}

resource "null_resource" "default" {
  depends_on = [google_artifact_registry_repository.ml_playground_api]

  provisioner "local-exec" {
    command = "docker build --platform linux/amd64 -t ml-playground-api ."
  }
  provisioner "local-exec" {
    command = "docker tag ml-playground-api ${var.region}-docker.pkg.dev/${var.project}/ml-playground-api/image"
  }
  provisioner "local-exec" {
    command = "docker push ${var.region}-docker.pkg.dev/${var.project}/ml-playground-api/image"
  }
}

resource "google_cloud_run_service" "default" {
  name       = "ml-playground-api"
  location   = var.region
  depends_on = [null_resource.default]

  template {
    spec {
      containers {
        image = "${var.region}-docker.pkg.dev/${var.project}/ml-playground-api/image"
      }
    }
  }
  traffic {
    percent         = 100
    latest_revision = true
  }
}

data "google_iam_policy" "noauth" {
  binding {
    role = "roles/run.invoker"
    members = [
      "allUsers",
    ]
  }
}

resource "google_cloud_run_service_iam_policy" "noauth" {
  location = google_cloud_run_service.default.location
  project  = google_cloud_run_service.default.project
  service  = google_cloud_run_service.default.name

  policy_data = data.google_iam_policy.noauth.policy_data
}

locals {
  api_config_id_prefix     = "api"
  api_gateway_container_id = "api-gw"
  gateway_id               = "gw"
}

resource "google_api_gateway_api" "api_gw" {
  provider     = google-beta
  api_id       = local.api_gateway_container_id
  display_name = "ML Playground API Gateway"
  depends_on   = [google_cloud_run_service.default]
}

resource "google_api_gateway_api_config" "api_cfg" {
  provider             = google-beta
  api                  = google_api_gateway_api.api_gw.api_id
  api_config_id_prefix = local.api_config_id_prefix
  display_name         = "ML Playground Config"
  depends_on           = [google_api_gateway_api.api_gw]

  openapi_documents {
    document {
      path = "openapi.yaml"
      contents = base64encode(
        templatefile(
          "openapi.yaml",
          { APP_URL = google_cloud_run_service.default.status[0].url }
        )
      )
    }
  }
  lifecycle {
    create_before_destroy = true
  }
}

resource "google_api_gateway_gateway" "gw" {
  provider   = google-beta
  region     = var.region
  depends_on = [google_api_gateway_api_config.api_cfg]

  api_config = google_api_gateway_api_config.api_cfg.id

  gateway_id   = local.gateway_id
  display_name = "ML Playground Gateway"
}
