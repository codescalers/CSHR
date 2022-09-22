<script lang="ts">
  import Evaluation from '../components/evaluation/Evaluation.svelte';
  import Sidebar from '../components/sidebar/Sidebar.svelte';
</script>

<Sidebar>
  <span slot="page-name">Evaluation</span>
  <div class="container" slot="content">
    <Evaluation />
  </div>
</Sidebar>
