<script lang="ts">
  export let option: string;
  export let fullName: string;
  export let imgLink: string;
</script>

<div class="d-flex flex-column gap-2">
  <img src={process.env.APP_BASE_API_URL + imgLink} />{fullName}
</div>
