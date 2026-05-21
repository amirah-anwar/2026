from app.capacity_forecast import forecast_cluster


def is_cluster_at_risk(cluster, history, weeks=4):
    forecast = forecast_cluster(cluster.name, history)

    reasons = []

    if forecast["4_week_gpu"] > cluster.gpu_available:
        reasons.append(
            f"GPU exhaustion predicted: needs {forecast['4_week_gpu']}, has {cluster.gpu_available}"
        )

    if forecast["4_week_cpu"] > cluster.cpu_available:
        reasons.append(
            f"CPU exhaustion predicted: needs {forecast['4_week_cpu']}, has {cluster.cpu_available}"
        )

    return reasons


def recommend_migrations(clusters, workloads, history, recommend_cluster):
    migrations = []

    for workload in workloads:
        best_result, rejected, ranked_clusters = recommend_cluster(workload, clusters)

        if best_result is None:
            migrations.append({
                "workload": workload.name,
                "current_cluster": None,
                "status": "No valid cluster found",
                "migration_needed": False,
                "recommended_cluster": None,
                "reasons": ["No cluster currently satisfies workload constraints"]
            })
            continue

        current_cluster, current_score = best_result
        risk_reasons = is_cluster_at_risk(current_cluster, history)

        if not risk_reasons:
            migrations.append({
                "workload": workload.name,
                "current_cluster": current_cluster.name,
                "status": "Healthy",
                "migration_needed": False,
                "recommended_cluster": current_cluster.name,
                "reasons": ["Current placement is healthy for the next 4 weeks"]
            })
            continue

        safer_candidates = []

        for cluster, score in ranked_clusters:
            if cluster.name == current_cluster.name:
                continue

            candidate_risks = is_cluster_at_risk(cluster, history)

            if not candidate_risks:
                safer_candidates.append((cluster, score))

        if safer_candidates:
            safer_candidates.sort(key=lambda item: item[1], reverse=True)
            new_cluster, new_score = safer_candidates[0]

            migrations.append({
                "workload": workload.name,
                "current_cluster": current_cluster.name,
                "status": "At risk",
                "migration_needed": True,
                "recommended_cluster": new_cluster.name,
                "reasons": risk_reasons,
                "migration_reason": f"Move from {current_cluster.name} to {new_cluster.name} to avoid predicted capacity exhaustion"
            })
        else:
            migrations.append({
                "workload": workload.name,
                "current_cluster": current_cluster.name,
                "status": "At risk",
                "migration_needed": True,
                "recommended_cluster": None,
                "reasons": risk_reasons,
                "migration_reason": "No safer cluster is currently available"
            })

    return migrations