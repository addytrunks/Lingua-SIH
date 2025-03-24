import { ServerHelper } from "./consts";

export type LanguageItem = [string, string];

export type TranslationResult = {
  audio: string;
  result: string;
  lang: string;
};

export type SigmlPreprocessorResult = {
  result: string[];
};
export type SummarizerResult = {
  summary: string;
};
export type Speech2TextResult = {
  text: string;
};
export type Text2ImageResult = {
  imgData: string;
};
export type Text2EmojiResult = {
  text: string;
};

export default class BeService {
  static headers = {
    Accept: "application/json",
    "Content-Type": "application/json",
  };
  static async summarize(text: string) {
    const res = await fetch(
      new URL(`api/summarize`, ServerHelper.mainBaseURL),
      {
        method: "POST",
        body: JSON.stringify({ text }),
        headers: this.headers,
      }
    );
    return (await res.json()) as SummarizerResult;
  }
  static async sigmlPreprocess(text: string) {
    const res = await fetch(
      new URL(`api/preprocess-sigml`, ServerHelper.mainBaseURL),
      {
        method: "POST",
        body: JSON.stringify({ text }),
        headers: this.headers,
      }
    );
    return (await res.json()) as SigmlPreprocessorResult;
  }
  static async speech2Text(audio: string) {
    const res = await fetch(
      new URL(`api/speechttext`, ServerHelper.mainBaseURL),
      {
        method: "POST",
        body: JSON.stringify({ audio }),
        headers: this.headers,
      }
    );
    return (await res.json()) as Speech2TextResult;
  }
  static async text2Image(text: string) {
    const res = await fetch(new URL(`/`, ServerHelper.t2iBaseURL), {
      method: "POST",
      body: JSON.stringify({ text }),
      headers: this.headers,
    });
    return { imgData: (await res.json()).image_data } as Text2ImageResult;
  }
  static async text2Emoji(text: string) {
    const res = await fetch(
      new URL(`/api/texttemoji`, ServerHelper.mainBaseURL),
      {
        method: "POST",
        body: JSON.stringify({ text }),
        headers: this.headers,
      }
    );
    return (await res.json()) as Text2EmojiResult;
  }
}
