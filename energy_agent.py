import random

class AutonomousAgent:
    def __init__(self):
        self.threshold = 50  # energy usage threshold
        self.log_file = open("logs.txt", "w")  # create log file

    def log(self, message):
        print(message)
        self.log_file.write(message + "\n")

    def think(self):
        usage = {
            "Classroom A": random.randint(20, 100),
            "Classroom B": random.randint(20, 100)
        }
        self.log(f"[Think] Current usage: {usage}")
        return usage

    def plan(self, usage):
        actions = {}
        for room, value in usage.items():
            if value > self.threshold:
                actions[room] = "Turn OFF devices"
            else:
                actions[room] = "Keep devices ON"
        self.log(f"[Plan] Decisions: {actions}")
        return actions

    def execute(self, actions):
        for room, action in actions.items():
            self.log(f"[Execute] {room}: {action}")

    def review(self, usage, actions):
        results = {}
        for room, action in actions.items():
            if action == "Turn OFF devices":
                results[room] = "Saved energy"
            else:
                results[room] = "Normal usage"
        self.log(f"[Review] Outcomes: {results}")
        return results

    def update(self, results):
        for room, result in results.items():
            if result == "Saved energy":
                self.threshold -= 2
            else:
                self.threshold += 2
        self.log(f"[Update] New threshold: {self.threshold}")

    def close(self):
        self.log_file.close()

agent = AutonomousAgent()
for day in range(10):  # simulate 10 cycles
    agent.log(f"\n--- Day {day+1} ---")
    usage = agent.think()
    actions = agent.plan(usage)
    agent.execute(actions)
    results = agent.review(usage, actions)
    agent.update(results)

agent.close()
print("Logs saved to logs.txt")