<script lang="ts">
  const links = [
    {
      text: "ISL to Text",
      symbol: "local_parking",
      href: "/alphabet-predictions",
    },
    {
      text: "Speech to ISL",
      symbol: "abc",
      href: "/speech-ttext",
    },
    {
      text: "Speech to ISL (Sigml)",
      symbol: "abc",
      href: "/sigml",
    },
  ];
</script>

<img
  src="/light-robotc.png"
  alt=""
  class="absolute bottom-0 left-0 w-[50%] lg:w-auto lg:h-[85%] ml-[5%] -z-20 -scale-x-100 hidden lg:block"
/>
<main
  class="flex flex-col place-content-center lg:grid grid-cols-3 p-4 lg:p-10 gap-4 place-items-center h-[100dvh] w-[100dvw]"
>
  <div class="place-content-center hidden lg:flex"></div>
  <div
    class="grid grid-cols-2 lg:grid-cols-4 grid-rows-3 lg:grid-rows-2 gap-4 col-span-2 lg:w-[50dvw] py-4"
  >
    <div
      class="flex flex-col backdrop-blur rounded-xl bg-white/40 px-12 py-8 z-0 lg:-z-30 col-span-2 lg:col-span-3 row-span-2"
    >
      <p class="text-2xl font-semibold">Welcome To</p>
      <p class="text-6xl font-bold">LINGUA</p>
      <p>The Indian Sign Language Translator</p>
      <div class="flex-grow"></div>
      <div class="flex items-center space-x-4 text-base self-end">
        <div class="flex flex-col items-end">
          <p>Built by</p>
          <p class="font-semibold">GenX H4CK3RS!</p>
        </div>
        <img
          src="/genxhackerss.png"
          class="w-12 h-12 rounded-full"
          alt="GenX Hackers Logo"
        />
      </div>
    </div>
    {#each links as link}
      <a
        href={link.href}
        class="flex flex-col py-4 lg:py-6 px-2 lg:px-4 gap-4 place-content-center items-center border border-slate-400/20 hover:backdrop-blur hover:bg-white/60 transition rounded-xl bg-white/40"
      >
        <span class="material-symbols-rounded text-4xl lg:text-6xl"
          >{link.symbol}</span
        >
        <p class="text-center">{link.text}</p>
      </a>
    {/each}
  </div>
</main>
