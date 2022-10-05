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

<div class="user-profile-image">
    <Link to={'/profile/' + user.id}>
        {#if user.image[0] == "#"}
            <span class="user-profile-image-p rounded-circle"
                style="background-color:{user.image}"
            >
                {username[0][0]}{username[1][0]}
            </span>
        {:else}
            <!-- svelte-ignore a11y-missing-attribute -->
            <img
                src="{process.env.APP_BASE_API_URL + user.image}"
                class="user-profile-image-img rounded-circle"
            />
        {/if}
    </Link>
</div>

<style>
    .user-profile-image-img{
        width: 50px;
        height: 50px;
    }
    .user-profile-image{
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .user-profile-image-p{
        width: 50px;
        height: 50px;
        color: rgb(245 222 179);
        font-weight: 700;
        justify-content: center;
        align-items: center;
        display: flex;
        margin-right: 5px;
    }
</style>
