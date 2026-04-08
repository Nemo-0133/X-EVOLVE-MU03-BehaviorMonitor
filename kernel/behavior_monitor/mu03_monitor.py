import statistics
from datetime import datetime

class MU03BehaviorMonitor:
    def __init__(self, window_size=50):
        self.history = []
        self.max_history = window_size

        self.status_flags = {
            "exploration": "INITIALIZING",
            "bias_drift": "INITIALIZING",
            "consistency": "INITIALIZING"
        }

    # === 記錄 MU-02 行為 ===
    def record(self, mu02_output):
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "mode": mu02_output.get("mode"),
            "b_value": mu02_output.get("b_value"),
            "bias": mu02_output.get("bias_state", 0),
            "action": mu02_output.get("action")
        }

        self.history.append(snapshot)
        if len(self.history) > self.max_history:
            self.history.pop(0)

    # === 核心分析 ===
    def analyze(self):
        size = len(self.history)

        if size < 10:
            return {
                "status": "COLLECTING_DATA",
                "progress": f"{size}/10",
                "confidence": "LOW"
            }

        modes = [h["mode"] for h in self.history if h["mode"]]
        biases = [h["bias"] for h in self.history]
        b_values = [h["b_value"] for h in self.history if h["b_value"] is not None]

        metrics = {
            "exploration": self._check_exploration(modes),
            "bias_drift": self._check_bias_drift(biases),
            "consistency": self._check_consistency(modes)
        }

        report = {
            "metrics": metrics,
            "confidence": self._confidence_score(size),
            "alerts": self._generate_alerts(metrics),
            "system_health": self._overall_health(metrics),
            "timestamp": datetime.now().isoformat()
        }

        self.status_flags.update(metrics)
        return report

    # === 指標計算 ===

    def _check_exploration(self, modes):
        diversity = len(set(modes))
        if diversity >= 3:
            return "OPTIMAL"
        elif diversity == 1:
            return "STAGNANT_WARNING"
        else:
            return "MODERATE"

    def _check_bias_drift(self, biases):
        avg_bias = sum(biases) / len(biases)

        if abs(avg_bias) > 0.4:
            return "CRITICAL_BIAS"
        elif abs(avg_bias) > 0.2:
            return "STOCHASTIC_DRIFT"
        else:
            return "CENTERED"

    def _check_consistency(self, modes):
        if len(modes) < 2:
            return "UNKNOWN"

        changes = sum(1 for i in range(1, len(modes)) if modes[i] != modes[i-1])
        volatility = changes / len(modes)

        if volatility > 0.6:
            return "ERRATIC"
        elif volatility < 0.1:
            return "RIGID"
        else:
            return "DYNAMIC_STABLE"

    # === 信心層（防誤判） ===

    def _confidence_score(self, size):
        if size < 20:
            return "LOW"
        elif size < 40:
            return "MEDIUM"
        else:
            return "HIGH"

    # === 告警系統（只提示，不干預） ===

    def _generate_alerts(self, metrics):
        alerts = []

        if metrics["bias_drift"] == "CRITICAL_BIAS":
            alerts.append({
                "type": "BIAS_ALERT",
                "level": "HIGH",
                "message": "系統偏見接近極值，建議檢查決策偏向。"
            })

        if metrics["consistency"] == "ERRATIC":
            alerts.append({
                "type": "STABILITY_ALERT",
                "level": "HIGH",
                "message": "決策行為波動過高，可能存在不穩定性。"
            })

        if metrics["exploration"] == "STAGNANT_WARNING":
            alerts.append({
                "type": "EXPLORATION_ALERT",
                "level": "MEDIUM",
                "message": "行為過於單一，可能失去探索能力。"
            })

        return alerts

    # === 系統健康評估 ===

    def _overall_health(self, metrics):
        if "CRITICAL_BIAS" in metrics.values() or "ERRATIC" in metrics.values():
            return "UNSTABLE"

        if "STAGNANT_WARNING" in metrics.values():
            return "DEGRADED"

        return "STABLE"
