#version 120

in vec3 fragmentColor;
in vec2 fragmentTexCoord;
uniform sampler2D imageTexture;

uniform float scale;  // diameter. maximum value is 1
uniform float smoothDist, alphaLerp;
uniform vec4 color;
uniform vec2 resolution;

vec2 enter = vec2(0.5, 0.5);

void main() {
    vec2 uv = fragmentTexCoord;
    float d = min(scale, 0.99);
    float r = d * 0.5;
    float l = length(uv - enter);
    float c = 1 - smoothstep(max(0.01, r-smoothDist), min(0.99, r+smoothDist), l);
    vec4 col = color;

    float inter = uv.x * uv.x;
    float alphaMul = smoothstep(0.08, 0.6, inter);
    alphaMul = mix(1, alphaMul, alphaLerp);

    col.a *= c * alphaMul;
    gl_FragColor = col;
}
