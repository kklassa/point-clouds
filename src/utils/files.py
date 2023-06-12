def read_obj(filename: str) -> list:
    vertices = []

    with open(filename, 'r') as file:
        for line in file:
            parts = line.split()
            if parts[0] == 'v':  # the line describes a vertex
                vertices.append(list(map(float, parts[1:])))

    return vertices

def read_shader_file(filename: str) -> str:
    with open(filename, 'r') as file:
        return file.read()