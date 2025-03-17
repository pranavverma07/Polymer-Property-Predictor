import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { useEffect, useRef } from 'react';
import * as THREE from 'three';

const MoleculeViewer = () => {
  const meshRef = useRef<THREE.Mesh>(null);

  useEffect(() => {
    if (meshRef.current) {
      meshRef.current.rotation.x = 0.5;
    }
  }, []);

  return (
    <div className="h-[400px] w-full rounded-lg bg-gray-900">
      <Canvas camera={{ position: [0, 0, 5] }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} />
        <mesh ref={meshRef}>
          <sphereGeometry args={[1, 32, 32]} />
          <meshStandardMaterial color="#00ff88" wireframe />
        </mesh>
        <OrbitControls enableZoom={true} />
      </Canvas>
    </div>
  );
};

export default MoleculeViewer;