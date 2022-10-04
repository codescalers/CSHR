<script lang="ts">
  //import { Router, Link } from "svelte-navigator";
</script>

<div class="container-fluid">
  <header class="header" id="header">
    <div class="header_toggle">
      <i class="fa-solid fa-bars" id="header-toggle" />
    </div>
    <div class="header_img">
      <img src="https://i.imgur.com/hczKIze.jpg" alt="" />
    </div>
  </header>
  <div class="row flex-nowrap">
    <div class="col-auto col-md-3 col-xl-2 px-sm-2 px-0 bg-dark">
      <div
        class="d-flex flex-column align-items-center align-items-sm-start px-3 pt-2 text-white min-vh-100"
      >
        <a
          href="/"
          class="d-flex align-items-center pb-3 mb-md-0 me-md-auto text-white text-decoration-none"
        >
          <span class="fs-5 d-none d-sm-inline">Menu</span>
        </a>
        <ul
          class="nav nav-pills flex-column mb-sm-auto mb-0 align-items-center align-items-sm-start"
          id="menu"
        >
          <li class="nav-item">
            <a href="#" class="nav-link align-middle px-0">
              <i class="fs-4 bi-house" />
              <span class="ms-1 d-none d-sm-inline">Home</span>
            </a>
          </li>
          <li>
            <a
              href="#submenu1"
              data-bs-toggle="collapse"
              class="nav-link px-0 align-middle"
            >
              <i class="fs-4 bi-speedometer2" />
              <span class="ms-1 d-none d-sm-inline">Dashboard</span>
            </a>
            <ul
              class="collapse show nav flex-column ms-1"
              id="submenu1"
              data-bs-parent="#menu"
            >
              <li class="w-100">
                <a href="#" class="nav-link px-0">
                  <span class="d-none d-sm-inline">Item</span> 1
                </a>
              </li>
              <li>
                <a href="#" class="nav-link px-0">
                  <span class="d-none d-sm-inline">Item</span> 2
                </a>
              </li>
            </ul>
          </li>
          <li>
            <a href="#" class="nav-link px-0 align-middle">
              <i class="fs-4 bi-table" />
              <span class="ms-1 d-none d-sm-inline">Orders</span></a
            >
          </li>
          <li>
            <a
              href="#submenu2"
              data-bs-toggle="collapse"
              class="nav-link px-0 align-middle "
            >
              <i class="fs-4 bi-bootstrap" />
              <span class="ms-1 d-none d-sm-inline">Bootstrap</span></a
            >
            <ul
              class="collapse nav flex-column ms-1"
              id="submenu2"
              data-bs-parent="#menu"
            >
              <li class="w-100">
                <a href="#" class="nav-link px-0">
                  <span class="d-none d-sm-inline">Item</span> 1</a
                >
              </li>
              <li>
                <a href="#" class="nav-link px-0">
                  <span class="d-none d-sm-inline">Item</span> 2</a
                >
              </li>
            </ul>
          </li>
          <li>
            <a
              href="#submenu3"
              data-bs-toggle="collapse"
              class="nav-link px-0 align-middle"
            >
              <i class="fs-4 bi-grid" />
              <span class="ms-1 d-none d-sm-inline">Products</span>
            </a>
            <ul
              class="collapse nav flex-column ms-1"
              id="submenu3"
              data-bs-parent="#menu"
            >
              <li class="w-100">
                <a href="#" class="nav-link px-0">
                  <span class="d-none d-sm-inline">Product</span> 1</a
                >
              </li>
              <li>
                <a href="#" class="nav-link px-0">
                  <span class="d-none d-sm-inline">Product</span> 2</a
                >
              </li>
              <li>
                <a href="#" class="nav-link px-0">
                  <span class="d-none d-sm-inline">Product</span> 3</a
                >
              </li>
              <li>
                <a href="#" class="nav-link px-0">
                  <span class="d-none d-sm-inline">Product</span> 4</a
                >
              </li>
            </ul>
          </li>
          <li>
            <a href="#" class="nav-link px-0 align-middle">
              <i class="fs-4 bi-people" />
              <span class="ms-1 d-none d-sm-inline">Customers</span>
            </a>
          </li>
        </ul>
        <hr />
        <div class="dropdown pb-4">
          <a
            href="#"
            class="d-flex align-items-center text-white text-decoration-none dropdown-toggle"
            id="dropdownUser1"
            data-bs-toggle="dropdown"
            aria-expanded="false"
          >
            <img
              src="https://github.com/mdo.png"
              alt="hugenerd"
              width="30"
              height="30"
              class="rounded-circle"
            />
            <span class="d-none d-sm-inline mx-1">loser</span>
          </a>
          <ul class="dropdown-menu dropdown-menu-dark text-small shadow">
            <li><a class="dropdown-item" href="#">New project...</a></li>
            <li><a class="dropdown-item" href="#">Settings</a></li>
            <li><a class="dropdown-item" href="#">Profile</a></li>
            <li>
              <hr class="dropdown-divider" />
            </li>
            <li><a class="dropdown-item" href="#">Sign out</a></li>
          </ul>
        </div>
      </div>
    </div>
    <div class="col py-3">
      <slot />
    </div>
  </div>
</div>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700&display=swap');
  :root {
    --header-height: 3rem;
    --nav-width: 68px;
    --first-color: #4723d9;
    --first-color-light: #afa5d9;
    --white-color: #f7f6fb;
    --body-font: 'Nunito', sans-serif;
    --normal-font-size: 1rem;
    --z-fixed: 100;
  }
  *,
  ::before,
  ::after {
    box-sizing: border-box;
  }
  body {
    position: relative;
    margin: var(--header-height) 0 0 0;
    padding: 0 1rem;
    font-family: var(--body-font);
    font-size: var(--normal-font-size);
    transition: 0.5s;
  }
  a {
    text-decoration: none;
  }
  .header {
    width: 100%;
    height: var(--header-height);
    position: fixed;
    top: 0;
    left: 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 1rem;
    background-color: var(--white-color);
    z-index: var(--z-fixed);
    transition: 0.5s;
  }
  .header_toggle {
    color: var(--first-color);
    font-size: 1.5rem;
    cursor: pointer;
  }
  .header_img {
    width: 35px;
    height: 35px;
    display: flex;
    justify-content: center;
    border-radius: 50%;
    overflow: hidden;
  }
  .header_img img {
    width: 40px;
  }
  .l-navbar {
    position: fixed;
    top: 0;
    left: -30%;
    width: var(--nav-width);
    height: 100vh;
    background-color: var(--first-color);
    padding: 0.5rem 1rem 0 0;
    transition: 0.5s;
    z-index: var(--z-fixed);
  }
  .nav {
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    overflow: hidden;
  }
  .nav_logo,
  .nav_link {
    display: grid;
    grid-template-columns: max-content max-content;
    align-items: center;
    column-gap: 1rem;
    padding: 0.5rem 0 0.5rem 1.5rem;
  }
  .nav_logo {
    margin-bottom: 2rem;
  }
  .nav_logo-icon {
    font-size: 1.25rem;
    color: var(--white-color);
  }
  .nav_logo-name {
    color: var(--white-color);
    font-weight: 700;
  }
  .nav_link {
    position: relative;
    color: var(--first-color-light);
    margin-bottom: 1.5rem;
    transition: 0.3s;
  }
  .nav_link:hover {
    color: var(--white-color);
  }
  .nav_icon {
    font-size: 1.25rem;
  }
  .show {
    left: 0;
  }
  .body-pd {
    padding-left: calc(var(--nav-width) + 1rem);
  }
  .active {
    color: var(--white-color);
  }
  .active::before {
    content: '';
    position: absolute;
    left: 0;
    width: 2px;
    height: 32px;
    background-color: var(--white-color);
  }
  .height-100 {
    height: 100vh;
  }
  @media screen and (min-width: 768px) {
    body {
      margin: calc(var(--header-height) + 1rem) 0 0 0;
      padding-left: calc(var(--nav-width) + 2rem);
    }
    .header_img {
      width: 40px;
      height: 40px;
    }
    .header_img img {
      width: 45px;
    }
    .l-navbar {
      left: 0;
      padding: 1rem 1rem 0 0;
    }
    .show {
      width: calc(var(--nav-width) + 156px);
    }
    .body-pd {
      padding-left: calc(var(--nav-width) + 188px);
    }
  }
</style>
