from Simulator.SimulatorMotor import SimulatorMotor


def main():
    simulator_farol = SimulatorMotor.create("example_file_farol.txt")
    simulator_farol.execute()

if __name__ == "__main__":
    main()