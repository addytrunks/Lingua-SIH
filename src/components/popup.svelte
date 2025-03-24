<script lang="ts">
  import type { Snippet } from "svelte";

  let {
    children,
    isVisible = $bindable(),
  }: {
    children: Snippet;
    isVisible: boolean;
  } = $props();
</script>

{#if isVisible}
  <div
    class="absolute bg-white inset-x-2 bottom-2 m-auto flex flex-col lg:relative border rounded-xl p-4 min-h-[20dvh] z-50"
  >
    <button
      class="absolute -top-14 right-2 w-12 h-12 rounded-full flex items-center justify-center bg-white border md:hidden"
      onclick={() => {
        isVisible = false;
      }}
    >
      <span class="material-symbols-rounded">close</span>
    </button>
    {@render children()}
  </div>
{/if}
