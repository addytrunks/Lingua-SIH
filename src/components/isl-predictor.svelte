<script lang="ts">
  import { onMount } from "svelte";
  import { fly, fade } from "svelte/transition";
  import IslPredictor from "$lib/isl-predictor";
  import MediaDeviceSelector from "./media-device-selector.svelte";

  let {
    onPredict,
    onLoadEnded,
  }: {
    onPredict: (data: any) => void;
    onLoadEnded?: () => void;
  } = $props();

  let islPredictor = new IslPredictor();
  let videoElement = $state.raw<HTMLVideoElement>();
  let canvasElement: HTMLCanvasElement;
  let predictedCharacter = $state("");
  let isSettingsOpen = $state(true);
  let isPaused = $state(true);

  async function onVideoFrame() {
    if (!isPaused) await islPredictor.predict();
    videoElement?.requestVideoFrameCallback(onVideoFrame);
  }

  async function handleVideoSelected(mediaStream: MediaStream) {
    if (!videoElement) return;
    isSettingsOpen = false;
    videoElement.srcObject = mediaStream;
    videoElement?.requestVideoFrameCallback(onVideoFrame);
    await videoElement?.play();
  }

  $effect(() => {
    if (!videoElement) return;
    islPredictor
      .initialize(videoElement, canvasElement, (results) => {
        predictedCharacter = results;
        onPredict(results);
      })
      .then(() => {
        isPaused = false;
        if (onLoadEnded) onLoadEnded();
      });
  });

  function pauseVideo() {
    isPaused = true;
  }

  function playVideo() {
    isPaused = false;
  }

  onMount(() => {
    window.addEventListener("blur", pauseVideo);
    window.addEventListener("focus", playVideo);
    return () => {
      window.removeEventListener("blur", pauseVideo);
      window.removeEventListener("focus", playVideo);
    };
  });
</script>

<div class="relative w-fit flex flex-col items-center">
  <div class="overflow-hidden rounded-t-3xl w-fit h-fit">
    <video
      bind:this={videoElement}
      class="max-h-[40dvh] {!isPaused ? 'opacity-100' : 'opacity-40'}"
    >
      <track kind="captions" />
    </video>
    <canvas bind:this={canvasElement} class="absolute inset-0"></canvas>
    <div
      class="absolute inset-0 flex items-center justify-center text-xl font-semibold {!isPaused
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
    class="-bottom-10 inset-x-0 flex w-full items-center justify-stretch overflow-hidden {predictedCharacter ==
    ''
      ? 'opacity-0'
      : 'opacity-100'} transition-all"
  >
    <p
      class="px-8 py-6 flex items-center justify-center w-full text-5xl bg-blue-700 text-white rounded-b-3xl shadow-md font-semibold"
    >
      {predictedCharacter}
    </p>
  </div>
</div>
