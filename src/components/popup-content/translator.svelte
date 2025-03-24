<script lang="ts">
  import { fade } from "svelte/transition";
  import { onMount } from "svelte";
  import { Translator } from "$lib/translator";
  import { base64TUrl } from "$lib/utils";

  let {
    text,
  }: {
    text?: string;
  } = $props();

  let languages = $state.raw<string[][]>();
  let selectedLanguageCode = $state<string>();
  let translatedText = $state<string>();
  let translatedAudioUrl = $state<string>();
  let translatedAudioElement = $state.raw<HTMLAudioElement>();

  async function handleTranslate() {
    if (!selectedLanguageCode || !text) return;
    const result = await Translator.translate(selectedLanguageCode, text);
    translatedText = result.result;
    translatedAudioUrl = base64TUrl(result.audio);
  }

  function handleTranslatedPlayAudio() {
    translatedAudioElement?.play();
  }

  onMount(async () => {
    languages = await Translator.getLanguages();
  });
</script>

<div class="md:w-[30dvw] h-[150px] overflow-y-auto pb-10">
  {#if !translatedText}
    <p class="text-xl text-slate-800">
      Choose a language to translate to and click translate button...
    </p>
  {:else}
    <p
      class="text-xl"
      style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;"
    >
      {translatedText}
    </p>
  {/if}
</div>
<div
  class="absolute bottom-0 inset-x-0 bg-gradient-to-b from-transparent via-white to-white flex items-center px-2 p-2"
>
  <div class="flex-grow"></div>
  <div class="flex items-center gap-2">
    <select
      class="h-12 bg-white border text-lg font-semibold rounded-full px-4 flex items-center justify-center disabled:text-slate-500 after:content-['']"
      disabled={!languages}
      bind:value={selectedLanguageCode}
    >
      {#if languages}
        {#each languages as language}
          <option value={language[1]}>{language[0]}</option>
        {/each}
      {:else}
        <option value="" out:fade>Loading...</option>
      {/if}
    </select>
    <button
      class="w-12 h-12 bg-blue-700 text-white text-lg font-semibold rounded-full flex items-center justify-center group gap-0"
      onclick={handleTranslate}
    >
      <span class="material-symbols-rounded">translate</span>
    </button>
    <button
      class="w-12 h-12 bg-blue-700 text-white text-lg font-semibold rounded-full flex items-center justify-center group gap-0"
      onclick={handleTranslatedPlayAudio}
    >
      <span class="material-symbols-rounded">play_arrow</span>
    </button>
    <audio src={translatedAudioUrl} bind:this={translatedAudioElement} autoplay
    ></audio>
  </div>
</div>
