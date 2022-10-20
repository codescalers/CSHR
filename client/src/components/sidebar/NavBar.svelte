<script lang="ts">
    import { Link, Router } from 'svelte-navigator';
    import { UserStore } from '../../stores';
</script>
<Router>
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
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-bell-fill" viewBox="0 0 16 16">
                    <path d="M8 16a2 2 0 0 0 2-2H6a2 2 0 0 0 2 2zm.995-14.901a1 1 0 1 0-1.99 0A5.002 5.002 0 0 0 3 6c0 1.098-.5 6-2 7h14c-1.5-1-2-5.902-2-7 0-2.42-1.72-4.44-4.005-4.901z"/>
                </svg>
                <span class="nav_name">Notifications</span>
            </Link>
            {#if $UserStore.user_type === "Supervisor"}
                <Link to="/requests" class="nav_link">
                    <i class="fa-solid fa-users nav_icon" />
                    <span class="nav_name">Requests</span>
                </Link>
            {/if}
            {#if $UserStore.user_type === "User"}
                <Link to="/team" class="nav_link">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-microsoft-teams nav_icon" viewBox="0 0 16 16">
                        <path d="M9.186 4.797a2.42 2.42 0 1 0-2.86-2.448h1.178c.929 0 1.682.753 1.682 1.682v.766Zm-4.295 7.738h2.613c.929 0 1.682-.753 1.682-1.682V5.58h2.783a.7.7 0 0 1 .682.716v4.294a4.197 4.197 0 0 1-4.093 4.293c-1.618-.04-3-.99-3.667-2.35Zm10.737-9.372a1.674 1.674 0 1 1-3.349 0 1.674 1.674 0 0 1 3.349 0Zm-2.238 9.488c-.04 0-.08 0-.12-.002a5.19 5.19 0 0 0 .381-2.07V6.306a1.692 1.692 0 0 0-.15-.725h1.792c.39 0 .707.317.707.707v3.765a2.598 2.598 0 0 1-2.598 2.598h-.013Z"/>
                        <path d="M.682 3.349h6.822c.377 0 .682.305.682.682v6.822a.682.682 0 0 1-.682.682H.682A.682.682 0 0 1 0 10.853V4.03c0-.377.305-.682.682-.682Zm5.206 2.596v-.72h-3.59v.72h1.357V9.66h.87V5.945h1.363Z"/>
                    </svg>
                    <span class="nav_name">Team</span>
                </Link>
            {/if}
            <Link to="/users" class="nav_link">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-microsoft-teams nav_icon" viewBox="0 0 16 16">
                    <path d="M9.186 4.797a2.42 2.42 0 1 0-2.86-2.448h1.178c.929 0 1.682.753 1.682 1.682v.766Zm-4.295 7.738h2.613c.929 0 1.682-.753 1.682-1.682V5.58h2.783a.7.7 0 0 1 .682.716v4.294a4.197 4.197 0 0 1-4.093 4.293c-1.618-.04-3-.99-3.667-2.35Zm10.737-9.372a1.674 1.674 0 1 1-3.349 0 1.674 1.674 0 0 1 3.349 0Zm-2.238 9.488c-.04 0-.08 0-.12-.002a5.19 5.19 0 0 0 .381-2.07V6.306a1.692 1.692 0 0 0-.15-.725h1.792c.39 0 .707.317.707.707v3.765a2.598 2.598 0 0 1-2.598 2.598h-.013Z"/>
                    <path d="M.682 3.349h6.822c.377 0 .682.305.682.682v6.822a.682.682 0 0 1-.682.682H.682A.682.682 0 0 1 0 10.853V4.03c0-.377.305-.682.682-.682Zm5.206 2.596v-.72h-3.59v.72h1.357V9.66h.87V5.945h1.363Z"/>
                </svg>
                <span class="nav_name">Employees</span>
            </Link>
            {#if $UserStore.user_type === "Admin"}
                <Link to="/dashboard" class="nav_link">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-bar-chart-line-fill" viewBox="0 0 16 16">
                        <path d="M11 2a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v12h.5a.5.5 0 0 1 0 1H.5a.5.5 0 0 1 0-1H1v-3a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v3h1V7a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v7h1V2z"/>
                    </svg>
                    <span class="nav_name">Dashboard</span>
                </Link>
            {/if}
            <a href="/team" data-bs-toggle="collapse" class="nav_link">
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
        <Link to="auth/logout/" class="nav_link">
            <i class="bx bx-log-out nav_icon" />
            <span class="nav_name">SignOut</span>
        </Link>
    </nav>
</Router>