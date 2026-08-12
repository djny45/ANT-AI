uniform float uTime;
void main(){
 vec3 pos=position;
 float wave=sin(uTime*2.0+position.y*8.0)*0.002;
 pos+=normal*wave;
 gl_Position=projectionMatrix*modelViewMatrix*vec4(pos,1.0);
}