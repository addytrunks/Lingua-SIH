import { ServerHelper } from "./consts";

export type LanguageItem = [string, string];

export type TranslationResult = {
  audio: string;
  result: string;
  lang: string;
};

export class Translator {
  static headers = {
    Accept: "application/json",
    "Content-Type": "application/json",
  };
  static async getLanguages() {
    const res = await fetch(
      new URL("languages", ServerHelper.translateBaseURL)
    );
    return (await res.json()) as LanguageItem[];
  }
  static async translate(langCode: string, text: string) {
    const res = await fetch(
      new URL(`translate`, ServerHelper.translateBaseURL),
      {
        method: "POST",
        body: JSON.stringify({ text, lang_code: langCode }),
        headers: this.headers,
      }
    );
    return (await res.json()) as TranslationResult;
  }
}
