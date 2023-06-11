#version 410 core

out vec4 fragColor;

uniform float transparency;
uniform float luminance;
uniform vec3 splatColor;

void main()
{
    vec3 finalColor = splatColor * luminance;
    float finalAlpha = transparency;
    fragColor = vec4(finalColor, finalAlpha);
}