from Simulators.SimulatorMotor import SimulatorMotor
from visualization.visualize import visualize_graphs


def main():
    headless = True     # True == no graphics
    single_run = False  # True --> Debug 1 episode

    # 1. Choose if you want to TRAIN or TEST
    MODE = "TEST"  # "TRAIN" or "TEST"

    # 2. Select Map
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

    # --- CONFIGURATION ---
    training_map = foraging_level3
    testing_map = foraging_level3

    if MODE == "TRAIN":
        print(f"--- MODE: TRAIN on {training_map} ---")
        simulator = SimulatorMotor.create(training_map, headless=headless, single_run=single_run)
        simulator.execute()
        visualize_graphs(simulator, outdir="results")

    elif MODE == "TEST":
        print(f"--- MODE: TEST on {testing_map} ---")
        # Note: We initialize with testing_map to ensure dimensions match if visual replay is needed
        simulator = SimulatorMotor.create(testing_map, headless=False, single_run=True)
        simulator.test(map_file=testing_map)



if __name__ == "__main__":
    main()