<script lang="ts">
    import type {
        AdminViewInterface,
        SupervisorViewInterface,
        UserInterface,
    } from '../../types';
    export let user: AdminViewInterface | SupervisorViewInterface | UserInterface | userType;
    export let size: number = 50;

    let username: string[] = user.full_name.split(' ')    
</script>

<a href='/profile/{user.id}'>
    {#if user.image[0] == "#"}
        <span class="user-profile-image rounded-circle"
            style="background-color:{user.image}; width:{size}px; height:{size}px;"
        >
            {username[0][0]}{username[1][0]}
        </span>
    {:else}
        <!-- svelte-ignore a11y-missing-attribute -->
        <img
            src="{process.env.APP_BASE_API_URL + user.image.replace('/', '')}"
            class="user-profile-image rounded-circle"
            style="width:{size}px; height:{size}px;"
        />
    {/if}
</a>

<style>
    .user-profile-image{
        color: #fff;
        font-weight: 700;
        justify-content: center;
        align-items: center;
        display: flex;
        border-radius: 50px
    }
</style>