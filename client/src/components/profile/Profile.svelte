<script lang="ts">
  import { UserStore } from "../../stores";
  import { onMount } from "svelte";
  import { useParams } from "svelte-navigator";
  import usersDataService from "../../services/axios/users/UsersDataService";
  import type { UserInterface } from "../../types";

  const params = useParams();
  let id: number = Number($params.id);
  export let isLoading = false;
  export let isError: boolean | null = null;
  let user: UserInterface;
  onMount(async () => {
    isLoading = true;
    try {
      if ($UserStore.id !== id) {
        user = await usersDataService.getById(id);
      } else if ($UserStore.id === id) {
        if (!$UserStore) {
          user = await usersDataService.getById(id);
          $UserStore = user;
        } else {
          user = $UserStore;
        }
        user = await usersDataService.getById(id);
      }
    } catch (error) {
      isError = true;
    }
    isLoading = false;
  });
</script>

{#if !isError && !isLoading && user}
  <div class="container ">
    <div class="row">
      <div class="col-lg-4">
        <div class="card mb-4">
          <div class="card-body text-center">
            <div
              class={`my-2  mx-auto card-img-top circular_img`}
              style={`background-image:url(${
                process.env.APP_BASE_API_URL + user.image
              });background-color:${
                user.gender === "Male" ? "#2986cc" : "#FB5858"
              };border:1.5px solid ${
                user.gender === "Male" ? "var(--secondary-color)" : "pink"
              }`}
              data-bs-toggle="tooltip"
              title={user.full_name + " #" + user.team}
            />

            <h5 class="my-3">{user.full_name}</h5>
            <p class="text-muted mb-1">{user.job_title}</p>
            <p class="text-muted mb-4">{user.address}</p>
          </div>
        </div>

        <div class="card mb-4 mb-lg-0">
          <div class="card-body p-0">
            <ul class="list-group list-group-flush rounded-3">
              <li
                class="list-group-item d-flex justify-content-between align-items-center p-3"
              >
                <i class="bi bi-telegram icon" style="color:#27A1E0;" />
                <a class="mb-0" href={user.telegram_link}>telegram</a>
              </li>
              <li
                class="list-group-item d-flex justify-content-between align-items-center p-3"
              >
                <i class="bi bi-github icon" style="color: #333333;" />
                <p class="mb-0">github</p>
              </li>
              <!--       <li
              class="list-group-item d-flex justify-content-between align-items-center p-3"
            >
              <i class="fab fa-twitter fa-lg" style="color: #55acee;" />
              <p class="mb-0">twitter</p>
            </li>
            <li
              class="list-group-item d-flex justify-content-between align-items-center p-3"
            >
              <i class="fab fa-instagram fa-lg" style="color: #ac2bac;" />
              <p class="mb-0">instagram</p>
            </li>
            <li
              class="list-group-item d-flex justify-content-between align-items-center p-3"
            >
              <i class="fab fa-facebook-f fa-lg" style="color: #3b5998;" />
              <p class="mb-0">facebook</p> 
            </li>-->
            </ul>
          </div>
        </div>
      </div>
      <div class="col-lg-8">
        <div class="card mb-4">
          <div class="card-body">
            <div class="row">
              <div class="col-sm-3">
                <p class="mb-0">Full Name</p>
              </div>
              <div class="col-sm-9">
                <p class="text-muted mb-0">{user.full_name}</p>
              </div>
            </div>
            <hr />
            <div class="row">
              <div class="col-sm-3">
                <p class="mb-0">Email</p>
              </div>
              <div class="col-sm-9">
                <p class="text-muted mb-0">{user.email}</p>
              </div>
            </div>
            <hr />
            <div class="row">
              <div class="col-sm-3">
                <p class="mb-0">Team</p>
              </div>
              <div class="col-sm-9">
                <p class="text-muted mb-0">{user.team}</p>
              </div>
            </div>
            <hr />
            <div class="row">
              <div class="col-sm-3">
                <p class="mb-0">Phone Number</p>
              </div>
              <div class="col-sm-9">
                <p class="text-muted mb-0">{user.phone_number}</p>
              </div>
            </div>
            <hr />
            <div class="row">
              <div class="col-sm-3">
                <p class="mb-0">Address</p>
              </div>
              <div class="col-sm-9">
                <p class="text-muted mb-0">{user.address}</p>
              </div>
            </div>
          </div>
        </div>
        <div class="row">
          <div class="col-md-6">
            <div class="card mb-4 mb-md-0">
              <div class="card-body">
                <p class="mb-4">
                  <span class="text-primary font-italic me-1"
                    ><i class="bi bi-tools icon" /></span
                  >
                  Skills
                </p>
                <p class="mb-1" style="font-size: .77rem;">Web Design</p>
                <div class="progress rounded" style="height: 5px;">
                  <div
                    class="progress-bar"
                    role="progressbar"
                    style="width: 80%"
                    aria-valuenow="80"
                    aria-valuemin="0"
                    aria-valuemax="100"
                  />
                </div>
                <p class="mt-4 mb-1" style="font-size: .77rem;">
                  Website Markup
                </p>
                <div class="progress rounded" style="height: 5px;">
                  <div
                    class="progress-bar"
                    role="progressbar"
                    style="width: 72%"
                    aria-valuenow="72"
                    aria-valuemin="0"
                    aria-valuemax="100"
                  />
                </div>
                <p class="mt-4 mb-1" style="font-size: .77rem;">One Page</p>
                <div class="progress rounded" style="height: 5px;">
                  <div
                    class="progress-bar"
                    role="progressbar"
                    style="width: 89%"
                    aria-valuenow="89"
                    aria-valuemin="0"
                    aria-valuemax="100"
                  />
                </div>
                <p class="mt-4 mb-1" style="font-size: .77rem;">
                  Mobile Template
                </p>
                <div class="progress rounded" style="height: 5px;">
                  <div
                    class="progress-bar"
                    role="progressbar"
                    style="width: 55%"
                    aria-valuenow="55"
                    aria-valuemin="0"
                    aria-valuemax="100"
                  />
                </div>
                <p class="mt-4 mb-1" style="font-size: .77rem;">Backend API</p>
                <div class="progress rounded mb-2" style="height: 5px;">
                  <div
                    class="progress-bar"
                    role="progressbar"
                    style="width: 66%"
                    aria-valuenow="66"
                    aria-valuemin="0"
                    aria-valuemax="100"
                  />
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-6">
            <div class="card mb-4 mb-md-0">
              <div class="card-body">
                <p class="mb-4">
                  <span class="text-primary font-italic me-1"
                    ><i class="bi bi-bookmark-fill icon" /></span
                  >
                  Certificates
                </p>
                <p class="mb-1" style="font-size: .77rem;">Web Design</p>
                <div class="progress rounded" style="height: 5px;">
                  <div
                    class="progress-bar"
                    role="progressbar"
                    style="width: 80%"
                    aria-valuenow={"80"}
                    aria-valuemin="0"
                    aria-valuemax="100"
                  />
                </div>
                <p class="mt-4 mb-1" style="font-size: .77rem;">
                  Website Markup
                </p>
                <div class="progress rounded" style="height: 5px;">
                  <div
                    class="progress-bar"
                    role="progressbar"
                    style="width: 72%"
                    aria-valuenow="72"
                    aria-valuemin="0"
                    aria-valuemax="100"
                  />
                </div>
                <p class="mt-4 mb-1" style="font-size: .77rem;">One Page</p>
                <div class="progress rounded" style="height: 5px;">
                  <div
                    class="progress-bar"
                    role="progressbar"
                    style="width: 89%"
                    aria-valuenow="89"
                    aria-valuemin="0"
                    aria-valuemax="100"
                  />
                </div>
                <p class="mt-4 mb-1" style="font-size: .77rem;">
                  Mobile Template
                </p>
                <div class="progress rounded" style="height: 5px;">
                  <div
                    class="progress-bar"
                    role="progressbar"
                    style="width: 55%"
                    aria-valuenow="55"
                    aria-valuemin="0"
                    aria-valuemax="100"
                  />
                </div>
                <p class="mt-4 mb-1" style="font-size: .77rem;">Backend API</p>
                <div class="progress rounded mb-2" style="height: 5px;">
                  <div
                    class="progress-bar"
                    role="progressbar"
                    style="width: 66%"
                    aria-valuenow="66"
                    aria-valuemin="0"
                    aria-valuemax="100"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
{/if}

<style>
  .icon {
    font-size: 1.4rem;
  }
</style>
