<script lang="ts">
    import { Link } from 'svelte-navigator';
    import type {
        AdminViewInterface,
        SupervisorViewInterface,
        UserInterface,
    } from '../../types';
    export let user: AdminViewInterface | SupervisorViewInterface | UserInterface;
    let username: string[] = user.full_name.split(' ')    
</script>

<Link to={'/profile/' + user.id}>
    {#if user.image[0] == "#"}
        <span class="user-profile-image rounded-circle"
            style="background-color:{user.image}"
        >
            {username[0][0]}{username[1][0]}
        </span>
    {:else}
        <!-- svelte-ignore a11y-missing-attribute -->
        <img
            src="{process.env.APP_BASE_API_URL + user.image}"
            class="user-profile-image rounded-circle"
        />
    {/if}
</Link>

<style>
    .user-profile-image{
        width: 50px;
        height: 50px;
        color: rgb(245 222 179);
        font-weight: 700;
        justify-content: center;
        align-items: center;
        display: flex;
        border-radius: 50px
    }
</style>
