<script lang="ts">
  import { v4 as uuidv4 } from 'uuid';

  type SelectOption = {
    label: any;
    value: any;
    extraData?: any;
  };

  export let options: SelectOption[] = [],
    selected: SelectOption[] = [],
    label: string = 'choose',
    placeholder = `Select`,
    removeAllTitle = 'Remove all',
    multiple: boolean = true,
    errorMessage: string = 'Please select an option',
    hint: string = multiple
      ? 'you can choose multiple options'
      : 'you can choose only one option',
    isTop: boolean = true,
    className: string = '',
    isError: boolean | null = null,
    show: boolean = true;
  let id: string = uuidv4();
</script>

<div class={`form-group row ${className}`}>
  <label for={id} class={`${isTop ? 'col-sm-4' : ''} col-form-label py-3`}
    >{label}</label
  >
  <div class={`${isTop ? 'col-sm-8' : 'col-sm-12'}`}>
    <div
      on:blur={() => (show = false)}
      on:click={() => (show = !show)}
      tabIndex="0"
      class="select-container select"
    >
      <span class="value">
        {#if selected.length > 0}
          {#each selected as option}
            <span class="selected-value">{option.label}</span>
          {/each}
        {:else}
          <span class="placeholder bg-white"> {placeholder}</span>
        {/if}
      </span>
      <button
        class="clear-btn"
        type="button"
        title={removeAllTitle}
        on:click={(e) => {
          e.stopPropagation();
          selected = [];
        }}>&times;</button
      >
      <div class="divider" />
      <div class="caret" />
      <ul class="options" class:show>
        {#each options as option, index (index + +'' + option.value + '' + index)}
          <li
            class={`option ${selected.includes(option) ? 'selected' : ''}`}
            data-value={option.value}
            on:click={(e) => {
              e.stopPropagation();
              if (multiple) {
                if (selected.includes(option)) {
                  selected = selected.filter(
                    (item) => item.value !== option.value
                  );

                  selected = selected.filter(
                    (item) => item.value !== option.value
                  );
                } else {
                  selected = [...selected, option];
                }
              } else {
                selected = [option];
              }
            }}
          >
            <span class="label">{option.label}</span>
          </li>
        {/each}
      </ul>
    </div>
    {#if isError}
      <div class="text-danger">
        <small class="fw-bold">{errorMessage} </small>, {hint}
      </div>
    {/if}
  </div>
</div>

<style>
  .select-container {
    position: relative;
    width: 20em;
    min-height: 1.5em;
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
    transition: all 0.3s ease-in-out;
  }

  .select-container:focus {
    border-color: hsl(200, 100%, 50%);
  }
  .select-container::selection {
    background-color: var(--secondary-color);
  }
  .value {
    flex-grow: 1;
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
  }

  .option.selected:nth-child(n-2) {
    background-color: var(--primary-color);
    border-bottom: 0.15em #aaa solid;
    color: white;
  }
  .option:hover {
    background-color: hsl(200, 100%, 50%);
    color: white !important;
  }
  .option.selected:hover {
    background-color: var(--error-color) !important;
    color: white;
  }
</style>
