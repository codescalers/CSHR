<script lang="ts">
    export let image: HTMLImageElement;
    export let styleOnRow: string = "";
    let input: HTMLInputElement;
    let container: HTMLDivElement;
    let placeholder: HTMLSpanElement;
    let showImage: boolean = false;
  
    function onChange() {
      const file = input.files[0];  
        if (file) {
            showImage = true;
            const reader: any = new FileReader();
            reader.addEventListener("load", function () {
                image.setAttribute("src", reader.result);
            });
            reader.readAsDataURL(file);
            return;
        }  
        showImage = false; 
    }
</script>

<div class="row" style="{styleOnRow}">
    <div class="col-6">
        <input
            bind:this={input}
            on:change={onChange}
            type="file"
        />
    </div>
    <div class="col-6 d-flex justify-content-end">
        <div bind:this={container} class="preview">
            {#if showImage}
                <img bind:this={image} src="" alt="Preview" />
            {:else}
                <span bind:this={placeholder}>Image Preview</span>
            {/if}
        </div>
    </div>
</div>


<style>
    .preview{
        width: 300px;
        min-height: 100px;
        border: 2px solid #ddd;
        margin-top: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: #ccc;
    }
    img {
        width: 100%;
    }
</style>
  