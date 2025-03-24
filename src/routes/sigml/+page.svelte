<script lang="ts">
  import SigmlService from "$lib/sigml-service";
  import SpeechInput from "../../components/speech-input.svelte";

  async function sendText(t: string) {
    await SigmlService.playSigml(t);
  }
</script>

<svelte:head>
  <!-- <link
    rel="stylesheet"
    href="https://vhg.cmp.uea.ac.uk/tech/jas/vhg2025/cwa/cwasa.css"
  /> -->
  <script
    type="text/javascript"
    src="https://vhg.cmp.uea.ac.uk/tech/jas/vhg2025/cwa/allcsa.js"
    onload={async () => {
      await SigmlService?.initCwasa();
    }}
  ></script>
</svelte:head>
<main
  class="flex flex-col-reverse lg:grid grid-cols-2 justify-center items-end lg:items-center p-10 gap-4 h-[100dvh] w-[100dvw]"
>
  <div
    class="flex flex-col w-full md:w-[30dvw] place-self-center items-center rounded-xl bg-white/40 backdrop-blur p-10 gap-4"
  >
    <SpeechInput onPlay={sendText} />
  </div>
  <div
    class="flex flex-col place-self-center min-h-[30dvh] w-full md:min-w-[40dvw] rounded-xl bg-white/40 backdrop-blur p-4"
  >
    <div class="flex justify-end gap-2 items-center">
      <select class="menuAv av0 hidden">
        {#each SigmlService.avatars as avatar}
          <option value={avatar}>{avatar}</option>
        {/each}
      </select>
      <p class="text-black/80 pr-2">Switch Avatar</p>
      <button
        class="flex items-center justify-center w-12 h-12 rounded-full border border-black/40"
        onclick={() => SigmlService.changeAvatar(-1)}
      >
        <span class="material-symbols-rounded text-4xl">chevron_left</span>
      </button>
      <button
        class="flex items-center justify-center w-12 h-12 rounded-full border border-black/40"
        onclick={() => SigmlService.changeAvatar(1)}
      >
        <span class="material-symbols-rounded text-4xl">chevron_right</span>
      </button>
    </div>
    <div class="CWASAAvatar av0 w-full min-h-[300px] md:min-h-[600px]"></div>
  </div>
</main>
