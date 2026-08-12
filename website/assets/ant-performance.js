// ANT Performance Layer
// Lightweight device adaptation for free hosting deployment

const ANTPerformance = {
  quality: 'high',
  detect(){
    const lowPower = navigator.hardwareConcurrency && navigator.hardwareConcurrency <= 4;
    this.quality = lowPower ? 'optimized' : 'high';
    return this.quality;
  }
};

window.ANTPerformance = ANTPerformance;
