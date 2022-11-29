<script lang="ts">
    import Userkills from './Userkills.svelte';
    import TrainingAndCourses from './TrainingAndCourses.svelte';
</script>

<div class="card">
    <div class="card-body">
        <div class="row">
            <div class="col-6 right-br relative">
                <Userkills />
            </div>
            <div class="col-6">
                <TrainingAndCourses />
            </div>
        </div>
    </div>
</div>

<style>
    .right-br{
        border-right: 1px solid rgb(54 55 64 / 21%);
    }
    .relative{
        position: relative;
    }
</style>
