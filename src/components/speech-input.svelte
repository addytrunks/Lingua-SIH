<script lang="ts">
  import MediaDeviceSelector from "./media-device-selector.svelte";
  import BeService from "$lib/be-service";
  import AudioRecorder from "$lib/audio-recorder";

  let {
    onPlay,
  }: {
    onPlay: (text: string) => void;
  } = $props();

  let isRecording = $state<boolean>(false);
  let text = $state<string>();
  let audioRecorder = $state<AudioRecorder>();
  let isMediaSelectorShown = $state<boolean>(false);

  async function handleAudioSelected(mediaStream: MediaStream) {
    isMediaSelectorShown = false;
    isRecording = false;
    if (audioRecorder) audioRecorder = undefined;
    audioRecorder = new AudioRecorder(mediaStream, (audioStr) => {
      BeService.speech2Text(audioStr).then((res) => {
        text = res.text;
      });
    });
  }

  function handleStartRecordingClick() {
    isRecording = true;
    audioRecorder?.startRecording();
    text = "";
  }

  function handleStopRecordingClick() {
    isRecording = false;
    text = undefined;
    audioRecorder?.stopRecording();
  }
</script>

<div
  class="transition-all overflow-hidden {isMediaSelectorShown
    ? 'h-24 py-4'
    : 'h-0 py-0'} px-4 bg-white/20 rounded-xl w-full"
>
  <MediaDeviceSelector onSelect={handleAudioSelected} type="audio" />
</div>
<div class="flex flex-wrap flex-row md:items-center justify-end gap-2 w-full">
  <input
    type="text"
    bind:value={text}
    placeholder="Enter Text"
    class="bg-white/20 h-12 min-w-0 placeholder:text-black/40 rounded-full px-4 flex-grow"
  />
  <div class="flex items-center justify-center gap-2">
    <button
      class="w-12 h-12 flex items-center justify-center rounded-full {isRecording
        ? 'bg-red-600'
        : 'bg-blue-600'} text-white transition"
      disabled={!audioRecorder}
      onclick={() => {
        isRecording ? handleStopRecordingClick() : handleStartRecordingClick();
      }}
    >
      <span class="material-symbols-rounded"
        >{isRecording ? "stop_circle" : "mic"}</span
      >
    </button>
    <button
      class="w-12 h-12 flex items-center justify-center rounded-full border border-black/40 transition"
      onclick={() => {
        isMediaSelectorShown = !isMediaSelectorShown;
      }}
    >
      <span class="material-symbols-rounded"
        >{isMediaSelectorShown ? "close" : "settings"}</span
      >
    </button>
  </div>
</div>
<button
  class="px-4 py-2 rounded-full border border-black/40 w-full"
  onclick={() => onPlay(text!)}
>
  Play ISL
</button>
