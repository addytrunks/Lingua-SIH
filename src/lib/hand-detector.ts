import {
  HandLandmarker,
  FilesetResolver,
  DrawingUtils,
  type HandLandmarkerOptions,
  type HandLandmarkerResult,
} from "@mediapipe/tasks-vision";

// https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task
const handLandmarkerOptions: HandLandmarkerOptions = {
  baseOptions: {
    modelAssetPath: `hands/hand_landmarker.task`,
    delegate: "GPU",
  },
  runningMode: "VIDEO",
  numHands: 2,
  minHandDetectionConfidence: 0.5,
  minTrackingConfidence: 0.5,
};

const handLandmarksCanvasDrawOptions = {
  connnectors: {
    color: "#00cc00",
    lineWidth: 5,
  },
  landmarks: {
    color: "#cc0000",
    lineWidth: 2,
    radius: 5,
  },
};

export default class HandDetector {
  private _videoElement: HTMLVideoElement;
  private _canvasElement: HTMLCanvasElement;
  private _canvasCtx?: CanvasRenderingContext2D;
  private _drawingUtils?: DrawingUtils;
  private _handLandmarker?: HandLandmarker;
  private _prevFrameTimeStamp = 0;
  private _hasInitialized = false;
  private _resultCallback: (results: HandLandmarkerResult) => void;

  constructor(
    videoElement: HTMLVideoElement,
    canvasElement: HTMLCanvasElement,
    resultCallback: (results: HandLandmarkerResult) => void
  ) {
    this._resultCallback = resultCallback;
    this._videoElement = videoElement;
    this._canvasElement = canvasElement;
    this._canvasElement.width = this._videoElement.offsetWidth;
    this._canvasElement.height = this._videoElement.offsetHeight;
    this._canvasCtx = this._canvasElement.getContext("2d") ?? undefined;
  }

  async initialize() {
    if (this._canvasCtx) this._drawingUtils = new DrawingUtils(this._canvasCtx);
    const vision = await FilesetResolver.forVisionTasks("/hands/wasm");
    this._handLandmarker = await HandLandmarker.createFromOptions(
      vision,
      handLandmarkerOptions
    );
    this._hasInitialized = true;
  }

  close() {
    this._handLandmarker?.close();
    this._drawingUtils?.close();
    this._hasInitialized = false;
  }

  async detect() {
    if (!this._hasInitialized) return;
    const currFrameTimeStamp = performance.now();
    if (
      !this._videoElement ||
      !this._handLandmarker ||
      currFrameTimeStamp / 10 <= this._prevFrameTimeStamp! / 10
    )
      return;
    this._handleResults(
      this._handLandmarker!.detectForVideo(
        this._videoElement,
        currFrameTimeStamp
      )
    );
    this._prevFrameTimeStamp = currFrameTimeStamp;
  }

  private _handleResults(results: HandLandmarkerResult) {
    if (!this._canvasCtx) return;
    this._canvasElement!.width = this._videoElement!.offsetWidth;
    this._canvasElement!.height = this._videoElement!.offsetHeight;
    this._canvasCtx.save();
    this._canvasCtx.clearRect(
      0,
      0,
      this._canvasElement.width,
      this._canvasElement.height
    );
    if (!results || results.handedness.length == 0) return;
    this._resultCallback(results);
    for (const landmarks of results.landmarks) {
      this._drawingUtils!.drawConnectors(
        landmarks as any,
        HandLandmarker.HAND_CONNECTIONS,
        handLandmarksCanvasDrawOptions.connnectors
      );
      this._drawingUtils!.drawLandmarks(
        landmarks as any,
        handLandmarksCanvasDrawOptions.landmarks
      );
    }
    this._canvasCtx.restore();
  }
}
