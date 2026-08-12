import React from 'react';
import { CLAWSphere } from './CLAWSphere';
import { CommandBar } from './CommandBar';
import { CLAWScene } from './CLAWScene';

export function CLAWCoreRuntime() {
  return (
    <main className="relative h-screen w-screen overflow-hidden bg-black">
      <CLAWScene>
        <CLAWSphere />
      </CLAWScene>
      <CommandBar />
    </main>
  );
}
