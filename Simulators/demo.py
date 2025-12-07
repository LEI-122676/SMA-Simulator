from Simulators.SimulatorMotor import SimulatorMotor


def main():
    headless = False         # True == no graphics
    single_run = True      # True --> Debug 1 episode

    simulator_farol = SimulatorMotor.create("Levels/farol_level1.txt", headless=headless, single_run=single_run) # TODO - test_mode=True
    simulator_farol.execute()

if __name__ == "__main__":
    main()