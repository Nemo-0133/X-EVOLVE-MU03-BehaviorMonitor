from kernel.decision_core.mu02 import MU02DecisionCore
from kernel.behavior_monitor.mu03_monitor import MU03BehaviorMonitor

mc = MockMC()  # 你原本的 MC-01 mock
mu02 = MU02DecisionCore(mc)
mu03 = MU03BehaviorMonitor()

for i in range(30):
    packet = {"content": "一般任務", "delta_s": 0.5}
    result = mu02.evaluate_task(packet)
    mu03.record(result)

report = mu03.analyze()
print(report)
