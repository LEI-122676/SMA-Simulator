from Simulators.SimulatorMotor import SimulatorMotor
from visualization.visualize import visualize_graphs


def main():

    MODE = "DUMB"       # "TRAIN" or "TEST" or "DUMB"

    simple_farol = "Levels/simple_farol.txt"
    simple_foraging = "Levels/simple_foraging.txt"
    farol_level1 = "Levels/farol_level1.txt"
    farol_level2 = "Levels/farol_level2.txt"
    farol_level3 = "Levels/farol_level3.txt"
    farol_level4 = "Levels/farol_level4.txt"
    farol_level5 = "Levels/farol_level5.txt"
    foraging_level1 = "Levels/foraging_level1.txt"
    foraging_level2 = "Levels/foraging_level2.txt"
    foraging_level3 = "Levels/foraging_level3.txt"
    foraging_level4 = "Levels/foraging_level4.txt"

    training_map = farol_level1
    testing_map = farol_level1

    if MODE == "DUMB":
        print(f"--- MODE: DUMB (Heuristic) on {testing_map} ---")
        # We use 'single_run=True' so it just plays one episode
        # The SimulatorMotor.fixed_policy() method handles the legacy logic
        simulator = SimulatorMotor.create(testing_map, headless=False, single_run=True)
        simulator.execute(method="fixed_policy")

    elif MODE == "TRAIN":
        print(f"--- MODE: TRAIN (Neuroevolution) on {training_map} ---")
        simulator = SimulatorMotor.create(training_map, headless=True, single_run=False)
        simulator.execute(method="evolutionary")
        visualize_graphs(simulator, outdir="results")

    elif MODE == "TEST":
        print(f"--- MODE: TEST (Best Neural Network) on {testing_map} ---")
        # Note: We initialize with testing_map to ensure dimensions match if visual replay is needed
        simulator = SimulatorMotor.create(testing_map, headless=False, single_run=True)
        simulator.test(map_file=testing_map)


if __name__ == "__main__":
    main()