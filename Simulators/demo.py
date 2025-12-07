from Simulators.SimulatorMotor import SimulatorMotor


def main():
    headless = False         # True == no graphics
    single_run = True        # True --> Debug 1 episode

    farol_level1 = "Levels/farol_level1.txt"
    farol_level2 = "Levels/farol_level2.txt"
    foraging_level1 = "Levels/foraging_level1.txt"
    foraging_level2 = "Levels/foraging_level2.txt"

    simulator_farol = SimulatorMotor.create(foraging_level1, headless=headless, single_run=single_run) # TODO - test_mode=True
    simulator_farol.execute()

if __name__ == "__main__":
    main()