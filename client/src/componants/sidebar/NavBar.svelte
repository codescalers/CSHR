<script lang="ts">
    import { Link, Router } from 'svelte-navigator';
    import { UserStore } from '../../utils/stores';
</script>

<Router>
    <nav class="nav">
        <div>
            <Link to="/" class="nav_logo" style="margin-left: -10px;margin-bottom: 3px;">                
                <img title="Codescalers" alt="threefold logo" src="/assets/images/codescalers_icon_white.png" style="width: 40px;"/>
                <span class="nav_logo-name">Codescalers</span>
            </Link>
            <div class="nav_list">
                <Link to="/" class="nav_link">
                    <i title="Calendar" class="fa-solid fa-calendar-days nav_icon" />
                    <span class="nav_name">Calendar</span>
                </Link>
                <Link to="/notifications/" class="nav_link">
                    <i title="Notifications" class="fa fa-bell nav_icon" />
                    <span class="nav_name">Notifications</span>
                </Link>
                <Link to="/requests" class="nav_link">
                    <i title="Requests" class="fa-solid fa-code-pull-request nav_icon"></i>
                    <span class="nav_name">Requests</span>
                </Link>
                {#if $UserStore && $UserStore.user_type === "User"}
                    <Link to="/team/" class="nav_link">
                        <i title="Team" class="fa fa-briefcase nav_icon" aria-hidden="true"></i>
                        <span class="nav_name">Team</span>
                    </Link>
                    <!-- <Link to="/hr_letters/" class="nav_link">
                        <i title="HR letter" class="fa fa-newspaper nav_icon" aria-hidden="true"></i>
                        <span class="nav_name">HR letter</span>
                    </Link>
                    <Link to="/offcial-document/" class="nav_link">
                        <i title="Offcial document" class="fa fa-file-text nav_icon" aria-hidden="true"></i>
                        <span class="nav_name">Offcial document</span>
                    </Link> -->
                    <!-- <Link to="/compensations/" class="nav_link">
                        <i title="Compensations" class="fa fa-sticky-note nav_icon" aria-hidden="true"></i>
                        <span class="nav_name">Compensations</span>
                    </Link> -->
                {/if}
                <Link to="/users/" class="nav_link">
                    <i title="Employees" class="fa-solid fa-users nav_icon" />
                    <span class="nav_name">Employees</span>
                </Link>
                {#if $UserStore && $UserStore.user_type === "Admin"}
                    <Link to="/dashboard/" class="nav_link">
                        <i title="Dashboard" class="fa fa-bar-chart nav_icon" aria-hidden="true"></i>
                        <span class="nav_name">Dashboard</span>
                    </Link>
                {/if}
                <Link to="/settings/" class="nav_link">
                    <i title="Settings" class="fa-solid fa-gear nav_icon" />
                    <span class="nav_name">Settings</span>
                </Link>
            </div>
        </div>
        <Link to="/logout/" class="nav_link">
            <i title="SignOut" class="bx bx-log-out nav_icon" />
            <span class="nav_name">SignOut</span>
        </Link>
    </nav>
</Router>