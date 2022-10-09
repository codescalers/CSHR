<script lang="ts">
    import { useNavigate } from 'svelte-navigator';
    import { onMount } from 'svelte';

    import userDataService from '../../services/axios/user/UserDataService';
    import ProfileImage from '../profile/ProfileImage.svelte';
    import { UserStore } from '../../stores';
    import { authStore } from '../../stores';

    const navigate = useNavigate();
    onMount(async () => {
        if (!authStore.isAuth() || $UserStore === undefined) {
            try {
                $UserStore = await userDataService.getMyProfile();
            } catch (error) {
                return navigate('/login');
            };
        };
    });
</script>

<header class="header" id="header">
    <div class="container-fluid">
        <div class="row align-items-center">
            <div class="col-6">
                <div class="header_toggle">
                    <button type="button" id="hamburger-icon">
                        <i class='bx bx-menu' id="header-toggle"></i>
                    </button>
                </div>
            </div>
            <div class="col-6 d-flex justify-content-end">
                {#if $UserStore}
                    <ProfileImage user={$UserStore}/>
                {/if}
            </div>
        </div>
    </div>
</header>