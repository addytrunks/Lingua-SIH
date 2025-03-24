import HandDetector from "$lib/hand-detector";
import type { HandLandmarkerResult } from "@mediapipe/tasks-vision";

export default class IslPredictor {
  private _pyodideContext?: any;
  private _handDetector?: HandDetector;
  async predict() {
    await this._handDetector?.detect();
  }
  async initialize(
    pyodideContext: any,
    videoElement: HTMLVideoElement,
    canvasElement: HTMLCanvasElement,
    callback: (results: any) => void
  ) {
    this._pyodideContext = pyodideContext;
    this._handDetector = new HandDetector(
      videoElement,
      canvasElement,
      async (results: HandLandmarkerResult) => {
        const [auxData, numHands] = [
          results.landmarks,
          results.landmarks.length,
        ];
        callback(await this._pyodideContext!.predictIsl(auxData, numHands));
      }
    );
    await this._handDetector.initialize();
  }

  close() {
    this._handDetector?.close();
  }
}
