<script lang="ts">
  import { onMount } from "svelte";

  let sip = $state<string | undefined>();

  $effect(() => {
    if (sip) localStorage.setItem("app-sip", sip);
  });

  onMount(() => {
    sip = localStorage.getItem("app-sip") ?? undefined;
  });
</script>

<main
  class="flex flex-col justify-center items-center gap-4 p-4 h-[100dvh] w-[100dvw]"
>
  <div class="flex flex-col bg-white rounded-xl p-10">
    <label class="flex flex-col space-y-2">
      <p class="font-semibold">Set Server Host</p>
      <input
        type="text"
        bind:value={sip}
        class="border px-2 py-1 rounded-lg"
      /></label
    >
  </div>
</main>
