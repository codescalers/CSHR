<script lang="ts">
    import type { SelectOptionType } from '../../types';
  
    export let option: SelectOptionType;
    let full_name: string = option.extraData.full_name;
    let team: string = option.extraData.team;
  
    let hidden = false;
  </script>
  
  <div class="option" title={`#${team}`}>
    <span>{full_name}</span>
  </div>
  
  <style>
    .option {
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    div span {
      font-size: 1rem;
      font-weight: 400;
      text-align: right;
    }
  </style>