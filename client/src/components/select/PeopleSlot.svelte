<script lang="ts">
  import type { SelectOptionType } from './types';

  export let option: SelectOptionType;
  let image: string = option.extraData.image;
  let full_name: string = option.extraData.full_name;
  let team: string = option.extraData.team;

  let hidden = false;
  // default back to visible every time src changes to see if the image loads successfully
  $: image, (hidden = false);
</script>

<div class="option" title={`#${team}`}>
  <img
    src={process.env.APP_BASE_API_URL + image}
    alt={'user avatar'}
    {hidden}
    on:error={() => (hidden = true)}
  /><span>{full_name}</span>
</div>

<style>
  img {
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 50%;
    object-fit: cover;
  }
  .option {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  div span {
    font-size: 1rem;
    font-weight: 400;
    text-align: right;
  }
</style>
