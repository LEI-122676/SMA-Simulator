from Simulators.SimulatorMotor import SimulatorMotor


def main():
    simulator_farol = SimulatorMotor.create("Levels/simple_foraging.txt", False) # headless=False to show the world
    simulator_farol.execute()

if __name__ == "__main__":
    main()