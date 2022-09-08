<script lang="ts">
  export let option;
  const { full_name, image } = option;
</script>

<div class="d-flex flex-column gap-2">
  <img src={image} alt={full_name + " avatar"} /><span>{full_name}</span>
</div>

<style>
  img {
    width: 1.5rem;
    height: 1.6rem;
    border-radius: 50%;
    object-fit: contain;
  }
  span {
    font-size: 1rem;
    font-weight: 400;
    text-align: right;
  }
</style>
