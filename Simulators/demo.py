from Simulators.SimulatorMotor import SimulatorMotor


def main():
    simulator_farol = SimulatorMotor.create("Levels/farol_level1.txt", False) # headless=False to show the world
    simulator_farol.execute()

if __name__ == "__main__":
    main()