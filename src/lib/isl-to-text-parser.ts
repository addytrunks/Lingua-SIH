import { AutoSuggestor } from "$lib/auto-suggestor";

export class ISL2TextParser {
  private _autoSuggestor: AutoSuggestor;
  private _word: string = "";
  private _text: string[] = [];
  private _suggestions: string[] | undefined;
  private _predictions: string[] = [];
  private _stablizedPredictions: string[] = [];
  private _hasPushedNext: boolean = false;

  constructor() {
    this._autoSuggestor = new AutoSuggestor();
    this._autoSuggestor.initialize();
  }

  appendSuggestion(index: number) {
    if (!this._suggestions || !this._suggestions.at(index)) return;
    this._word = "";
    this._text.push(this._suggestions[index]);
  }

  backspace() {
    if (!this._word) this._word = this._text.pop() ?? "";
    this._word = this._word.slice(0, this._word.length - 1);
  }

  space() {
    if (!this._word) return;
    this._text.push(this._word);
    this._word = "";
  }

  next() {
    if (this._hasPushedNext) return;
    const char = this._stablizedPredictions.at(-1);
    console.log("Last Stablized Prediction: ", char);
    if (!char) return;
    switch (true) {
      case char == "SPACE":
        this.space();
        break;
      case char == "BACKSPACE":
        this.backspace();
        break;
      case "1" <= char && char <= "9":
        this.appendSuggestion(parseInt(char) - 1);
        break;
      default:
        this._word += char.toLowerCase();
        break;
    }
    this._hasPushedNext = true;
  }

  reset() {
    this._word = "";
    this._predictions = [];
    this._stablizedPredictions = [];
    this._text = [];
  }

  getAutoSuggestorSuggestions() {
    if (this._word === "") return;
    return new Set<string>(
      this._autoSuggestor
        .getSuggestions(this._word)
        .map((v: string) => v.toLowerCase())
    )
      .values()
      .toArray();
  }

  getStablizedPrediction() {
    const predFr: any = {};
    const recentPredictions = this._predictions.slice();
    recentPredictions.forEach((v) => {
      if (v in predFr) predFr[v]++;
      else predFr[v] = 0;
    });
    const sortedPreds = recentPredictions.sort((a, b) => predFr[b] - predFr[a]);
    if (predFr[sortedPreds[0]] < 3) return;
    return sortedPreds[0];
  }

  pushPrediction(prediction: string) {
    if (prediction !== "NEXT") {
      this._predictions.push(prediction);
      if (this._predictions.length > 10)
        this._predictions = this._predictions.slice(1);
    }

    const currPrediction = this.getStablizedPrediction();
    if (!currPrediction) return;

    if (prediction === "NEXT") this.next();
    else this._hasPushedNext = false;

    if (this._stablizedPredictions.at(-1) !== currPrediction)
      this._stablizedPredictions.push(currPrediction);

    this._suggestions = this.getAutoSuggestorSuggestions();

    return {
      suggestions: this._suggestions?.slice(0, 9),
      word: this._word,
      text: this._text.join(" "),
    };
  }
}
