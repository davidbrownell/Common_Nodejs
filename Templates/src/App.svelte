<script lang="typescript">
  import TailwindCss from "./TailwindCSS.svelte";
  import { onMount } from "svelte";

  let count: number = 0;
  onMount(() => {
    const interval = setInterval(() => count++, 1000);
    return () => {
      clearInterval(interval);
    };
  });
</script>

<style type="text/sass">
  @use 'App'
</style>

<div class="text-center">
  <header class="flex flex-col items-center justify-center">
    <img src="/logo.svg" alt="logo" class="pointer-events-none" />
    <p>Edit <code>src/App.svelte</code> and save to reload.</p>
    <p>Page has been open for <code>{count}</code> seconds.</p>
    <p>
      <a href="https://svelte.dev" target="_blank" rel="noopener noreferrer">
        Learn Svelte
      </a>
    </p>
  </header>
</div>
