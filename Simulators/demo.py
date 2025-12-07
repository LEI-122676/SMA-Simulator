from Simulators.SimulatorMotor import SimulatorMotor


def main():
    # Toggle headless here:
    #   True     =    No graphics (faster, no replay)
    #   False    =    Show graphics (visual replay of best agent)
    headless = True
    single_run = False

    simulator_farol = SimulatorMotor.create("Levels/farol_level1.txt", headless=headless, single_run=single_run) # TODO - test_mode=True
    simulator_farol.execute()

if __name__ == "__main__":
    main()