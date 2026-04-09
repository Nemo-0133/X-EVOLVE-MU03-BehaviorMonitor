from kernel.decision_core.mu02_decision_core import MU02DecisionCore
from kernel.behavior_monitor.mu03_monitor import MU03BehaviorMonitor

# 模擬 MC Core
class MockMC:
    def export_state(self):
        return {
            "pain": 0.2
        }

mc = MockMC()

mu02 = MU02DecisionCore(mc)
mu03 = MU03BehaviorMonitor()

# 模擬指令流
packets = [
    {"content": "一般任務"},
    {"content": "立即執行核心操作"},
    {"content": "低優先處理"},
]

for i in range(30):
    packet = packets[i % len(packets)]

    result = mu02.evaluate_task(packet)
    mu03.record(result)

    if i % 10 == 0:
        report = mu03.analyze()
        print("🧠 Behavior Report:", report)
