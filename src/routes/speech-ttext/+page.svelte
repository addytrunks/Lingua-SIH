<script lang="ts">
  import { onMount } from "svelte";
  import SpeechInput from "../../components/speech-input.svelte";
  import { TextTISLWSHandler } from "$lib/ws-handler";

  const categories = ["railway", "medical", "academic"];

  let img = $state<string>();
  let wsHandler = $state.raw<TextTISLWSHandler>();
  let currentCategory = $state<string>("railway");

  onMount(() => {
    wsHandler = new TextTISLWSHandler((data) => {
      img = data;
    });
    return wsHandler?.disconnect;
  });
</script>

<main
  class="flex flex-col-reverse lg:grid grid-cols-2 justify-center items-end lg:items-center p-10 gap-4 h-[100dvh] w-[100dvw]"
>
  <div
    class="flex flex-col w-full md:w-[30dvw] place-self-center items-center rounded-xl bg-white/40 backdrop-blur p-10 gap-4"
  >
    <select
      bind:value={currentCategory}
      class="w-full h-12 bg-white/20 rounded-full px-4 flex-grow capitalize"
    >
      {#each categories as category}
        <option value={category} class="">{category}</option>
      {/each}
    </select>
    <SpeechInput
      onPlay={(text) => {
        wsHandler?.sendText(text, currentCategory);
      }}
    />
  </div>
  <div
    class="flex flex-col place-self-center min-h-[30dvh] w-full md:min-w-[40dvw] rounded-xl bg-white/40 backdrop-blur p-4"
  >
    {#if img}
      <img
        class="w-[75dvw] md:w-[60dvw] gap-3 self-center rounded-xl"
        src={img}
        alt="Loading"
      />
    {:else}
      <p class="text-black/70 m-auto">
        Type or speak and click the Play ISL button...
      </p>
    {/if}
  </div>
</main>
