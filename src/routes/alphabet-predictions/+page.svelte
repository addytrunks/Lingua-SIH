<script lang="ts">
  import { fade } from "svelte/transition";
  import { ISL2TextParser } from "$lib/isl-to-text-parser";
  import IslPredictor from "../../components/isl-predictor.svelte";
  import Popup from "../../components/popup.svelte";
  import Translator from "../../components/popup-content/translator.svelte";
  import TextSummarizer from "../../components/popup-content/text-summarizer.svelte";
  import TextToImage from "../../components/popup-content/text-to-image.svelte";
  import TextToEmoji from "../../components/popup-content/text-to-emoji.svelte";

  const menuItems = [
    {
      icon: "translate",
      title: "Translator",
      snippet: Translator,
    },
    {
      icon: "description",
      title: "Text Summarizer",
      snippet: TextSummarizer,
    },
    {
      icon: "image",
      title: "Text to Image",
      snippet: TextToImage,
    },
    {
      icon: "mood",
      title: "Text to Emoji",
      snippet: TextToEmoji,
    },
  ];

  function initMenuItemsVisibility() {
    const visibility: Record<string, boolean> = {};
    menuItems.forEach((item) => {
      visibility[item.title] = false;
    });
    return visibility;
  }

  let suggestionsFor = $state<string>();
  let suggestions = $state.raw<string[]>();
  let text = $state<string>();
  let currWord = $state<string>();
  const islTextParser = new ISL2TextParser();
  let isMenuItemsVisible = $state(initMenuItemsVisibility());

  const isTauri = (window as any).__TAURI__ as boolean;
  function handleIslPredictorOnPredict(predictedChar: any) {
    const parserResults = islTextParser.pushPrediction(predictedChar);
    if (!parserResults) return;
    if (suggestionsFor != parserResults.word.at(-1)) {
      suggestions = parserResults.suggestions;
      suggestionsFor = parserResults.word.at(-1);
    }
    currWord = parserResults?.word;
    text = parserResults?.text;
  }
</script>

<main
  class="flex flex-col lg:grid grid-cols-2 gap-4 p-4 h-[100dvh] w-[100dvw] bg-white backdrop-blur"
>
  <div class="flex flex-col-reverse lg:flex-col items-center">
    <IslPredictor onPredict={handleIslPredictorOnPredict} />

    <div class="min-h-[15dvh] mt-4">
      <div class="flex flex-wrap justify-center gap-2 p-4">
        {#if suggestions}
          {#each suggestions as suggestion, i}
            <button
              class="text-base md:text-lg pr-4 gap-2 rounded-full border h-fit flex items-center"
              in:fade
            >
              <p
                class="flex items-center justify-center w-6 h-6 md:w-7 md:h-7 font-bold text-white bg-blue-600 rounded-full"
              >
                {i + 1}
              </p>
              <p class="">{suggestion}</p>
            </button>
          {/each}
        {/if}
      </div>
    </div>
  </div>
  <div class="flex flex-col items-stretch space-y-4">
    <div
      class="flex flex-col relative border rounded-xl p-4 min-h-[20dvh] overflow-hidden"
    >
      {#if !text && !currWord}
        <p class="text-lg text-slate-400">
          Select camera and once predictor is ready sign ISL to see results
          here...
        </p>
      {/if}
      <p class="text-xl">{text}{currWord != "" ? " " : ""}{currWord}</p>
      <div
        class="absolute bottom-0 inset-x-0 bg-gradient-to-b from-transparent via-white to-white flex items-center px-4 p-2"
      >
        <p class="text-xl font-semibold">Result</p>
        <div class="flex-grow"></div>
        <div class="flex items-center gap-2">
          {#each menuItems as item}
            <label
              class="w-12 h-12 border {isMenuItemsVisible[item.title]
                ? 'border-transparent bg-blue-700 text-white'
                : 'border-inherit bg-inherit text-inherit'} transition text-lg font-semibold rounded-full hover:gap-3 hover:w-auto hover:px-4 items-center justify-center group gap-0 flex"
            >
              <p
                class="w-0 whitespace-nowrap overflow-hidden transition group-hover:w-auto"
              >
                {isMenuItemsVisible[item.title] ? "Hide" : "Show"}
                {item.title}
              </p>
              <span class="material-symbols-rounded">{item.icon}</span>
              <input
                type="checkbox"
                class="hidden"
                bind:checked={isMenuItemsVisible[item.title]}
              />
            </label>
          {/each}
        </div>
      </div>
    </div>
    {#each menuItems as item}
      <Popup bind:isVisible={isMenuItemsVisible[item.title]}>
        <item.snippet {text} />
      </Popup>
    {/each}
  </div>
</main>
