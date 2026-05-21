import json


def load_history(file_path):

    with open(file_path, "r") as file:
        return json.load(file)


def calculate_growth(history):

    if len(history) < 2:
        return 0

    total_growth = 0

    for i in range(1, len(history)):

        growth = history[i] - history[i - 1]

        total_growth += growth

    return total_growth / (len(history) - 1)


def forecast_resource(current, growth_rate, weeks):

    return current + (growth_rate * weeks)


def forecast_cluster(cluster_name, history):

    cluster = history[cluster_name]

    gpu_growth = calculate_growth(
        cluster["gpu_usage"]
    )

    cpu_growth = calculate_growth(
        cluster["cpu_usage"]
    )

    current_gpu = cluster["gpu_usage"][-1]
    current_cpu = cluster["cpu_usage"][-1]

    forecast_4w_gpu = forecast_resource(
        current_gpu,
        gpu_growth,
        4
    )

    forecast_4w_cpu = forecast_resource(
        current_cpu,
        cpu_growth,
        4
    )

    forecast_12w_gpu = forecast_resource(
        current_gpu,
        gpu_growth,
        12
    )

    forecast_12w_cpu = forecast_resource(
        current_cpu,
        cpu_growth,
        12
    )

    return {

        "gpu_growth_per_week":
            round(gpu_growth, 2),

        "cpu_growth_per_week":
            round(cpu_growth, 2),

        "4_week_gpu":
            round(forecast_4w_gpu),

        "4_week_cpu":
            round(forecast_4w_cpu),

        "12_week_gpu":
            round(forecast_12w_gpu),

        "12_week_cpu":
            round(forecast_12w_cpu)
    }