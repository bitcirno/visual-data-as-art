#version 330 core

//Provided by the pygame_shaders library. Do not modify...
in vec3 fragmentColor;
in vec2 fragmentTexCoord;
uniform sampler2D imageTexture;

out vec4 color;

//Added some custom pparameters
uniform float time, fadeScale, rotVelocity, swingArms, density, moveSpeed;
uniform vec2 resolution;
uniform vec3 bgColor1, bgColor2;

float orb(vec3 p) {
    // orb time
    float t = time * .1;
    return length(p - vec3(
            sin(sin(t*.2)+t*.4) * 6.,
            1.+sin(sin(t*.5)+t*.2) *4.,
            12.+time+cos(t*.3)*8.));
}

// Reference:
// hurricane (@diatribes): https://www.shadertoy.com/view/tflBDM
void hurricane(out vec4 o, vec2 u) {
    float d,a,e,i,s,t = time;
    vec3  p = vec3(resolution, 0);

    // scale coords
    u = (u+u-p.xy)/p.y;

    // camera movement
    u += vec2(cos(t*.1)*.3, cos(t*.3)*.1);

    for(o*=i; i++<128.;

        // accumulate distance
        d += s = min(.03+.2*abs(s),e=max(.5*e, .01)) * density,

        // grayscale color and orb light
        o += 1./(s+e*3.))

        // noise loop start, march
        for (p = vec3(u*d,d+t), // p = ro + rd *d, p.z + t;

            // entity (orb)
            e = orb(p)+fadeScale,

            // spin by t, twist by p.z
            p.xy *= mat2(cos(rotVelocity*t + p.z/swingArms + vec4(0,33,11,0))),

            // mirrored planes 4 units apart
            s = 4. - abs(p.y),

            // noise starts at .8 up to 32., grow by a+=a
            a = .8; a < 32.; a += a)

            // apply turbulence
            p += cos(.7*t+p.yzx)*.2,

            // apply noise
            s -= abs(dot(sin(moveSpeed*t+p * a ), .6+p-p)) / a;

    // tanh tonemap, brightness, light off-screen
    o = tanh(o/1e1);
}

void main() {
    vec4 hurricane_col;
    hurricane(hurricane_col, gl_FragCoord.xy);

    vec2 uv = gl_FragCoord.xy / resolution;
    vec4 bg_gradient = vec4(mix(bgColor1, bgColor2, uv.x), 1);
    vec4 col = hurricane_col * hurricane_col.r + bg_gradient * (1 - bg_gradient.r);
    gl_FragColor = col;
}
