<script lang="ts">
  import type { UserInterface } from '../../types'

  import { onMount } from 'svelte'
  import { AllUsersStore } from '../../stores'

  export let option: string
  let image: string
  let full_name: string
  onMount(() => {
    if ($AllUsersStore.length > 0) {
      const user = $AllUsersStore.find(
        (user: UserInterface) => user.id === Number(option)
      )
      if (user) {
        image = user.image
        full_name = user.full_name
      }
    }
  })

  let hidden = false
  // default back to visible every time src changes to see if the image loads successfully
  $: image, (hidden = false)
</script>

<span class="option">
  <img
    src={process.env.APP_BASE_API_URL + image}
    alt={'user avatar'}
    {hidden}
    on:error={() => (hidden = true)}
  /><span>{full_name}</span>
</span>

<style>
  img {
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 50%;
    object-fit: cover;
  }
  .option {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  span span {
    font-size: 1rem;
    font-weight: 400;
    text-align: right;
  }
</style>
