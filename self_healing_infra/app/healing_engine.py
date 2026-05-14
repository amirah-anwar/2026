class SelfHealingEngine:

    def determine_actions(self, alerts):
        actions = []

        for alert in alerts:
            if (
                "Service is DOWN" in alert.message and
                alert.severity == "CRITICAL"
            ):
                actions.append({
                    "action": "restart_service",
                    "target": alert.service,
                    "priority": "HIGH",
                    "confidence": 0.95,
                })

        return actions
    
    def execute_actions(self, actions, simulator):
        execution_results = []
        for action in actions:
            if action["confidence"] < 0.8:
                execution_results.append({
                    "target": action["target"],
                    "status": "SKIPPED_LOW_CONFIDENCE"
                })
                continue

            if action["action"] == "restart_service":
                simulator.recover_service(action["target"])
                execution_results.append({
                    "target": action["target"],
                    "status": "RECOVERED",
                    "action_taken": "restart_service"
                })

        return execution_results