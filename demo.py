# demo.py
from Agent import Agent
from Map import Map
from Observation import Observation


def main():
    # Mapa  10x10 para testar o comportamento básico dos agentes.
    env = Map(width=10, height=10)

    agents = [
        Agent(id=0),
        Agent(id=1),
        Agent(id=2),
        Agent(id=3),
        Agent(id=4),
        Agent(id=5),
        Agent(id=6),
        Agent(id=7),
        Agent(id=8),
    ]

    # Necessário associar a um env
    for a in agents:
        a.env = env

    # TODO : Agentes podem estar na mesma posição inicial?
    for a in agents:
        env.positions[a.id] = (0, 0)

    print("=== Initial Observations ===")
    for a in agents:
        obs = env.observationFor(a)
        print(f"Agent {a.id} starts at {obs.positions}")

    print("\n=== Running 20 manual steps ===")
    for step in range(20):
        print(f"\n--- Step {step} ---")

        for a in agents:
            action = a.act()

            env.act(action, a)

            obs = env.observationFor(a)

            # estando a forçar as ações dos agentes,
            # é preciso fazer o tracking da exploração do agente.
            a.behavior.add(obs.positions)
            a.path.append(obs.positions)

            print(f"Agent {a.id} moved {action} → new pos {obs.positions}")

    print("\n=== Final Positions ===")
    for a in agents:
        obs = env.observationFor(a)

        print(f"Agent {a.id} final position: {obs.positions}")

        print(f"  Unique cells visited: {len(a.behavior)}")


if __name__ == "__main__":
    main()
