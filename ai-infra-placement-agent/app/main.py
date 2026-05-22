from fastapi import FastAPI
from app.placement_engine import load_clusters, load_workloads, recommend_cluster
from app.capacity_forecast import load_history, forecast_cluster
from app.self_healing import recommend_migrations
from app.ai_explainer import explain_recommendation

app = FastAPI(
    title="AI Infrastructure Planning & Placement Agent",
    description="Recommends infrastructure placement based on capacity, constraints, scoring, and forecasts.",
    version="1.0.0"
)


CLUSTERS_FILE = "data/clusters.json"
WORKLOADS_FILE = "data/workloads.json"
HISTORY_FILE = "data/utilization_history.json"


@app.get("/")
def root():
    return {
        "message": "AI Infrastructure Planning & Placement Agent is running"
    }


@app.get("/clusters")
def get_clusters():
    clusters = load_clusters(CLUSTERS_FILE)
    return clusters


@app.get("/workloads")
def get_workloads():
    workloads = load_workloads(WORKLOADS_FILE)
    return workloads


@app.get("/recommendations")
def get_recommendations():
    clusters = load_clusters(CLUSTERS_FILE)
    workloads = load_workloads(WORKLOADS_FILE)

    results = []

    for workload in workloads:
        best_result, rejected, ranked_clusters = recommend_cluster(
            workload,
            clusters
        )

        if best_result is None:
            recommendation = None
        else:
            best_cluster, best_score = best_result
            recommendation = {
                "cluster": best_cluster.name,
                "region": best_cluster.region,
                "score": best_score,
                "reason": "Highest score among clusters that satisfy all constraints"
            }

        results.append({
            "workload": workload.name,
            "recommendation": recommendation,
            "ranked_valid_clusters": [
                {
                    "cluster": cluster.name,
                    "region": cluster.region,
                    "score": score
                }
                for cluster, score in ranked_clusters
            ],
            "rejected_clusters": [
                {
                    "cluster": cluster.name,
                    "reasons": reasons
                }
                for cluster, reasons in rejected
            ]
        })

    return results


@app.get("/forecast")
def get_forecast():
    clusters = load_clusters(CLUSTERS_FILE)
    history = load_history(HISTORY_FILE)

    results = []

    for cluster in clusters:
        forecast = forecast_cluster(cluster.name, history)

        results.append({
            "cluster": cluster.name,
            "region": cluster.region,
            "forecast": forecast
        })

    return results


@app.get("/self-healing")
def get_self_healing_recommendations():
    clusters = load_clusters(CLUSTERS_FILE)
    workloads = load_workloads(WORKLOADS_FILE)
    history = load_history(HISTORY_FILE)

    return recommend_migrations(
        clusters,
        workloads,
        history,
        recommend_cluster
    )


@app.get("/recommendations/explained")
def get_explained_recommendations():
    clusters = load_clusters(CLUSTERS_FILE)
    workloads = load_workloads(WORKLOADS_FILE)

    results = []

    for workload in workloads:
        best_result, rejected, ranked_clusters = recommend_cluster(
            workload,
            clusters
        )

        if best_result is None:
            recommendation = None
        else:
            best_cluster, best_score = best_result
            recommendation = {
                "cluster": best_cluster.name,
                "region": best_cluster.region,
                "score": best_score
            }

        ranked_data = [
            {
                "cluster": cluster.name,
                "region": cluster.region,
                "score": score
            }
            for cluster, score in ranked_clusters
        ]

        rejected_data = [
            {
                "cluster": cluster.name,
                "reasons": reasons
            }
            for cluster, reasons in rejected
        ]

        explanation = explain_recommendation(
            workload.name,
            recommendation,
            ranked_data,
            rejected_data
        )

        results.append({
            "workload": workload.name,
            "recommendation": recommendation,
            "ranked_valid_clusters": ranked_data,
            "rejected_clusters": rejected_data,
            "ai_explanation": explanation
        })

    return results


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }