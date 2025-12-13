import random

from Agents.Agent import Agent

def read_file_parameters(allowed_params, file_name):
    
    
    # TODO : NOVO FORMATO DE CONFIGURAÇÃO EM MATRIZ

    allowed = {p: None for p in allowed_params}  # Dict of allowed keys

    try:
        with open(file_name, "r") as f:
            for line in f:

                # Clean and skip empty/comment lines
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    raise ValueError(f"Invalid line (no '='): {line}")

                key, value = line.split("=", 1)
                key = key.strip()

                if key not in allowed:
                    raise ValueError(f"Unexpected parameter in file: '{key}'")

                value = value.strip()

                # Try to convert to int or float
                if value.isdigit():
                    value = int(value)
                else:
                    try:
                        value = float(value)
                    except ValueError:
                        pass  # keep as string

                allowed[key] = value

    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_name}' does not exist")

    # Check for missing allowed parameters
    missing = [k for k, v in allowed.items() if v is None]
    if missing:
        raise ValueError(f"Missing required parameters: {missing}")

    return allowed

def read_matrix_file_with_metadata(file_name):
    ALLOWED_CHARS = {'.', 'E', 'N', 'S', 'W', 'F', 'C'}
    matrix = []

    try:
        with open(file_name, "r") as f:
            for line_number, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue

                if line.startswith("#"):
                    continue

                # Validate characters
                for char in line:
                    if char not in ALLOWED_CHARS:
                        raise ValueError(
                            f"Invalid character '{char}' on line {line_number}"
                        )

                matrix.append(list(line))

        if not matrix:
            raise ValueError("Matrix is empty")

        # Ensure all rows are same length
        row_length = len(matrix[0])
        for i, row in enumerate(matrix, start=1):
            if len(row) != row_length:
                raise ValueError(f"Row {i} has length {len(row)}, expected {row_length}")

        return matrix

    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_name}' does not exist")

def read_agent_config(file_name: str) -> dict:
    config = {}
    try:
        with open(file_name, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    raise ValueError(f"Invalid line in config: {line}")
                key, value = line.split("=", 1)
                config[key.strip()] = value.strip()
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Agent config file '{file_name}' does not exist")
