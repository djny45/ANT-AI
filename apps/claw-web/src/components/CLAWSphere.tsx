import { Canvas, useFrame } from '@react-three/fiber';
import { Bloom, EffectComposer } from '@react-three/postprocessing';
import { useRef } from 'react';
import * as THREE from 'three';

function CoreSphere(){
  const ref = useRef<THREE.Mesh>(null);
  useFrame(({clock})=>{
    if(ref.current){
      const pulse = 1 + Math.sin(clock.elapsedTime * 2) * 0.03;
      ref.current.scale.setScalar(pulse);
      ref.current.rotation.y += 0.002;
    }
  });

  return <mesh ref={ref}>
    <sphereGeometry args={[1.4,128,128]}/>
    <meshStandardMaterial color="#ff6a00" emissive="#ff3300" emissiveIntensity={2.5} transparent opacity={0.75}/>
  </mesh>;
}

export default function CLAWSphere(){
 return <Canvas camera={{position:[0,0,5]}}>
   <ambientLight intensity={0.4}/>
   <pointLight color="#ff5500" intensity={8}/>
   <CoreSphere/>
   <EffectComposer><Bloom intensity={2}/></EffectComposer>
 </Canvas>;
}
