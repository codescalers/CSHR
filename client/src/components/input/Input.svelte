<script lang="ts">
  import { v4 as uuidv4 } from "uuid";

  export let type: "email" | "text" | "password" | "number" | "url" = "text";
  export let id: string = uuidv4(); // ⇨ '1b9d6bcd-bbfd-4b2d-9b5d-ab8dfbbd4bed'
  export let value: any;
  export let name: string = id;
  export let size: number = 255;
  export let label: string = "label";
  export let placeholder: string;
  export let errorMessage: string;
  export let hint: string = "";
  export let isError: boolean | null = null;

  export let handleInput: (e: any) => boolean;
  // for setting the error function
  const ref = (node: HTMLInputElement) => {
    node.type = type;
  };
</script>

<div class="form-group row">
  <label for={id} class="col-sm-4 col-form-label py-3">{label}</label>
  <div class="col-sm-8">
    <input
      use:ref
      bind:value
      class={`form-control ${
        isError !== null
          ? isError
            ? "is-invalid error-border text-danger"
            : "is-valid text-success"
          : ""
      } `}
      aria-describedby={id}
      on:input={(e) => {
        isError = (value + "").length === 0 || handleInput(e);
      }}
      {id}
      {placeholder}
      {name}
      {size}
    />

    <div {id} class="invalid-feedback ">
      <span class="alert-link">{errorMessage}</span> , {hint}
    </div>
    <div {id} class="valid-feedback">Looks good!</div>
  </div>
  
</div>

<style>
  input {
    margin-top: 0.3cm;
    background-color: #edf2f9;
  }
  
</style>
