import { io, type Socket } from "socket.io-client";
import { ServerHelper } from "./consts";
export class ISLPredictionWSHandler {
  private _socket: Socket;
  constructor(predictionCallback: (prediction: string) => void) {
    this._socket = io(`http://${ServerHelper.ip}:5000`, {
      autoConnect: false,
      transports: ["websocket"],
      secure: false,
      withCredentials: true,
    });
    this._socket.on("prediction_feed", predictionCallback);
    this._socket.connect();
  }
  disconnect() {
    this._socket.disconnect();
  }
  sendLandmarks(landmarks: any) {
    this._socket.emit("predict_isl", landmarks);
  }
}
export class TextTISLWSHandler {
  private _socket: Socket;
  constructor(islCallback: (img: string) => void) {
    this._socket = io(`http://${ServerHelper.ip}:5000`, {
      autoConnect: false,
      transports: ["websocket"],
      secure: false,
      withCredentials: true,
    });
    this._socket.on("isl_feed", islCallback);
    this._socket.connect();
  }
  disconnect() {
    this._socket.disconnect();
  }
  sendText(text: string, category: string) {
    this._socket.emit("request_isl_feed", text, category);
  }
}
