import { loadPyodide, type PyodideInterface } from "pyodide";

export type IslPredictorPyodideContext = {
  loadIslModel?: () => Promise<void>;
  predictIsl?: (auxData: number[], numHands: number) => Promise<string>;
};
export type TranslatorResult = {
  audio: string;
  result: string;
  lang: string;
};
export type TranslatorPyodideContext = {
  getLanguages?: () => Promise<string[][]>;
  getTranslated?: (langCode: string, text: string) => Promise<TranslatorResult>;
};
export type PyodideContext = IslPredictorPyodideContext &
  TranslatorPyodideContext;

export default class PyodideHandler {
  private static async _loadPyodide(
    packages: string[],
    pyodide?: PyodideInterface
  ) {
    if (!pyodide)
      pyodide = await loadPyodide({
        indexURL: "/pyodide",
      });
    await pyodide.loadPackage(packages);
    return pyodide;
  }
  private static async _loadPyCode(path: string) {
    const res = await fetch(path);
    const code = await res.text();
    return code;
  }
  static async loadISLPredictorPyodide(
    pyodide: PyodideInterface
  ): Promise<PyodideInterface> {
    pyodide = await this._loadPyodide(
      ["numpy", "scipy", "joblib", "threadpoolctl", "scikit_learn"],
      pyodide
    );
    await pyodide.runPythonAsync(
      await this._loadPyCode("/py/isl-alphabet-prediction/isl-predictor.py")
    );
    return pyodide;
  }
  static getISLPredictorContextFromPyodide(
    pyodide: PyodideInterface
  ): IslPredictorPyodideContext {
    const context = pyodide.globals.toJs();
    return {
      loadIslModel: async () => {
        await context.loadIslModel();
      },
      predictIsl: async (auxData, numHands) => {
        return await context.predictIsl(auxData, numHands);
      },
    };
  }
  static async loadTranslatorPyodide(
    pyodide?: PyodideInterface
  ): Promise<PyodideInterface> {
    pyodide = await this._loadPyodide(
      [
        "requests",
        "ssl",
        "py/translations/googletrans-3.0.0-py3-none-any.whl",
        "py/translations/gTTS-2.5.4-py3-none-any.whl",
        "py/translations/httpcore-0.9.1-py3-none-any.whl",
        "py/translations/sniffio-1.3.1-py3-none-any.whl",
        "py/translations/h2-3.2.0-py2.py3-none-any.whl",
        "py/translations/chardet-3.0.4-py2.py3-none-any.whl",
        "py/translations/h11-0.9.0-py2.py3-none-any.whl",
        "py/translations/hpack-3.0.0-py2.py3-none-any.whl",
        "py/translations/hstspreload-2024.12.1-py3-none-any.whl",
        "py/translations/httpx-0.13.3-py3-none-any.whl",
        "py/translations/rfc3986-1.5.0-py2.py3-none-any.whl",
        "py/translations/hyperframe-5.2.0-py2.py3-none-any.whl",
      ],
      pyodide
    );
    await pyodide.runPythonAsync(
      await this._loadPyCode("/py/translations/translator.py")
    );
    return pyodide;
  }
  static getTranslatorContextFromPyodide(
    pyodide: PyodideInterface
  ): TranslatorPyodideContext {
    const context = pyodide.globals.toJs();
    return {
      getLanguages: async () => {
        return (await context.getLanguages()).toJs();
      },
      getTranslated: async (langCode: string, text: string) => {
        const val = await context.getTranslated(langCode, text);
        return (await context.getTranslated(langCode, text)).toJs();
      },
    };
  }
}
