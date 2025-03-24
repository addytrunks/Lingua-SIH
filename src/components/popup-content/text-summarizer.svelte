<script lang="ts">
  import BeService from "$lib/be-service";

  let {
    text,
  }: {
    text?: string;
  } = $props();

  let summarizedText = $state<string>();

  async function handleSummarize() {
    if (!text || !text) return;
    const result = await BeService.summarize(text);
    summarizedText = result.summary;
  }
</script>

<div class="md:w-[30dvw] h-[150px] overflow-y-auto pb-10">
  {#if !summarizedText}
    <p class="text-xl text-slate-800">Click the summarize button...</p>
  {:else}
    <p
      class="text-xl"
      style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;"
    >
      {summarizedText}
    </p>
  {/if}
</div>
<div
  class="absolute bottom-0 inset-x-0 bg-gradient-to-b from-transparent via-white to-white flex items-center px-2 p-2 gap-2"
>
  <input
    class="h-12 bg-white border text-lg rounded-full px-4 flex items-center justify-center disabled:text-slate-500 flex-grow"
    bind:value={text}
  />
  <button
    class="w-12 h-12 bg-blue-700 text-white text-lg font-semibold rounded-full flex items-center justify-center group gap-0"
    onclick={handleSummarize}
  >
    <span class="material-symbols-rounded">play_arrow</span>
  </button>
</div>
