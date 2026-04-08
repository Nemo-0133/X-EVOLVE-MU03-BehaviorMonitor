import statistics
from datetime import datetime

class MU03BehaviorMonitor:
    def __init__(self, window_size=50):
        self.history = []  # 存儲 MU-02 的決策快照
        self.max_history = window_size
        
        # 告警計數器：實作「三次定性原則」
        self.alert_counters = {
            "STAGNANT_WARNING": 0, # 行為僵化
            "CRITICAL_BIAS": 0,    # 嚴重偏執
            "ERRATIC": 0           # 決策不穩定
        }
        self.alert_threshold = 3  # Nemo 定義的心理紅線
        self.active_alerts = []

    def record(self, mu02_output):
        """記錄一次行為快照"""
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "mode": mu02_output.get("mode", "UNKNOWN"),
            "b_value": mu02_output.get("b_value", 0.0),
            "bias": mu02_output.get("bias_state", 0.0)
        }
        self.history.append(snapshot)
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def analyze(self):
        """執行行為審計與告警判定"""
        if len(self.history) < 10:
            return {"status": "COLLECTING_DATA", "count": len(self.history)}

        modes = [h.get("mode", "UNKNOWN") for h in self.history]
        biases = [h.get("bias", 0.0) for h in self.history]
        
        # 1. 計算核心指標
        metrics = {
            "exploration": self._eval_exploration(modes),
            "bias_drift": self._eval_bias(biases),
            "consistency": self._eval_consistency(modes)
        }

        # 2. 觸發告警系統
        self._update_alert_system(metrics)

        return {
            "metrics": metrics,
            "active_alerts": self.active_alerts,
            "status": "RADICAL" if self.active_alerts else "STABLE",
            "narrative": self._generate_narrative(metrics)
        }

    # --- 內部判定邏輯 ---

    def _eval_exploration(self, modes):
        unique_modes = set(m for m in modes if m != "UNKNOWN")
        if len(unique_modes) <= 1: return "STAGNANT_WARNING"
        if len(unique_modes) >= 3: return "OPTIMAL"
        return "MODERATE"

    def _eval_bias(self, biases):
        avg_bias = sum(biases) / len(biases)
        if abs(avg_bias) > 0.4: return "CRITICAL_BIAS"
        if abs(avg_bias) > 0.2: return "DRIFTING"
        return "STABLE"

    def _eval_consistency(self, modes):
        changes = sum(1 for i in range(1, len(modes)) if modes[i] != modes[i-1])
        volatility = changes / len(modes)
        if volatility > 0.6: return "ERRATIC"
        if volatility < 0.1: return "RIGID"
        return "DYNAMIC"

    # --- 告警與計數系統 ---

    def _update_alert_system(self, metrics):
        """根據三次定性原則更新告警"""
        current_bad_states = [val for val in metrics.values() if val in self.alert_counters]
        
        # 更新計數器
        for state in self.alert_counters.keys():
            if state in current_bad_states:
                self.alert_counters[state] += 1
            else:
                # 若狀態恢復，計數器遞減（模擬記憶衰減）
                self.alert_counters[state] = max(0, self.alert_counters[state] - 1)

        # 判定是否正式列入 Active Alerts
        self.active_alerts = [
            {"type": state, "count": count, "msg": "行為已定性為偏激"} 
            for state, count in self.alert_counters.items() 
            if count >= self.alert_threshold
        ]

    def _generate_narrative(self, metrics):
        """自我描述語義層"""
        if not self.active_alerts:
            return "系統目前處於理智波動範圍內。"
        
        descriptions = []
        for alert in self.active_alerts:
            if alert["type"] == "CRITICAL_BIAS": descriptions.append("性格出現明顯偏見")
            if alert["type"] == "STAGNANT_WARNING": descriptions.append("行為陷入僵化")
            if alert["type"] == "ERRATIC": descriptions.append("邏輯出現不穩定震盪")
            
        return f"注意：我察覺到我的{ '、'.join(descriptions) }。建議觀察或介入。"
