<script lang="ts">
  import { onMount } from "svelte";
  import { fly, fade } from "svelte/transition";
  import IslPredictor from "$lib/isl-predictor-pyodide";
  import PyodideHandler, {
    type IslPredictorPyodideContext,
  } from "$lib/pyodide-handler";
  import MediaDeviceSelector from "./media-device-selector.svelte";

  let {
    onPredict,
    onLoadEnded,
  }: {
    onPredict: (data: any) => void;
    onLoadEnded?: () => void;
  } = $props();

  let islPredictor: IslPredictor;
  let videoElement = $state.raw<HTMLVideoElement>();
  let pyodide: any;
  let pyodideContext = $state.raw<IslPredictorPyodideContext>();
  let canvasElement: HTMLCanvasElement;
  let hasScriptsLoaded = $state(false);
  let predictedCharacter = $state("");
  let isSettingsOpen = $state(true);
  let isPaused = $state(false);
  let videoFrameCallbackNumber = $state<number>();

  $effect(() => {
    if (!isPaused && !videoFrameCallbackNumber) {
      videoFrameCallbackNumber =
        videoElement?.requestVideoFrameCallback(onVideoFrame);
      videoElement?.play();
      return;
    }
    if (isPaused) {
      if (videoFrameCallbackNumber)
        videoElement?.cancelVideoFrameCallback(videoFrameCallbackNumber);
      videoFrameCallbackNumber = undefined;
      videoElement?.pause();
    }
  });

  async function onVideoFrame() {
    if (isPaused) return;
    await islPredictor.predict();
    videoFrameCallbackNumber =
      videoElement?.requestVideoFrameCallback(onVideoFrame);
  }

  async function handleVideoSelected(mediaStream: MediaStream) {
    if (!videoElement) return;
    videoElement.srcObject = mediaStream;
    videoElement?.requestVideoFrameCallback(onVideoFrame);
    await videoElement?.play();
  }

  $effect(() => {
    if (!videoElement || !pyodideContext) return;
    islPredictor
      .initialize(pyodideContext, videoElement, canvasElement, (results) => {
        predictedCharacter = results;
        onPredict(results);
      })
      .then(() => {
        hasScriptsLoaded = true;
        if (onLoadEnded) onLoadEnded();
      });
  });

  async function handlePyScriptOnLoad() {
    pyodide = await PyodideHandler.loadISLPredictorPyodide(pyodide);
    pyodideContext = PyodideHandler.getISLPredictorContextFromPyodide(pyodide);
    await pyodideContext?.loadIslModel!();
  }

  function setPauseState(state: boolean) {
    isPaused = state;
  }

  onMount(() => {
    window.addEventListener("blur", () => setPauseState(true));
    window.addEventListener("focus", () => setPauseState(false));
    islPredictor = new IslPredictor();
    handlePyScriptOnLoad();
    return () => {};
  });
</script>

<div class="relative w-full flex flex-col items-center">
  <div class="relative flex items-center mb-10">
    <div class="overflow-hidden rounded-2xl w-full h-fit">
      <video
        bind:this={videoElement}
        class="max-h-[40dvh] {hasScriptsLoaded && !isPaused
          ? 'opacity-100'
          : 'opacity-40'}"
      >
        <track kind="captions" />
      </video>
      <canvas bind:this={canvasElement} class="absolute inset-0"></canvas>
      <div
        class="absolute inset-0 flex items-center justify-center text-xl font-semibold {hasScriptsLoaded &&
        !isPaused
          ? 'hidden'
          : 'block'}"
      >
        {#if isPaused}
          <span class="material-symbols-rounded text-[5rem] animate-pulse">
            pause_circle
          </span>
        {:else}
          <span class="material-symbols-rounded text-[5rem] animate-spin">
            progress_activity
          </span>
        {/if}
      </div>
      <div class="absolute top-2 right-2 flex flex-col items-end">
        <label
          class="w-12 h-12 bg-white roudend-full flex items-center justify-center rounded-full border overflow-hidden relative"
        >
          {#if isSettingsOpen}
            <span
              class="material-symbols-rounded absolute"
              transition:fly={{ x: 0, y: 50, duration: 200 }}
            >
              close
            </span>
          {:else}
            <span
              class="material-symbols-rounded absolute"
              transition:fly={{ x: 0, y: -50, duration: 200 }}
            >
              settings
            </span>
          {/if}
          <input type="checkbox" class="hidden" bind:checked={isSettingsOpen} />
        </label>
        {#if isSettingsOpen}
          <div
            class="whitespace-nowrap bg-white/90 backdrop-blur rounded-xl p-2"
            transition:fly={{ x: 0, y: 50, duration: 200 }}
          >
            <MediaDeviceSelector onSelect={handleVideoSelected} type="video" />
          </div>
        {/if}
      </div>
    </div>
    <div
      class="absolute -bottom-10 inset-x-0 flex items-center justify-center overflow-hidden {predictedCharacter ==
      ''
        ? 'opacity-0'
        : 'opacity-100'} transition-all"
    >
      <p
        class="px-8 py-6 flex items-center justify-center text-5xl bg-blue-700 text-white rounded-full shadow-md font-semibold"
      >
        {predictedCharacter}
      </p>
    </div>
  </div>
</div>
