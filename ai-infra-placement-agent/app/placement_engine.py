import json
from app.models import Cluster, Workload
from app.logger import logger


def load_clusters(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

    return [Cluster(**item) for item in data]


def load_workloads(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

    return [Workload(**item) for item in data]


def check_cluster(workload, cluster):
    reasons = []

    if cluster.cpu_available < workload.cpu_required:
        reasons.append(
            f"Not enough CPU: needs {workload.cpu_required}, has {cluster.cpu_available}"
        )

    if cluster.gpu_available < workload.gpu_required:
        reasons.append(
            f"Not enough GPU: needs {workload.gpu_required}, has {cluster.gpu_available}"
        )

    if cluster.memory_available < workload.memory_required:
        reasons.append(
            f"Not enough memory: needs {workload.memory_required}, has {cluster.memory_available}"
        )

    if cluster.latency_ms > workload.max_latency_ms:
        reasons.append(
            f"Latency too high: max allowed {workload.max_latency_ms}ms, cluster latency {cluster.latency_ms}ms"
        )

    if workload.preferred_region is not None and cluster.region != workload.preferred_region:
        reasons.append(
            f"Region mismatch: preferred {workload.preferred_region}, cluster is {cluster.region}"
        )

    return reasons


def calculate_score(workload, cluster):
    cpu_ratio = cluster.cpu_available / workload.cpu_required
    gpu_ratio = (
        cluster.gpu_available / workload.gpu_required
        if workload.gpu_required > 0
        else 1
    )
    memory_ratio = cluster.memory_available / workload.memory_required

    capacity_score = min(cpu_ratio, gpu_ratio, memory_ratio) * 40

    cost_score = (1 / cluster.cost_per_hour) * 30

    latency_score = (workload.max_latency_ms / cluster.latency_ms) * 30

    total_score = capacity_score + cost_score + latency_score

    return round(total_score, 2)


def recommend_cluster(workload, clusters):

    logger.info(
        f"Evaluating workload "
        f"{workload.name}"
    )
    accepted = []
    rejected = []

    for cluster in clusters:
        reasons = check_cluster(workload, cluster)

        if not reasons:
            score = calculate_score(workload, cluster)
            accepted.append((cluster, score))
        else:
            rejected.append((cluster, reasons))

    if not accepted:
        return None, rejected, []

    accepted.sort(key=lambda item: item[1], reverse=True)
    best_result = accepted[0]
    best_cluster, best_score = best_result

    logger.info(
        f"Selected "
        f"{best_cluster.name} "
        f"for "
        f"{workload.name} "
        f"with score {best_score}"
    )

    return best_result, rejected, accepted
