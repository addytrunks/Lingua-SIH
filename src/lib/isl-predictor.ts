import HandDetector from "$lib/hand-detector";
import type { HandLandmarkerResult } from "@mediapipe/tasks-vision";
import IslTextService from "./islttext-service";
import { ISLPredictionWSHandler } from "./ws-handler";

export default class IslPredictor {
  private _handDetector?: HandDetector;
  private _wsHandler?: ISLPredictionWSHandler;
  async predict() {
    await this._handDetector?.detect();
  }
  async initialize(
    videoElement: HTMLVideoElement,
    canvasElement: HTMLCanvasElement,
    callback: (results: any) => void
  ) {
    this._wsHandler = new ISLPredictionWSHandler(callback);
    this._handDetector = new HandDetector(
      videoElement,
      canvasElement,
      async (results: HandLandmarkerResult) => {
        if (results.landmarks.length === 0) callback("");
        try {
          this._wsHandler?.sendLandmarks(results.landmarks);
        } catch (error) {
          callback("");
          console.group();
          console.log(`ISL Server Error`);
          console.log(error);
          console.groupEnd();
        }
      }
    );
    await this._handDetector.initialize();
  }

  close() {
    this._handDetector?.close();
  }
}
