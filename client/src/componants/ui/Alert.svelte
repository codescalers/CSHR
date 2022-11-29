<script lang="ts">
    export let title: string, className: string, message: string;
</script>

<div class={`alert alert-${className} alert-dismissible fade show text-center`} role="alert">
    <span>{title}</span>, {message}
</div>
  