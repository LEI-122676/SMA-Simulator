from Simulators.SimulatorMotor import SimulatorMotor


def main():
    # Toggle headless here:
    #   True     =    No graphics (faster, no replay)
    #   False    =    Show graphics (visual replay of best agent)
    run_headless = False

    simulator_farol = SimulatorMotor.create("Levels/foraging_level2.txt", headless=run_headless, single_run=True) # TODO - test_mode=True
    simulator_farol.execute()

if __name__ == "__main__":
    main()