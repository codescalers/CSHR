<script lang="ts">
  export let fullName: string;
  export let imgLink: string;
</script>

<div class="d-flex flex-column gap-2">
  <img src={process.env.APP_BASE_API_URL + imgLink} /><span>{fullName}</span>
</div>

<style>
  img {
    width: 100px;
    height: 100px;
    border-radius: 50%;
  }
  span {
    font-size: 1.5rem;
    font-weight: 600;
    text-align: right;
  }
</style>
