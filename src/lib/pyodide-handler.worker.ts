import { loadPyodide, type PyodideInterface } from "pyodide";
const pyodide = await loadPyodide({
  indexURL: "/pyodide",
});
const channel = new BroadcastChannel("pyodide_islalpha");

await pyodide.loadPackage([
  "numpy",
  "scipy",
  "joblib",
  "threadpoolctl",
  "scikit_learn",
]);
const res = await fetch("/py/isl-alphabet-prediction/isl-predictor.py");
const code = await res.text();
await pyodide.runPythonAsync(code);
const context = pyodide.globals.toJs();
channel.addEventListener("message", (event) => {});
