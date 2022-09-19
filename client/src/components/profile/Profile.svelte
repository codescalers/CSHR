<script lang="ts">
  import { UserStore } from "../../stores";
</script>

<div class="container ">
  <div class="row">
    <div class="col-lg-4">
      <div class="card mb-4">
        <div class="card-body text-center">
          <div
            class={`my-2  mx-auto card-img-top circular_img`}
            style={`background-image:url(${
              process.env.APP_BASE_API_URL + $UserStore.image
            });background-color:${
              $UserStore.gender === "Male" ? "#2986cc" : "#FB5858"
            };border:1.5px solid ${
              $UserStore.gender === "Male" ? "var(--secondary-color)" : "pink"
            }`}
            data-bs-toggle="tooltip"
            title={$UserStore.full_name + " #" + $UserStore.team}
          />

          <h5 class="my-3">{$UserStore.full_name}</h5>
          <p class="text-muted mb-1">{$UserStore.job_title}</p>
          <p class="text-muted mb-4">{$UserStore.address}</p>
          <div class="d-flex justify-content-center mb-2">
            <button type="button" class="btn btn-primary">Email</button>
            <button type="button" class="btn btn-outline-primary ms-1"
              >Call</button
            >
          </div>
        </div>
      </div>

      <div class="card mb-4 mb-lg-0">
        <div class="card-body p-0">
          <ul class="list-group list-group-flush rounded-3">
            <li
              class="list-group-item d-flex justify-content-between align-items-center p-3"
            >
              <a class="bi bi-telegram icon" style="color:#27A1E0;" />
              <a class="mb-0" href={$UserStore.telegram_link}>telegram</a>
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
              <p class="text-muted mb-0">{$UserStore.full_name}</p>
            </div>
          </div>
          <hr />
          <div class="row">
            <div class="col-sm-3">
              <p class="mb-0">Email</p>
            </div>
            <div class="col-sm-9">
              <p class="text-muted mb-0">{$UserStore.email}</p>
            </div>
          </div>
          <hr />
          <div class="row">
            <div class="col-sm-3">
              <p class="mb-0">Team</p>
            </div>
            <div class="col-sm-9">
              <p class="text-muted mb-0">{$UserStore.team}</p>
            </div>
          </div>
          <hr />
          <div class="row">
            <div class="col-sm-3">
              <p class="mb-0">Phone Number</p>
            </div>
            <div class="col-sm-9">
              <p class="text-muted mb-0">{$UserStore.phone_number}</p>
            </div>
          </div>
          <hr />
          <div class="row">
            <div class="col-sm-3">
              <p class="mb-0">Address</p>
            </div>
            <div class="col-sm-9">
              <p class="text-muted mb-0">Bay Area, San Francisco, CA</p>
            </div>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-md-6">
          <div class="card mb-4 mb-md-0">
            <div class="card-body">
              <p class="mb-4">
                <span class="text-primary font-italic me-1"><i class="bi bi-tools icon"></i></span> 
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
              <p class="mt-4 mb-1" style="font-size: .77rem;">Website Markup</p>
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
                <span class="text-primary font-italic me-1"><i class="bi bi-bookmark-fill icon"></i></span> 
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
              <p class="mt-4 mb-1" style="font-size: .77rem;">Website Markup</p>
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

<style>
  .icon {
    font-size: 1.4rem;
  }

</style>
