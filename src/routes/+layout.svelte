<script lang="ts">
  import "../app.css";
  import type { Snippet } from "svelte";
  import type { LayoutData } from "./$types";

  let { data, children }: { data: LayoutData; children: Snippet } = $props();
</script>

<div class="absolute inset-0 -z-30 bg-[url('home-bg1.jpg')] bg-center"></div>
<a
  href="/"
  class="w-8 h-8 flex justify-center absolute top-2 left-2 items-center bg-white rounded-full z-50"
>
  <span class="material-symbols-rounded">home</span>
</a>
<a
  href="/settings"
  class="w-8 h-8 flex justify-center absolute top-2 left-12 items-center bg-white rounded-full z-50"
>
  <span class="material-symbols-rounded">settings</span>
</a>
<div class="overflow-hidden">
  {@render children()}
</div>
