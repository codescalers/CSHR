<script lang="ts">
    import ProfileImage from "../profile/ProfileImage.svelte";
    import NavBar from "./NavBar.svelte"
    import { useNavigate } from 'svelte-navigator';
    import { onMount } from 'svelte';

    import userDataService from '../../services/axios/user/UserDataService';
    import { UserStore } from '../../stores';
    import { authStore } from '../../stores';
  import PageFooter from "./PageFooter.svelte";
    
    let toggleId: HTMLElement, navId: HTMLElement, bodyId: HTMLElement, headerId: HTMLElement, pageContent: HTMLElement;

    const changeSidebar = () => {
        navId.classList.toggle("show-sidebar")
        toggleId.classList.toggle('bx-x')
        bodyId.classList.toggle('body-pd')
        headerId.classList.toggle('body-pd')
        pageContent.classList.toggle('page-content-open')
    }


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

<div id="body-pd" bind:this={bodyId}>
    <header class="header" id="header" bind:this={headerId}>
        <div class="container-fluid">
            <div class="row align-items-center">
                <div class="col-6">
                    <div class="header_toggle"> 
                        <button id="btn header-toggle" bind:this={toggleId} on:click={changeSidebar}>
                            <i class='bx bx-menu'></i>
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
    
    <div class="l-navbar" id="nav-bar" bind:this={navId}>
        <NavBar />
    </div>

    <div class="container-fluid page-content height-100" bind:this={pageContent}>
        <slot name="content"></slot>
    </div>
</div>
<PageFooter />

<style>
    button{
        outline: none;
        border: none;
        background: rgb(0 0 0 / 0%);
    }
</style>
