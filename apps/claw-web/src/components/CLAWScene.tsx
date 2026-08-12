import React from 'react';
import { Canvas } from '@react-three/fiber';
import { EffectComposer, Bloom } from '@react-three/postprocessing';
import { CLAWSphere } from './CLAWSphere';
import { ReflectiveFloor } from '../components/ReflectiveFloor';

export function CLAWScene() {
  return (
    <Canvas camera={{ position: [0, 0, 6], fov: 45 }}>
      <color attach="background" args={["#050505"]} />
      <ambientLight intensity={0.4} />
      <pointLight position={[0, 2, 3]} intensity={4} color="#ff6600" />
      <CLAWSphere />
      <ReflectiveFloor />
      <EffectComposer>
        <Bloom intensity={1.5} luminanceThreshold={0.1} />
      </EffectComposer>
    </Canvas>
  );
}
