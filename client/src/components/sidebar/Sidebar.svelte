<script lang="ts">
  import { Router, Link } from 'svelte-routing';
  import { onMount } from 'svelte';
  import Footer from '../footer/Footer.svelte';
  import { UserStore, NotificationStore } from '../../stores';
  import LoadingComponent from '../loader/LoadingComponent.svelte';
  import ErrorComponent from '../error/ErrorComponent.svelte';

  onMount(() => {
    const showNavbar = (
      toggleId: string,
      navId: string,
      bodyId: string,
      headerId: string
    ) => {
      const toggle = document.getElementById(toggleId),
        nav = document.getElementById(navId),
        bodypd = document.getElementById(bodyId),
        headerpd = document.getElementById(headerId);

      // Validate that all variables exist
      if (toggle && nav && bodypd && headerpd) {
        toggle.addEventListener('click', () => {
          // show navbar
          nav.classList.toggle('show');
          // change icon
          toggle.classList.toggle('bx-x');
          // add padding to body
          bodypd.classList.toggle('body-pd');
          // add padding to header
          headerpd.classList.toggle('body-pd');
        });
      }
    };

    showNavbar('header-toggle', 'nav-bar', 'body-pd', 'header');

    /*===== LINK ACTIVE =====*/
    const linkColor = document.querySelectorAll('.nav_link');

    function colorLink(this: any) {
      if (linkColor) {
        linkColor.forEach((l) => l.classList.remove('active'));
        this.classList.add('active');
      }
    }
    linkColor.forEach((l) => l.addEventListener('click', colorLink));

    // Your code to run since DOM is loaded and ready
  });

  export let isLoading = false;
  export let isError: boolean | null = null;
</script>
 {#if $UserStore}
<div id="body-pd">
  <header class="header" id="header">
    <div class="header_toggle">
      <i class="bx bx-menu" id="header-toggle" />
      <slot name="page-name" />
    </div>
    <div class="d-flex flex-row gap-4">
      <div>
        <Link to="/notifications" class="position-relative">
          <p class="mt-2">
            <i class="bi bi-bell notification-btn" />
            {#if $NotificationStore.length > 0}
              <span
                style="background: var(--primary-color); "
                class="position-absolute top-5 start-100 translate-middle badge rounded-pill"
              >
                +{$NotificationStore.length}
                <span class="visually-hidden  bg-primary">unread messages</span>
              </span>
            {/if}
          </p>
        </Link>
      </div>
      <h6 class="py-2 text-muted">{$UserStore.full_name}</h6>
      <div class="header_img">
        <Link to={'/profile/' + $UserStore.id}>
          <div
            class={`circular_img`}
            style={`background-image:url(${
              process.env.APP_BASE_API_URL + $UserStore.image
            });background-color:${
              $UserStore.gender === 'Male' ? '#2986cc' : '#FB5858'
            };border:1.5px solid ${
              $UserStore.gender === 'Male' ? 'var(--secondary-color)' : 'pink'
            }`}
            data-bs-toggle="tooltip"
            title={$UserStore.full_name + ' #' + $UserStore.team}
          />
        </Link>
      </div>
    </div>
  </header>
  <div class="l-navbar" id="nav-bar">
    <nav class="nav">
      <Router>
        <div>
          <Link to="/" class="nav_logo">
            <i class="bx bx-layer nav_logo-icon" />
            <span class="nav_logo-name">Threefold</span>
          </Link>
          <div class="nav_list">
            <Link to="/" class="nav_link">
              <i class="fa-solid fa-calendar-days nav_icon" />
              <span class="nav_name">Calendar</span>
            </Link>
            <Link to="/notifications" class="nav_link">
              <i class="fa-solid fa-ticket nav_icon" />
              <span class="nav_name">Notifications</span>
            </Link>
            <Link to="/requests" class="nav_link">
              <i class="fa-solid fa-users nav_icon" />
              <span class="nav_name">Requests</span>
            </Link>
            <Link to="/employee-info" class="nav_link">
              <i class="fa-solid fa-lightbulb nav_icon" />
              <span class="nav_name">Employment Info</span>
            </Link>
            <Link to="/reports" class="nav_link">
              <i class="fa-solid fa-id-card nav_icon" />
              <span class="nav_name">Reports</span>
            </Link>
            <a href="/evaluation-form" class="nav_link">
              <i class="fa-solid fa-book nav_icon" />
              <span class="nav_name">Evaluation Form</span>
            </a>
            <a href="#submenu3" data-bs-toggle="collapse" class="nav_link">
              <i class="fa-solid fa-gear nav_icon" />
              <span class="nav_name">Settings</span>
            </a>
            <ul
              class="collapse nav flex-column  ms-1"
              id="submenu3"
              data-bs-parent="#menu"
            >
              <li class="w-100">
                <Link to="/public-info" class="nav_link">
                  <i class="fa-solid fa-id-badge nav_icon" />
                  <span class="nav_name">Public info</span>
                </Link>
              </li>
              <li class="w-100">
                <Link to="/personal-info" class="nav_link">
                  <i class="fa-solid fa-user-secret nav_icon" />
                  <span class="nav_name">Personal info</span>
                </Link>
              </li>
              <li class="w-100">
                <Link to="/emergency-contacts" class="nav_link">
                  <i class="fa-solid fa-address-book nav_icon" />
                  <span class="nav_name">Emergency Contact</span>
                </Link>
              </li>
              <li class="w-100">
                <Link to="/my-docs" class="nav_link">
                  <i class="fa-solid fa-file-lines nav_icon" />
                  <span class="nav_name">My Docs</span>
                </Link>
              </li>
            </ul>
          </div>
        </div>
        <Link to="/signout" class="nav_link">
          <i class="bx bx-log-out nav_icon" />
          <span class="nav_name">SignOut</span>
        </Link>
      </Router>
    </nav>
  </div>
  <div class="height-100 bg-light d-flex flex-column justify-content-between">
    <section class="fluid-container mt-5 content">
      {#if isError}
        <ErrorComponent
          errorMessage="please try to reload page and raise an issues"
        />
      {:else if isLoading}
        <LoadingComponent />
      {:else}
        <slot name="content" {isError} {isLoading} />
      {/if}
    </section>
    <Footer />
  </div>
</div>
{/if}
<style>
  .notification-btn {
    color: var(--primary-color);
    border: 1px solid var(--primary-color);
    cursor: pointer;
    border-radius: 50%;
    padding: 0.75rem;
    transition: all 0.2s ease-in-out;
  }
  .notification-btn:hover {
    background-color: var(--secondary-color);
    border: 1px solid var(--secondary-color);
  }
  .content {
    height: fit-content;
  }
</style>
