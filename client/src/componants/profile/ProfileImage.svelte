<script lang="ts">
  import type { userDataType } from "../../utils/types";

  export let user: userDataType | undefined;
  export let size = 50;
  export let noLink = false;

  let username: string[];
  let logo: string;

  if (user) {
    if (user.full_name.split(" ")[0] == "") {
      logo = `${user.email[0].toLocaleUpperCase()}${user.email[1].toLocaleUpperCase()}`;
    } else {
      username = user.full_name.split(" ");
      logo = `${username[0][0].toLocaleUpperCase()}${username[1][0].toLocaleUpperCase()}`;
    }
  }
</script>

{#if user}
  {#if noLink}
    {#if user.image.includes("profile_image")}
      <!-- svelte-ignore a11y-missing-attribute -->
      <img
        src={window.configs.SERVER_BASE_URL + user.image}
        class="user-profile-image rounded-circle"
        style="width:{size}px; height:{size}px;"
      />
    {:else}
      <span
        class="user-profile-image rounded-circle"
        style="background-color:{user.image}; width:{size}px; height:{size}px;"
      >
        {logo}
      </span>
    {/if}
  {:else}
    <a href="/profile/{user.id}">
      {#if user.image.includes("profile_image")}
        <!-- svelte-ignore a11y-missing-attribute -->
        <img
          src={window.configs.SERVER_BASE_URL + user.image}
          class="user-profile-image rounded-circle"
          style="width:{size}px; height:{size}px;"
        />
      {:else}
        <span
          class="user-profile-image rounded-circle"
          style="background-color:{user.image}; width:{size}px; height:{size}px;"
        >
          {logo}
        </span>
      {/if}
    </a>
  {/if}
{/if}

<style>
  .user-profile-image {
    color: #fff;
    font-weight: 700;
    justify-content: center;
    align-items: center;
    display: flex;
    border-radius: 50px;
  }
</style>
