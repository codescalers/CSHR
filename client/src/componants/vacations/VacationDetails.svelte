<script lang="ts">
    import Error from '../../pages/Error.svelte';
    import { onMount } from 'svelte';
    import { Route } from 'svelte-navigator';
    import Loading from '../ui/Loading.svelte';
    import Vacation from '../../apis/vacations/Vacation';
    import ProfileImage from '../profile/ProfileImage.svelte';
    import { RequestStatus } from '../../utils/enums';
    import Submit from '../ui/Button.svelte';
    import { UserStore } from '../../utils/stores';
    import { tweened } from 'svelte/motion';
    import ActionButton from '../requests/requestsButtons.svelte';
    import { Link } from 'svelte-navigator';
    import { navigate } from 'svelte-navigator';
    import Requests from "../../apis/requests/Requests"

    export let isLoading = false;
    export let isError: boolean | null = null;

    var path = window.location.pathname;
    const vacationID = path.split("/")[2];
    let vacation: any, thisComment: string|null = null;

    let original = 0 * 60; // TYPE NUMBER OF SECONDS HERE
    let timer = tweened(original)
    const enableTimer = () => {
        setInterval(() => {
            if ($timer >= 0) $timer++;
        }, 1000);        
    };

    $: minutes = Math.floor($timer / 60);
    $: formDisable = thisComment == null || thisComment == "";

    if (! +vacationID){
        isError = true;
    }

    onMount(async () => {
        isLoading = true;
        try {
            vacation = await Vacation.vacatioDetails(+vacationID);
        } catch (error) {
        isError = true;
        }
        isLoading = false;
    });

    const handleActions = (event: { detail: { text: any; }; }) => {
        const sRequest = event.detail.text
        vacation.status = vacation.status
        vacation.status = sRequest.status
        vacation.change_log = vacation.change_log
        vacation.approval_user = $UserStore
        vacation.change_log.push(
            {"user": $UserStore, "comment": `${$UserStore.full_name} ${vacation.status} your vacation`}
        )
    }
</script>

{#if isError}
    <Route>
        <Error error={404} />
    </Route>
{/if}

{#if isLoading}
  <div class="d-flex justify-content-center align-items-center height-100">
    <Loading className={"loader"}/>
  </div>
{/if}
{#if vacation}
    <div class="container">
        {#if $UserStore.user_type == "Supervisor"}
            <div class="mb-4" style="width: 20%;">
                <ActionButton request = {vacation} on:message={handleActions}/>
            </div>
        {/if}
        {#if $UserStore.user_type == "User" && vacation.status == RequestStatus.pinding}
            <div class="d-flex display-buttons">
                <Link to="/vacation/{vacation.id}/update" class="abtn btn-primary mb-2 custom-a"
                    style="color: #fff"
                    >
                    <span class="nav_name">Update Vacation</span>
                </Link>
                <button on:click={async() => {
                    await Requests.delete(vacation);
                    navigate('/', { replace: true });
                }} class="abtn btn-danger mb-2 custom-a"
                    style="color: #fff"
                    >
                    <span class="nav_name">Delete vacation</span>
                </button>
            </div>
            <small class="text-muted text-center">
                Hint: Once you click on the delete button the request will delete without any confirmation
            </small>
        {/if}
        <div class="card p-4 d-flex justify-content-center">
            <div class="row">
                <div class="col-6">
                    <p>Applying User</p>
                </div>
                <div class="col-6 d-flex">
                    <ProfileImage user={vacation.applying_user}/>
                    <p class="p-2">{vacation.applying_user.full_name}</p>
                </div>
                <div class="col-6">
                    <p>Approval User</p>
                </div>
                <div class="col-6 d-flex">
                    {#if vacation.approval_user.email != ""}
                        <ProfileImage user={vacation.approval_user}/>
                        <p class="p-2">{vacation.approval_user.full_name}</p>
                    {:else}
                        <p class="p-2 text-muted">
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-hourglass-bottom" viewBox="0 0 16 16">
                                <path d="M2 1.5a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 0 1h-1v1a4.5 4.5 0 0 1-2.557 4.06c-.29.139-.443.377-.443.59v.7c0 .213.154.451.443.59A4.5 4.5 0 0 1 12.5 13v1h1a.5.5 0 0 1 0 1h-11a.5.5 0 1 1 0-1h1v-1a4.5 4.5 0 0 1 2.557-4.06c.29-.139.443-.377.443-.59v-.7c0-.213-.154-.451-.443-.59A4.5 4.5 0 0 1 3.5 3V2h-1a.5.5 0 0 1-.5-.5zm2.5.5v1a3.5 3.5 0 0 0 1.989 3.158c.533.256 1.011.791 1.011 1.491v.702s.18.149.5.149.5-.15.5-.15v-.7c0-.701.478-1.236 1.011-1.492A3.5 3.5 0 0 0 11.5 3V2h-7z"/>
                            </svg>
                            Under aprroving...
                        </p>
                    {/if}
                </div>
                <div class="col-6">
                    <p>Start Date</p>
                </div>
                <div class="col-6">
                    <p>{vacation.from_date}</p>
                </div>
                <div class="col-6">
                    <p>End Date</p>
                </div>
                <div class="col-6">
                    <p>{vacation.end_date}</p>
                </div>
                <div class="col-6">
                    <p>Reason</p>
                </div>
                <div class="col-6">
                    <p>{vacation.reason}</p>
                </div>
                <div class="col-6">
                    <p>Status</p>
                </div>
                <div class="col-6">
                    <p class="text-muted">
                        {#if vacation.status == RequestStatus.pinding}
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-hourglass-bottom text-muted" viewBox="0 0 16 16">
                                <path d="M2 1.5a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 0 1h-1v1a4.5 4.5 0 0 1-2.557 4.06c-.29.139-.443.377-.443.59v.7c0 .213.154.451.443.59A4.5 4.5 0 0 1 12.5 13v1h1a.5.5 0 0 1 0 1h-11a.5.5 0 1 1 0-1h1v-1a4.5 4.5 0 0 1 2.557-4.06c.29-.139.443-.377.443-.59v-.7c0-.213-.154-.451-.443-.59A4.5 4.5 0 0 1 3.5 3V2h-1a.5.5 0 0 1-.5-.5zm2.5.5v1a3.5 3.5 0 0 0 1.989 3.158c.533.256 1.011.791 1.011 1.491v.702s.18.149.5.149.5-.15.5-.15v-.7c0-.701.478-1.236 1.011-1.492A3.5 3.5 0 0 0 11.5 3V2h-7z"/>
                            </svg>
                        {:else if vacation.status == RequestStatus.approved}
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-check2-all text-success" viewBox="0 0 16 16">
                                <path d="M12.354 4.354a.5.5 0 0 0-.708-.708L5 10.293 1.854 7.146a.5.5 0 1 0-.708.708l3.5 3.5a.5.5 0 0 0 .708 0l7-7zm-4.208 7-.896-.897.707-.707.543.543 6.646-6.647a.5.5 0 0 1 .708.708l-7 7a.5.5 0 0 1-.708 0z"/>
                                <path d="m5.354 7.146.896.897-.707.707-.897-.896a.5.5 0 1 1 .708-.708z"/>
                            </svg>
                        {:else}
                            <!-- Rejacted -->
                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-lg text-danger" viewBox="0 0 16 16">
                                <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z"/>
                            </svg>
                        {/if}
                        {vacation.status}
                    </p>
                </div>
                <form>
                    <div class="form-group">
                        <label for="comment" class="mb-4">Leave Comment</label>
                        <textarea bind:value={thisComment} class="form-control" id="comment"></textarea>
                    </div>
                    <div class="mt-3 pt-3 d-flex justify-content-center align-items-center w-100">
                        <Submit
                          width={"20"}
                          bind:disabled={formDisable}
                          className=""
                          successMessage={'Comment Submited!'}
                          errorMessage={'Something went wrong with your request!'}
                          label="Comment"
                          onClick={async () => {
                            isLoading = true;
                            try {
                                await Vacation.comment(+vacationID, {
                                    comment: thisComment
                                });
                                vacation.change_log = vacation.change_log
                                vacation.change_log.push(
                                    {"user": $UserStore, "comment": thisComment}
                                )
                            
                            } catch (error) {
                                isError = true;
                            } finally {
                                isLoading = false;
                                thisComment = ''
                            }
                            return isError;
                          }}
                        />
                      </div>
                </form>
                
            </div>
        </div>
        <div class="card mt-4 p-4 card-comments d-flex justify-content-center">
            <h5 class="text-center">Change log</h5>
            {#if vacation.change_log.length > 0}
                <div class="row">
                    {#each vacation.change_log as comment}
                        {#if comment.user.id == $UserStore.id}
                            <div class="col-12 mt-4 d-flex card p-4 d-flex justify-content-end left-card">
                                <div class="row">
                                    <div class="col-12 d-flex">
                                        <ProfileImage user={comment.user}/>
                                        <p class="p-2">{comment.user.full_name}</p>
                                        {#if comment.commented_at == undefined}
                                            <span class="d-none">{enableTimer()}</span>
                                            {#if minutes == 0}
                                                <p class="p-2 text-muted">Just now</p>
                                            {:else}
                                                <p class="p-2 text-muted">Posted from {minutes} min</p>
                                            {/if}
                                        {:else}
                                            <p class="p-2 text-muted">{comment.commented_at}</p>
                                        {/if}
                                    </div>
                                    <div class="col-12">
                                        <p class="p-2 mb-0">{comment.comment}</p>
                                    </div>
                                </div>
                            </div>
                        {:else}
                            <div class="col-12 mt-4 d-flex card p-4 d-flex justify-content-center right-card">
                                <div class="row">
                                    <div class="col-12 d-flex">
                                        <ProfileImage user={comment.user}/>
                                        <p class="p-2">{comment.user.full_name}</p>
                                        <p class="p-2 text-muted">{comment.commented_at}</p>
                                    </div>
                                    <div class="col-12">
                                        <p class="p-2 mb-0">{comment.comment}</p>
                                    </div>
                                </div>
                            </div>
                        {/if}
                    {/each}
                </div>
            {/if}
        </div>
    </div>
{/if}


<style>
    textarea{
        max-height: 250px;
    }
    .right-card{
        width: 55%;
        margin-left: 565px;
        border-radius: 0px 50px 50px 50px;
        background: rgb(240 248 255);
    }
    .left-card{
        width: 55%;
        border-radius: 50px 0px 50px 50px;
        background: rgb(220 226 231);
    }

    .custom-a:hover{
        color: #fff !important;
    }
    .display-buttons{
        flex-direction: column;
        width: 20%
    }
</style>
