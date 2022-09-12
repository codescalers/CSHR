<script lang="ts">
    import RequestModal from "../requests/requestModal.svelte"
    import updateVacations from "../../services/axios/requests/vacations";
    import updateLetters from "../../services/axios/requests/hr_letters";
    import updateCompensation from "../../services/axios/requests/compensation"
    import getRequests from "../../services/axios/requests/requests"
    export let request:any, index:number

    
  async function  approve_btn (element: any,index:number) { 
    document.body.style.cursor ='wait';
    if (element.type == "Vacation"){
      console.log("before")
     if(await updateVacations(element.id, { status: "approved"}) ){
      console.log("after"+index)
      
     }
      
    }else if (element.type == "HR letters"){
      
      await updateLetters(element.id, { status: "approved"});
    }else if (element.type == "Compensation"){
      let data:JSON= JSON.parse('{"status":"approved"}')
      await updateCompensation(element.id,data);
    }
    element = await getRequests();
    document.body.style.cursor ='defult';
    console.log(element);
  }
  async function reject_btn(element: any,index:number) {
    document.body.style.cursor='wait';
    if (element.type == "Vacation"){
    
     if (await updateVacations(element.id,{"status":"rejected"})){

     }
      
    }else if (element.type == "HR letters"){
      let data:JSON= JSON.parse('{"status":"rejected"}')
      await updateLetters(element.id,data);
    }else if (element.type == "Compensation"){
      let data:JSON= JSON.parse('{"status":"rejected"}')
      await updateCompensation(element.id,data);
    }
    element = await getRequests();
    document.body.style.cursor='default';
    console.log(element.type,element.id);
  }
  
</script>
<div class="column">
    {#if request.status == "Rejected" || request.status == "rejected"}
      <div class="row align-items-center">
        <div class="col">
          <button
            type="button"
            class="btn btn-danger btn-border btn-sm w-100 "
            disabled>Rejected</button
          >
        </div>
        <div class="col pl-0">
          <button type="button" class=" btn btn-view p-0"
          data-bs-toggle={"modal"}
          data-bs-target={"#modal" + index}
            ><i class="bi bi-eye" /></button
          >
        </div>
      </div>
    {:else if request.status == "Approved" || request.status == "approved"}
      <div
        class="row  align-items-center justify-content-start "
      >
        <div class="col">
          <button
            type="button"
            class="btn btn-success btn-border btn-sm w-100 "
            disabled>Approved</button
          >
        </div>
        <div class="col pl-0">
          <button
            type="button"
            class="btn  btn-view p-0"
            data-bs-toggle={"modal"}
            data-bs-target={"#modal" + index}
            ><i class="bi bi-eye" /></button
          >
          <RequestModal {index}{request}></RequestModal>
        </div>
      </div>
    {:else}
      <div class="row align-items-center">
        <div class="col">
          <button
            type="button"
            on:click={()=>approve_btn(request,index)}
            class="btn btn-success btn-border btn-sm w-100 mb-1"
            >Approve</button
          >
          <button
            type="button"
            
            on:click={()=>reject_btn(request,index)}
            class="btn btn-danger btn-border btn-sm w-100">Reject</button
          >
        </div>
        <div class="col pl-0">
          <button type="button" class="btn btn-view p-0"
          data-bs-toggle={"modal"}
          data-bs-target={"#modal" + index}
            ><i class="bi bi-eye" /></button
          >
        </div>
      </div>
    {/if}
  </div>