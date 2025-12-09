from Simulators.SimulatorMotor import SimulatorMotor


def main():
    headless = False          # True == no graphics
    single_run = True        # True --> Debug 1 episode

    simple_farol = "Levels/simple_farol.txt"
    simple_foraging = "Levels/simple_foraging.txt"
    farol_level1 = "Levels/farol_level1.txt"
    farol_level2 = "Levels/farol_level2.txt"
    farol_level3 = "Levels/farol_level3.txt"
    farol_level_b = "Levels/farol_level_basic.txt"
    foraging_level1 = "Levels/foraging_level1.txt"
    foraging_level2 = "Levels/foraging_level2.txt"

    simulator_farol = SimulatorMotor.create(farol_level3, headless=headless, single_run=single_run) # TODO - test_mode=True
    simulator_farol.execute()

if __name__ == "__main__":
    main()