<script lang="ts">
  import { v4 as uuidv4 } from "uuid";

  export let type:
    | "file"
    | "tel"
    | "time"
    | "email"
    | "text"
    | "password"
    | "number"
    | "url"
    | "date" = "text";
  export let id: string = uuidv4(); // ⇨ '1b9d6bcd-bbfd-4b2d-9b5d-ab8dfbbd4bed'
  export let value: any;
  export let name: string = id;
  export let size = 255;
  export let label = "label";
  export let placeholder: string;
  export let className = "";
  export let correctMessage = "";
  export let errorMessage: string;
  export let hint = "";
  export let disabled = false;
  // if true the input is invalid && show error message
  // if false the input is valid && hide error message
  /// if null the input is not touched && hide error message
  export let isError: boolean | null | Promise<boolean> = null;
  export let isTop = true;

  export let handleInput: (e: any) => boolean | Promise<boolean>;
  // for setting the error function
  const ref = (node: HTMLInputElement) => {
    node.type = type;
  };

  $: if ((value + "").trim.length === 0) {
    isError = null;
  }
</script>

<div class={`form-group row ${className}`}>
  <label for={id} class={`${isTop ? "col-sm-4" : ""} col-form-label py-3`}
    >{label}</label
  >
  <div class={`${isTop ? "col-sm-8" : "col-sm-12"}`}>
    <input
      use:ref
      bind:value
      {disabled}
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

    <div {id} class="invalid-feedback">
      <span class="alert-link">{errorMessage}</span>
      {hint.length ? `, ${hint}` : ""}
    </div>
    <div {id} class="valid-feedback">{correctMessage}</div>
  </div>
</div>

<style>
  input {
    margin-top: 0.3cm;
    background-color: var(--secondary-color);
  }
</style>
