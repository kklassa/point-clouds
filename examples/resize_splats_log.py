from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glfw
import numpy as np
from scipy.spatial import distance

vertex_shader = """
#version 410
layout (location = 0) in vec3 aPos;
layout (location = 1) in float aSize;
out float Size;
void main()
{
    gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
    Size = aSize;
}
"""

geometry_shader = """
#version 410
layout (points) in;
layout (triangle_strip, max_vertices = 4) out;
in float Size[];
uniform float baseSize;
void main() {
    vec4 pos = gl_in[0].gl_Position;
    float size = baseSize * Size[0];
    gl_Position = pos + vec4(-size, -size, 0.0, 0.0);
    EmitVertex();
    gl_Position = pos + vec4( size, -size, 0.0, 0.0);
    EmitVertex();
    gl_Position = pos + vec4(-size,  size, 0.0, 0.0);
    EmitVertex();
    gl_Position = pos + vec4( size,  size, 0.0, 0.0);
    EmitVertex();
    EndPrimitive();
}
"""

fragment_shader = """
#version 410
out vec4 FragColor;
void main()
{
    FragColor = vec4(1.0f, 0.0f, 0.0f, 1.0f);
}
"""

def create_vao(points, sizes):
    points = np.array(points, dtype=np.float32)
    sizes = np.array(sizes, dtype=np.float32)

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vbo1 = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo1)
    glBufferData(GL_ARRAY_BUFFER, points.nbytes, points, GL_STATIC_DRAW)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

    vbo2 = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo2)
    glBufferData(GL_ARRAY_BUFFER, sizes.nbytes, sizes, GL_STATIC_DRAW)
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 1, GL_FLOAT, GL_FALSE, 0, None)

    return vao

def calculate_distances(vertices: list) -> list:
    # reshape the array into a 2D array where each row represents a point
    points = np.array(vertices).reshape(-1, 3)

    # calculate the pairwise Euclidean distance between all points
    distance_matrix = distance.cdist(points, points, 'euclidean')

    # sort each row and take the second smallest element (i.e. the smallest non-zero distance)
    distances = np.sort(distance_matrix, axis=1)[:, 1]

    return distances

def scale_distances_log(distances, new_min, new_max):

    # calculate the old min and max
    original_min = distances.min()
    original_max = distances.max()

    # make sure there are no zero or negative values for the log scaling
    distances = np.log(distances - original_min + 0.0001)

    # calculate the new min and max after log transformation
    log_min = np.log(new_min)
    log_max = np.log(new_max)

    # scale the log-transformed distances
    scales = (log_max - log_min) * (distances - np.min(distances)) / (np.max(distances) - np.min(distances)) + log_min

    # convert back from log scale
    scales = np.exp(scales)

    return scales

def main():

    # Initialize the library
    if not glfw.init():
        return

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(800, 800, "Log Scaled Splats", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    shader = compileProgram(
        compileShader(vertex_shader, GL_VERTEX_SHADER),
        compileShader(geometry_shader, GL_GEOMETRY_SHADER),
        compileShader(fragment_shader, GL_FRAGMENT_SHADER)
    )

    points = [
        -0.5, -0.5, 0.0,
        0.5, -0.5, 0.0,
        0.0,  0.5, 0.0,
        0.1, 0.2, 0.3,
        0.4, 0.5, 0.6,
        -0.2, -0.3, -0.4
    ]

    distances = calculate_distances(points)

    sizes = scale_distances_log(distances, 0.5, 2.0)

    vao = create_vao(points, sizes)

    glUseProgram(shader)

    size_location = glGetUniformLocation(shader, "baseSize")
    glUniform1f(size_location, 0.05)  # Adjust size value as needed

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Render
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glBindVertexArray(vao)
        glDrawArrays(GL_POINTS, 0, len(points)//3)

        # Swap front and back buffers
        glfw.swap_buffers(window)

        # Poll for and process events
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
