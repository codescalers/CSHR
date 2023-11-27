<script lang="ts">
  import { createEventDispatcher } from "svelte";
  import { v4 as uuidv4 } from "uuid";

  import type {
    SelectOptionsComponent,
    SelectOptionType
  } from "../../../utils/types";

  export let options: SelectOptionsComponent = {
    optionsList: [],
    selected: [],
    label: "choose",
    removeAllTitle: "Remove all",
    multiple: true,
    errorMessage: "Please select atleast an option.",
    isTop: true,
    className: "",
    isError: false,
    isLabel: false,
    show: false,
    disabled: false
  };

  if (!options.placeholder) {
    options.placeholder = `Select ${options.label}`;
  }

  if (!options.hint) {
    options.hint = options.multiple
      ? "you can choose multiple options"
      : "you can choose only one option";
  }

  let id: string = uuidv4();
  const dispatch = createEventDispatcher();

  function select(e: any, option: SelectOptionType) {
    e.stopPropagation();
    if (options.multiple) {
      if (options.selected?.includes(option)) {
        options.selected = options.selected.filter(
          (item) => item.value !== option.value
        );

        options.selected = options.selected.filter(
          (item) => item.value !== option.value
        );
      } else {
        options.selected = [...options.selected!, option];
      }
    } else {
      options.selected = [option];
    }
    dispatch("select", {
      selected: options.selected[0]
    });
    options.show = false;
  }

  let highlightedIndex = 1;

  const ref = (node: HTMLDivElement) => {
    node.addEventListener("keydown", (e: KeyboardEvent) => {
      if (e.target !== node) return;

      switch (e.code) {
        case "ArrowUp":
          options.show = true;
          e.preventDefault();
          if (highlightedIndex === 0) {
            highlightedIndex = options.optionsList!.length - 1;
          } else {
            highlightedIndex--;
          }
          break;
        case "ArrowDown":
          options.show = true;
          if (highlightedIndex === options.optionsList!.length - 1) {
            highlightedIndex = 0;
          } else {
            highlightedIndex++;
          }
          break;
        case "Enter":
        case "Space":
          select(e, options[highlightedIndex]);
          e.preventDefault();
          e.stopPropagation();
          break;
      }
    });
  };
</script>

<div class={`form-group row ${options.className}`}>
  <label
    for={id}
    class={`${options.isTop ? "col-sm-4" : ""} col-form-label py-3`}
  >
    {options.label}
  </label>

  <div class={`${options.isTop ? "col-sm-8" : "col-sm-12"}`}>
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <!-- svelte-ignore a11y-no-static-element-interactions -->
    <div
      use:ref
      on:blur={() => (options.show = false)}
      on:click={() => (options.show = !options.show)}
      tabIndex="0"
      class="select-container my-2 {options.disabled ? 'disabled' : ''}"
    >
      <div class="value">
        {#if options.selected}
          {#if options.selected.length > 0}
            {#each options.selected as option, index (index)}
              <button
                class="option-badge"
                on:click={(e) => {
                  e.stopPropagation();
                  options.selected = options.selected?.filter(
                    (o) => o.value !== option.value
                  );
                  dispatch("removeItem", {
                    selected: options.selected
                  });
                }}
                >{option.label}
                <span class="remove-btn" title={option.extraData?.title}
                  >&times;</span
                ></button
              >
            {/each}
          {/if}
        {/if}
      </div>
      <button
        class="clear-btn"
        type="button"
        title={options.removeAllTitle}
        on:click={(e) => {
          e.stopPropagation();
          options.selected = [];
          dispatch("removeAllItems", {
            selected: options.selected
          });
        }}>&times;</button
      >
      <div class="divider" />
      <div class="caret" />
      <ul class="options {options.show ? 'show' : ''}">
        {#if options.optionsList}
          {#each options.optionsList as option, index (index + +"" + option.value + "" + index)}
            <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
            <li
              class={`option ${
                options.selected?.includes(option) ? "selected" : ""
              } ${highlightedIndex === index ? "highlighted" : ""}`}
              data-value={option.value}
              data-index={index}
              on:mouseenter={() => (highlightedIndex = index)}
              on:click={(e) => select(e, option)}
            >
              <div class="">
                <div>
                  {options.isLabel ? option.label + "" : ""}
                  <slot id={uuidv4()} name="option" {option} />
                </div>
              </div>
            </li>
          {/each}
        {/if}
      </ul>
    </div>
    {#if options.isError}
      <div class="text-danger">
        <small class="fw-bold">{options.errorMessage} </small>, {options.hint}
      </div>
    {/if}
  </div>
</div>

<style>
  .select-container {
    position: relative;
    width: 100%;
    min-height: 0.9em;
    border: 0.05em solid #777;
    display: flex;
    align-items: center;
    gap: 0.5em;
    padding: 0.5em;
    border-radius: 0.5em;
    outline: none;
    font-size: 0.9rem;
    color: #333;
    cursor: pointer;
    background-color: var(--secondary-color);
    transition: all 0.3s ease-in-out;
  }
  .disabled {
    pointer-events: none;
    opacity: 0.6;
  }
  .place {
    color: #777;
    opacity: 0.8;
    font-weight: 500;
    background-color: var(--secondary-color) !important;
  }

  .select-container:focus {
    border-color: hsl(200, 100%, 50%);
  }
  .select-container::selection {
    background-color: var(--secondary-color);
  }
  .value {
    flex-grow: 1;
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
  }
  .option-badge {
    display: flex;
    align-items: center;
    border: 0.05em solid #777;
    border-radius: 0.25em;
    padding: 0.15em 0.5em;
    gap: 0.25em;
    background-color: rgb(43 81 95);
    color: var(--text-light);
    outline: none;
    cursor: pointer;
    color: white;
  }
  .option-badge:hover,
  .option-badge:focus {
    background-color: hsl(0, 100%, 90%);
    border-color: hsl(0, 100%, 50%);
    color: #000;
  }

  .option-badge > .remove-btn {
    cursor: pointer;
    font-size: 1.25rem;
    color: #777;
    background: none;
    border: none;
    outline: none;
  }
  .option-badge:hover > .remove-btn,
  .option-badge:focus > .remove-btn {
    color: hsl(0, 100%, 50%);
    transition: all 0.3s ease-in-out;
  }
  .clear-btn {
    background: none;
    border: none;
    outline: none;
    cursor: pointer;
    font-size: 1.5em;
    transition: all 0.2s ease;
    padding: 0;
    color: #000;
  }

  .clear-btn:hover,
  .clear-btn:focus {
    color: #444;
  }

  .divider {
    width: 0.05em;
    align-self: stretch;
    background: #777;
  }
  .caret {
    translate: 0 35%;
    border-left: 0.35em solid transparent;
    border-right: 0.35em solid transparent;
    border-top: 0.35em solid #777;
  }
  .select-container:focus .caret {
    border-top: 0.35em solid hsl(200, 100%, 50%);
  }

  .options {
    position: absolute;
    margin: 0;
    padding: 0;
    list-style: none;
    display: none;
    max-height: 15em;
    overflow-y: auto;
    border: 0.05em solid #777;
    border-radius: 0.25em;
    width: 100%;
    left: 0;
    top: calc(100% + 0.25em);
    background-color: white;
    z-index: 100;
    transition: all 0.3s ease-in-out;
  }

  .options.show {
    display: block;
  }

  .option {
    cursor: pointer;
    padding: 0.25em 0.5em;
    transition: all 0.2s ease-in-out;
    font-size: 1.2em;
    position: relative;
  }

  .option.selected:nth-child(n-2) {
    background-color: var(--primary-color);
    border-bottom: 0.15em #aaa solid;
    border-top: 0.15em #aaa solid;
    color: #000;
  }
  .option:hover {
    background-color: hsl(200, 100%, 50%);
    color: white !important;
  }
  .option.highlighted {
    background-color: hsl(200, 100%, 50%);
    color: rgb(15, 4, 4) !important;
  }
  .remove-label {
    width: 0.15em;
    height: 0.1em;
    position: absolute;
    right: 0.5em;
    top: -0.15em;
    cursor: pointer;
    display: none;
  }
  .option.selected:hover,
  .option.selected.highlighted {
    background-color: var(--error-color) !important;
    color: white;
  }

  .option.selected:hover .remove-label,
  .option.selected.highlighted .remove-label {
    display: inline;
  }
</style>
