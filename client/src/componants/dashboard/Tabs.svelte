<script lang="ts">
  // import Evaluation from '../evaluation/Evaluation.svelte';
  // import UserEvaluation from '../evaluation/UserEvaluation.svelte';
  import Office from "../office/Office.svelte";
  import Register from "../register/Register.svelte";
  import UpdateProfile from "../settings/UpdateProfile.svelte";
  import AdjustmentVacationBalance from "../vacations/AdjustmentVacationBalance.svelte";
  import UsersVacationBalanceForm from "../vacations/UsersVacationBalanceForm.svelte";
  // import UserDocuments from "../userdocuments/UserDocuments.svelte"
  import VacationBalance from "../vacations/VacationBalance.svelte";
  import GreatAndHint from "./GreatAndHint.svelte";

  let date: Date = new Date();
  let tab = 1;
</script>

<div class="row w-100 p-4">
  <div class="col-4">
    <div
      class="nav flex-column nav-tabs text-center no-bottom-border"
      id="v-tabs-tab"
      role="tablist"
      aria-orientation="vertical"
    >
      <a
        class="nav-link navtab active mb-2"
        id="v-tabs-vacation-balance-tab"
        data-mdb-toggle="tab"
        href="#v-tabs-vacation-balance"
        role="tab"
        aria-controls="v-tabs-vacation-balance"
        aria-selected="false"
        on:click={() => (tab = 1)}
      >
        Update/Post vacations balance form
      </a>
      <a
        class="nav-link navtab mb-2"
        id="v-tabs-user-vacation-balance-tab"
        data-mdb-toggle="tab"
        href="#v-tabs-user-vacation-balance"
        role="tab"
        aria-controls="v-tabs-user-vacation-balance"
        aria-selected="false"
        on:click={() => (tab = 2)}
      >
        Update/Set user vacation balance form
      </a>
      <a
        class="nav-link navtab mb-2"
        id="v-tabs-Adjustment-vacation-balance-tab"
        data-mdb-toggle="tab"
        href="#v-tabs-Adjustment-vacation-balance"
        role="tab"
        aria-controls="v-tabs-Adjustment-vacation-balance"
        aria-selected="false"
        on:click={() => (tab = 2)}
      >
        Vacation balance adjustment form
      </a>
      <!-- RFNV1.0 <a
        class="nav-link navtab mb-2"
        id="v-tabs-home-tab"
        data-mdb-toggle="tab"
        href="#v-tabs-home"
        role="tab"
        aria-controls="v-tabs-home"
        aria-selected="true"
        >Evaluation Form</a
      > -->
      <!-- RFNV1.0 <a
        class="nav-link navtab mb-2"
        id="v-tabs-user-eval-tab"
        data-mdb-toggle="tab"
        href="#v-tabs-user-eval"
        role="tab"
        aria-controls="v-tabs-user-eval"
        aria-selected="false"
        >User Evaluation Form</a
      > -->
      <!-- RFNV1.0 <a
        class="nav-link navtab mb-2"
        id="v-tabs-user-docs-tab"
        data-mdb-toggle="tab"
        href="#v-tabs-user-docs"
        role="tab"
        aria-controls="v-tabs-user-docs"
        aria-selected="false"
        >User Documents</a
      > -->
      <a
        class="nav-link navtab mb-2"
        id="v-tabs-office-tab"
        data-mdb-toggle="tab"
        href="#v-tabs-office"
        role="tab"
        aria-controls="v-tabs-office"
        aria-selected="false"
        on:click={() => (tab = 6)}
      >
        Add new office form
      </a>
      <a
        class="nav-link navtab mb-2"
        id="v-tabs-new-user-tab"
        data-mdb-toggle="tab"
        href="#v-tabs-new-user"
        role="tab"
        aria-controls="v-tabs-new-user"
        aria-selected="false"
        on:click={() => (tab = 7)}
      >
        Add new user form
      </a>
      <a
        class="nav-link navtab mb-2"
        id="v-tabs-update-user-tab"
        data-mdb-toggle="tab"
        href="#v-tabs-update-user"
        role="tab"
        aria-controls="v-tabs-update-user"
        aria-selected="false"
        on:click={() => (tab = 8)}
      >
        Update user profile form
      </a>
    </div>
  </div>
  <div class="col-8">
    <!-- Tab content -->
    <div class="tab-content" id="v-tabs-tabContent">
      <div
        class="tab-pane fade show active"
        id="v-tabs-vacation-balance"
        role="tabpanel"
        aria-labelledby="v-tabs-vacation-balance-tab"
      >
        <div class="height-100">
          <GreatAndHint
            hint={"You have to update the values every year"}
            header={"this is vacation values of " + date.getFullYear()}
          />
          <VacationBalance bind:tab />
        </div>
      </div>
      <div
        class="tab-pane fade"
        id="v-tabs-user-vacation-balance"
        role="tabpanel"
        aria-labelledby="v-tabs-user-vacation-balance-tab"
      >
        <div class="height-100">
          <GreatAndHint
            header={"This is the user balance of year " + date.getFullYear()}
            hint={""}
          />
          <UsersVacationBalanceForm />
        </div>
      </div>
      <div
        class="tab-pane fade"
        id="v-tabs-Adjustment-vacation-balance"
        role="tabpanel"
        aria-labelledby="v-tabs-Adjustment-vacation-balance-tab"
      >
        <div class="height-100">
          <GreatAndHint
            header={"This is the adjustment vacation balance form"}
            hint={"The 'Vacation Balance Adjustment Form' is utilized by administrators to increment the vacation balance for the entire team. This form is designed for specific instances where an increase in the balance is warranted, such as adding an extra day to the annual leave entitlement. Administrators can provide a reason for the adjustment, ensuring transparency and clarity in the modification of vacation balances for the office team.            "}
          />
          <AdjustmentVacationBalance />
        </div>
      </div>
      <!-- RFNV1.0 <div
      class="tab-pane fade"
      id="v-tabs-home"
      role="tabpanel"
      aria-labelledby="v-tabs-home-tab"
    >
      <div class="height-100">
        <GreatAndHint 
          header={"this is evaluation form of " + date.getFullYear()}
          hint={"Select quarter and link to make it visible to all of users."} 
        />
        <Evaluation />
      </div>
    </div> -->
      <!-- RFNV1.0 <div
      class="tab-pane fade"
      id="v-tabs-user-eval"
      role="tabpanel"
      aria-labelledby="v-tabs-user-eval-tab"
    >
      <div class="height-100">
        <GreatAndHint 
          header={"User evaluation form"}
          hint={"Add evaluation link to a specific user."} 
        />
        <UserEvaluation />
      </div>
    </div> -->
      <!-- RFNV1.0 <div
      class="tab-pane fade"
      id="v-tabs-user-docs"
      role="tabpanel"
      aria-labelledby="v-tabs-user-docs-tab"
    >
      <div class="height-100">
        <GreatAndHint 
          header={"User documents"}
          hint={"You can add any documents related to user by using this form."} 
        />
        <UserDocuments />
      </div>
    </div> -->
      <div
        class="tab-pane fade"
        id="v-tabs-office"
        role="tabpanel"
        aria-labelledby="v-tabs-office-tab"
      >
        <div class="height-100">
          <GreatAndHint
            header={"New Office"}
            hint={"You can add office .e.g. `Codescalers` using this form."}
          />
          <Office />
        </div>
      </div>
      <div
        class="tab-pane fade"
        id="v-tabs-new-user"
        role="tabpanel"
        aria-labelledby="v-tabs-new-user-tab"
      >
        <div>
          <GreatAndHint
            header={"New User"}
            hint={"You can add new user using this form."}
          />
          <Register />
        </div>
      </div>
      <div
        class="tab-pane fade"
        id="v-tabs-update-user"
        role="tabpanel"
        aria-labelledby="v-tabs-update-user-tab"
      >
        <div class="height-100">
          <GreatAndHint
            header={"Update user profile"}
            hint={"You can update the user information using this form."}
          />
          <UpdateProfile />
        </div>
      </div>
    </div>
  </div>
</div>

<style>
  .nav {
    height: auto !important;
  }
  .navtab {
    padding: 15px;
    border-radius: 5px !important;
    transition: 0.3s;
  }
  .no-bottom-border {
    border-bottom: none;
  }
</style>
