<script lang="ts">
  import { dialogs } from "svelte-dialogs";
  //import { onMount } from "svelte";
  //import { fade, scale } from "svelte/transition";
  import SettingsApi from "./SettingsApi";
  //import types {SettingsType} from "../../types";
  import { SettingsStore } from "../../stores";

  import { v4 as uuidv4 } from "uuid";

  let inputs = [
    { label: "name", type: "text", required: true },
    { label: "email", type: "email" },
    { label: "Primary Color", type: "color" },
    { label: "Secondary Color", type: "color" },
    { label: "Background Image Link", type: "url" },
  ];
  const promptOptions = {
    title: "Settings",
  };
  const alertSettings = () => {
    if (SettingsApi.isName() === true && inputs[0].label === "name") {
      inputs = inputs.splice(1, inputs.length - 1);
    }

    dialogs.prompt(inputs, promptOptions).then((settingsInputData) => {
      console.log("before settingsInputDatCa", settingsInputData);
      console.log("before settingstore", settingsInputData);
      const newSettings = {
        name: !SettingsApi.isName()
          ? settingsInputData[0] + "#" + uuidv4()
          : SettingsApi.getName(),
        email: settingsInputData[1] + "",
        "primary-color":
          settingsInputData[2] === undefined
            ? "#aaaa"
            : settingsInputData[2] + "",
        "secondary-color":
          settingsInputData[3] === undefined
            ? "#eee"
            : settingsInputData[3] + "",
        "background-image":
          settingsInputData[4] === undefined
            ? $SettingsStore["background-image"]
            : "url(" + settingsInputData[4] + ")",
      };
      console.log("after newSettings", newSettings);

      if (SettingsApi.isName() === true) {
        SettingsApi.setSettings(newSettings);
      } else {
        SettingsApi.setSettings(newSettings);
        SettingsStore.update((oldSettings) => {
          return {
            ...oldSettings,
            ...newSettings,
          };
        });
      }
      console.log("after @settings.svelte", $SettingsStore["name"]);
    });
  };
  // checking if name is set or not in local storage && running the settings once
  if (SettingsApi.isName() === false) {
    alertSettings();
  }
</script>

<div class="settings">
  <button class="settings-btn" on:click={alertSettings}
    ><i class="fa-solid fa-gear icon" />
  </button>
</div>

<style>
  .settings {
    text-align: right;
  }
  .settings-btn {
    background: none;
    border: none;
  }

  .icon {
    font-size: 2rem;
    color: var(--primary-color);
  }
</style>
