<script lang="ts">
  import SettingsApi from './components/settings/SettingsApi'
  import { onMount } from 'svelte'
  import { SettingsStore } from './stores'
  import Routes from './Routes.svelte'
  onMount(async function () {
    $SettingsStore = await SettingsApi.getSettings()
  })
  let rootElement: HTMLDivElement

  $: rootElement &&
    rootElement.style.setProperty(
      '--primary-color',
      $SettingsStore['primary-color']
    )
  $: rootElement &&
    rootElement.style.setProperty(
      '--secondary-color',
      $SettingsStore['secondary-color']
    )
</script>

<div class="fluid-container all" bind:this={rootElement}>
  <Routes />
</div>

<style>
  :root {
    --primary-color: inherit;
    --secondary-color: inherit;
    --background-image: inherit;
    --text-color: var(var(--secondary-color));
    font-family: 'Quicksand', sans-serif;
  }
</style>
