from Simulator.SimulatorMotor import SimulatorMotor


def main():
    simulator_farol = SimulatorMotor()
    file_path = "example_file_farol.txt"
    simulator_farol.create(file_path)
    simulator_farol.execute()

if __name__ == "__main__":
    main()