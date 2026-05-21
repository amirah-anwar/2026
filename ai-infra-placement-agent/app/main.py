from app.placement_engine import load_clusters, load_workloads, recommend_cluster
from app.capacity_forecast import (
    load_history,
    forecast_cluster
)

def main():
    clusters = load_clusters("data/clusters.json")
    workloads = load_workloads("data/workloads.json")
    history = load_history("data/utilization_history.json")

    print("\n")
    print("=" * 60)
    print("CAPACITY FORECAST")
    print("=" * 60)

    for cluster in clusters:

        forecast = forecast_cluster(
            cluster.name,
            history
        )

        print()

        print(cluster.name)

        print(
            "GPU growth/week:",
            forecast["gpu_growth_per_week"]
        )

        print(
            "4 week GPU forecast:",
            forecast["4_week_gpu"]
        )

        print(
            "12 week GPU forecast:",
            forecast["12_week_gpu"]
        )

        print()

        print(
            "CPU growth/week:",
            forecast["cpu_growth_per_week"]
        )

        print(
            "4 week CPU forecast:",
            forecast["4_week_cpu"]
        )

        print(
            "12 week CPU forecast:",
            forecast["12_week_cpu"]
        )


    for workload in workloads:
        best_result, rejected, ranked_clusters = recommend_cluster(workload, clusters)

        print("\n" + "=" * 60)
        print(f"Workload: {workload.name}")

        if best_result is None:
            print("Recommendation: No valid cluster found")
        else:
            best_cluster, best_score = best_result
            print(f"Recommendation: Place on {best_cluster.name}")
            print(f"Region: {best_cluster.region}")
            print(f"Score: {best_score}")
            print("Reason: Highest score among clusters that satisfy all constraints")

        print("\nRanked valid clusters:")
        for cluster, score in ranked_clusters:
            print(f"- {cluster.name}: {score}")

        print("\nRejected clusters:")
        for cluster, reasons in rejected:
            print(f"- {cluster.name}")
            for reason in reasons:
                print(f"  - {reason}")


if __name__ == "__main__":
    main()