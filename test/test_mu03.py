from kernel.decision_core.mu02_decision_core import MU02DecisionCore
from kernel.behavior_monitor.mu03_monitor import MU03BehaviorMonitor

mu02 = MU02DecisionCore(mc)
mu03 = MU03BehaviorMonitor()

for i in range(30):
    packet = {"content": f"task_{i}", "delta_s": 0.5}
    
    result = mu02.evaluate_task(packet)
    mu03.record(result)

    if i % 10 == 0:
        report = mu03.analyze()
        print("🧠 MU-03 REPORT:", report)
