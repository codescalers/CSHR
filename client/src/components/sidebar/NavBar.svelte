<script lang="ts">
    import { Link } from 'svelte-navigator';
    import { UserStore } from '../../stores';
</script>

<div class="l-navbar" id="nav-bar">
    <nav class="nav">
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
              <Link to="/profile" class="nav_link">
                <i class="fa-solid fa-lightbulb nav_icon" />
                <span class="nav_name">Employment Info</span>
              </Link>
              {#if $UserStore.user_type === "Admin"}
                <Link to="/register" class="nav_link">
                  <i class="fa-solid fa-plus-circle nav_icon" />
                  <span class="nav_name">add a user</span>
                </Link>
              {/if}
              <Link to="/reports" class="nav_link">
                <i class="fa-solid fa-id-card nav_icon" />
                <span class="nav_name">Reports</span>
              </Link>
              <a href="/evaluation" class="nav_link">
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
          <Link to="/auth/logout/" class="nav_link">
            <i class="bx bx-log-out nav_icon" />
            <span class="nav_name">SignOut</span>
          </Link>
      </nav>
</div>