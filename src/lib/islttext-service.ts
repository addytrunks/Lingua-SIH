import { ServerHelper } from "./consts";

export type PredictionResult = {
  char: string;
};

export default class IslTextService {
  static headers = {
    Accept: "application/json",
    "Content-Type": "application/json",
  };
  static async predict(landmarks: any) {
    const res = await fetch(
      new URL(`api/predictisl`, ServerHelper.mainBaseURL),
      {
        method: "POST",
        body: JSON.stringify({ landmarks }),
        headers: this.headers,
      }
    );
    return (await res.json()) as PredictionResult;
  }
}
