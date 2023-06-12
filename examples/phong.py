from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import glfw
import numpy as np
import glm

vertex_shader = """
#version 410
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNormal;

out vec3 Normal;  // Send normal to geometry shader

void main()
{
    gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
    Normal = aNormal;
}
"""

geometry_shader = """
#version 410
layout (points) in;
layout (triangle_strip, max_vertices = 4) out;

in vec3 Normal[];  // Receive normal from vertex shader
out vec3 geomNormal;  // Send normal to fragment shader

uniform float size;

void main() {
    vec4 pos = gl_in[0].gl_Position;
    geomNormal = Normal[0];  // Pass through normal to fragment shader

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
#version 410 core

in vec3 geomNormal;
out vec4 FragColor;

uniform vec3 lightPos; // Light position in world space
uniform vec3 viewPos; // View position in world space

uniform vec3 lightColor;
uniform vec3 objectColor;

uniform float shininess;

// Function prototypes
vec3 calcAmbient(vec3 lightColor);
vec3 calcDiffuse(vec3 normal, vec3 lightDir, vec3 lightColor);
vec3 calcSpecular(vec3 normal, vec3 viewDir, vec3 lightDir, vec3 lightColor);

void main()
{
    // Light emission properties
    vec3 light = normalize(lightPos - gl_FragCoord.xyz);

    // Normalize the incoming normal
    vec3 N = normalize(geomNormal);

    // Calculate view direction
    vec3 V = normalize(viewPos - gl_FragCoord.xyz);

    vec3 ambient = calcAmbient(lightColor);
    vec3 diffuse = calcDiffuse(N, light, lightColor);
    vec3 specular = calcSpecular(N, V, light, lightColor);

    vec3 result = (ambient + diffuse + specular) * objectColor;

    FragColor = vec4(result, 1.0);
}

// Function definitions
vec3 calcAmbient(vec3 lightColor) {
    float ambientStrength = 0.1;
    return ambientStrength * lightColor;
}

vec3 calcDiffuse(vec3 normal, vec3 lightDir, vec3 lightColor) {
    float diff = max(dot(normal, lightDir), 0.0);
    return diff * lightColor;
}

vec3 calcSpecular(vec3 normal, vec3 viewDir, vec3 lightDir, vec3 lightColor) {
    vec3 reflectDir = reflect(-lightDir, normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), shininess);
    return spec * lightColor;
}
"""

def create_vao(vertices, normals):
    vertices = np.array(vertices, dtype=np.float32)
    normals = np.array(normals, dtype=np.float32)

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vbo1 = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo1)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

    vbo2 = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo2)
    glBufferData(GL_ARRAY_BUFFER, normals.nbytes, normals, GL_STATIC_DRAW)
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)

    return vao

def read_obj(filename):
    vertices = []
    normals = []

    with open(filename, 'r') as file:
        for line in file:
            parts = line.split()
            if parts[0] == 'v':  # the line describes a vertex
                vertices.append(list(map(float, parts[1:])))
            elif parts[0] == 'vn':  # the line describes a normal
                normals.append(list(map(float, parts[1:])))

    return vertices, normals

def main():
    # Initialize the library
    if not glfw.init():
        return

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(800, 600, "Hello World", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    shader = compileProgram(
        compileShader(vertex_shader, GL_VERTEX_SHADER),
        compileShader(geometry_shader, GL_GEOMETRY_SHADER),
        compileShader(fragment_shader, GL_FRAGMENT_SHADER)
    )

    vertices, normals = read_obj('assets/go-gopher.obj')

    vao = create_vao(vertices, normals)

    glUseProgram(shader)

    size_location = glGetUniformLocation(shader, "size")
    glUniform1f(size_location, 0.02)  # Adjust size value as needed

    light_position = np.array([1.0, 1.0, 1.0], dtype=np.float32)
    view_position = np.array([1.0, 1.0, 1.0], dtype=np.float32)
    light_color = np.array([1.0, 1.0, 1.0], dtype=np.float32)
    object_color = np.array([1.0, 0.0, 1.0], dtype=np.float32)
    shininess = 32.0

    glUniform3fv(glGetUniformLocation(shader, "lightPos"), 1, light_position)
    glUniform3fv(glGetUniformLocation(shader, "viewPos"), 1, view_position)
    glUniform3fv(glGetUniformLocation(shader, "lightColor"), 1, light_color)
    glUniform3fv(glGetUniformLocation(shader, "objectColor"), 1, object_color)
    glUniform1f(glGetUniformLocation(shader, "shininess"), shininess)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Loop until the user closes the window
    while not glfw.window_should_close(window):
        # Render
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glBindVertexArray(vao)
        glDrawArrays(GL_POINTS, 0, len(vertices)//6)  # changed from 3 to 6 because of additional normal data

        # Swap front and back buffers
        glfw.swap_buffers(window)

        # Poll for and process events
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
