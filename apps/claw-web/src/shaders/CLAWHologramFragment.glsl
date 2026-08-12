uniform float uTime;
void main(){
 float pulse=0.65+sin(uTime*3.0)*0.15;
 vec3 glow=vec3(1.0,0.35,0.02)*pulse;
 gl_FragColor=vec4(glow,0.85);
}