<script lang="ts">
  import { onMount } from "svelte";
  import { fade } from "svelte/transition";

  let {
    onSelect,
    type,
  }: {
    onSelect: (data: MediaStream) => void;
    type: "audio" | "video";
  } = $props();

  const localStorageKey =
    type === "video" ? "selectedvideodeviceid" : "selectedaudiodeviceid";
  let selectDeviceId = $state<string>();
  let mediaDevices = $state.raw<MediaDeviceInfo[]>();
  let selectElement: HTMLSelectElement;

  $effect(() => {
    if (selectDeviceId) handleSelectionChange(selectDeviceId);
  });

  async function handleSelectionChange(deviceId: string) {
    const device = await navigator.mediaDevices?.getUserMedia(
      type === "video"
        ? {
            video: { deviceId: deviceId },
          }
        : {
            audio: { deviceId: deviceId },
          }
    );
    localStorage.setItem(localStorageKey, deviceId);
    onSelect(device);
  }

  onMount(async () => {
    if (selectElement) selectElement.focus();
    await navigator.mediaDevices.getUserMedia(
      type === "video" ? { video: true } : { audio: true }
    );
    let devices = await navigator.mediaDevices.enumerateDevices();
    if (!devices) {
      const val = await navigator.mediaDevices.getUserMedia(
        type === "video" ? { video: true } : { audio: true }
      );
      onSelect(val);
    }
    devices = devices.filter(
      (d) => d.kind === (type === "video" ? "videoinput" : "audioinput")
    );
    mediaDevices = devices;
    const storedSelectDeviceId = localStorage.getItem(localStorageKey);
    if (!storedSelectDeviceId) return;
    selectDeviceId = storedSelectDeviceId;
  });
</script>

<label class="p-2 flex flex-col space-y-2">
  <p class="text-xs font-bold px-2">
    Select {type == "video" ? "Camera" : "Mic"}
  </p>
  <select
    bind:value={selectDeviceId}
    bind:this={selectElement}
    class="px-4 py-1 border border-black/40 rounded bg-transparent overflow-hidden text-ellipsis w-[300px] disabled:text-black/40"
    disabled={!mediaDevices}
  >
    {#if mediaDevices}
      {#each mediaDevices as device}
        <option value={device.deviceId}>{device.label}</option>
      {/each}
    {:else}
      <option value="" out:fade>Loading...</option>
    {/if}
  </select>
</label>
