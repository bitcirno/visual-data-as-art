#version 120

in vec3 fragmentColor;
in vec2 fragmentTexCoord;
uniform sampler2D imageTexture;

uniform float scale;  // diameter. maximum value is 1
uniform float smoothDist;
uniform vec4 color;

vec2 enter = vec2(0.5, 0.5);

void main() {
    float d = min(scale, 0.99);
    float r = d * 0.5;
    float l = length(fragmentTexCoord - enter);
    float c = 1 - smoothstep(max(0, r-smoothDist), min(1, r+smoothDist), l);
    vec4 col = color * c;
    col.a = c;
    gl_FragColor = col;
}
