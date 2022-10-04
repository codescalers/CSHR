<script lang="ts">
  export let image = '';
  export let full_name = '';
  export let team = '';
  export let gender: 'Male' | 'Female';
</script>

<div
  class={`circular_img`}
  style={`background-image:url(${
    process.env.APP_BASE_API_URL + image
  });background-color:${
    gender === 'Male' ? '#2986cc' : '#FB5858'
  };border:1.5px solid ${
    gender === 'Male' ? 'var(--secondary-color)' : 'pink'
  }`}
  data-bs-toggle="tooltip"
  title={full_name + ' #' + team}
/>
