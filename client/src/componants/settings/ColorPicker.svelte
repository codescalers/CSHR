<script lang="ts">
    import { Color, ColorInput } from 'color-picker-svelte'
    export let color: Color;

</script>

<ColorInput bind:color className={"input"} title={color.toHexString()} showAlphaSlider />

<svelte:head>
    <style>
        .input{
            background-color: var(--secondary-color)!important;
        }
    </style>
</svelte:head>