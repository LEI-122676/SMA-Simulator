from Simulators.SimulatorMotor import SimulatorMotor


def main():
    # Toggle headless here:
    #   True     =    No graphics (faster, no replay)
    #   False    =    Show graphics (visual replay of best agent)
    run_headless = False

    simulator_farol = SimulatorMotor.create("Levels/farol_level1.txt", headless=run_headless)
    simulator_farol.execute()


if __name__ == "__main__":
    main()