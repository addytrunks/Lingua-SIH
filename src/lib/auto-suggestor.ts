import Predictionary from "predictionary";

export class AutoSuggestor {
  private _pdct: Predictionary;
  constructor() {
    this._pdct = Predictionary.instance();
  }
  async initialize() {
    const res = await fetch("/word-prediction/predictionary_dicts.json");
    const resText = await res.text();
    this._pdct.loadDictionaries(resText);
  }
  getSuggestions(prompt: string) {
    return this._pdct.predict(prompt);
  }
}
