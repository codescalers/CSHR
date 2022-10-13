<script lang="ts">
  import { navigate } from 'svelte-routing';
  import Input from '../components/input/Input.svelte';
  import LocationSelect from '../components/select/LocationSelect.svelte';
  import PeopleSelect from '../components/select/PeopleSelect.svelte';
  import Sidebar from '../components/sidebar/Sidebar.svelte';
  
  import RegisterDataService from '../services/axios/register/RegisterDataService';
  import type { registeringData } from '../services/axios/register/types';
  const handleSalary=(e:any): boolean=>{
    if(e.target.value>0){
      return false;}
      return  true;
  }
 
  const handleMail = (e: any): boolean => {
    if (
      e.target.value
        .toLowerCase()
        .match(
          /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
        )
    )
      return false;
    return true;
  };

  const handleName = (e: any): boolean => {
    if (e.target.value.match(/\b([A-Z-a-z]+)$/)) return false;
    return true;
  };

  const handleMobile = (e: any): boolean => {
    if (e.target.value.match(/\b(\d{10,15})$/)) return false;
    return true;
  };

  let registeration : registeringData={
    first_name: "",
    last_name: "",
    telegram_link: "",
    email:"",
    birthday:new Date(),
    mobile_number:"",
    password: "",
    location: 0,
    team: "",
    salary: {
  current_salary:{net:[],gross:[]},
  net_salary_before_joining:[],
  joining_salary: {
    net:[],
    gross:[]
  },
  benefits:[] },
  
    user_type:"",
    reporting_to:[],
    gender:  "",
    job_title:"",

  };
   
   
 

 
  let isErrormail: null | boolean = null;
  // let isErrorImage: null | boolean = null;
  let isErrorfName: null | boolean = null;
  let isErrorlName: null | boolean = null;
  let isErrorLink: null | boolean = null;
  let isErrorBirthday: null | boolean = null;
  let isErrorMobile: null | boolean = null;
  let isErrorpass: null | boolean = null;
  let isErrorSuper: null | boolean = null;
  let isErrorLocation: null | boolean = null;
  let isErrorNCSalary: null | boolean = null;
  let isErrorGCSalary: null | boolean = null;
  let isErrorJSalary: null | boolean = null;
  let isErrorNBSalary: null | boolean = null;
  let isErrorBenefits: null | boolean = null;
  let isErrorJobTitle: null | boolean = null;

  let formDisable = (isErrormail === null ||
    isErrorfName === null || isErrorlName===null || isErrorlName||isErrorlName||
    isErrorBirthday||isErrorBirthday===null||isErrorGCSalary||
    isErrorGCSalary===null||isErrorJobTitle||isErrorJobTitle===null||
    isErrorLink===null|| isErrorLocation===null||isErrorMobile||isErrorMobile==null||
    isErrormail||isErrorNCSalary||isErrorNCSalary===null||
    isErrorpass ||isErrorpass===null) as boolean;

    
  $: formDisable = (isErrormail === null ||
    isErrorfName === null || isErrorlName===null || isErrorlName||isErrorlName||
    isErrorBirthday||isErrorBirthday===null||isErrorGCSalary||
    isErrorGCSalary===null||isErrorJobTitle||
    isErrorJobTitle===null||isErrorLink===null|| isErrorLocation===null||isErrorMobile||isErrorMobile==null||
    isErrormail ||isErrorNCSalary||isErrorNCSalary===null||
    isErrorpass ||isErrorpass===null) as boolean;
 
 
  let salaryField = [false,false,false,false]
  let showaddbutton= true;
  const addAField = () => {
    let flag = false;
    let count=0;
  for(var i in salaryField){
    if(salaryField[i]===false){
      if(flag===false){
      salaryField[i]=true;
      flag=true;
    }
    count++;
  }}

  if(count<2)
    showaddbutton = false;
   
  };  
 
//   let myregisteringData:registeringData={
//     first_name : fNameValue,
//     last_name: lNameValue,
//     telegram_link: telegramValue,
//     email: emailValue,
//     birthday:new Date(birthd),
//     mobile_number: mobileValue,
//     password: passwordValue,
//     location: locationValue[0],
//     team: team,
//     salary: mysalary,
//     user_type:userType,
//     reporting_to:  Supervisor,
//     image: imageValue,
//     gender:  GenderValue,
//     job_title: jobTitleValue


//   };
let reportingto:[];
let location:[];
  const submit = async () => {
    let isError = false;
    for (var i in reportingto) {
      registeration.reporting_to[i]=reportingto[i].value;
}

registeration.location=location[0].value
 
  
    
    try {
       await RegisterDataService.register(registeration)

      

      navigate('/', { replace: true });
    } catch (e) {
      isError = true;
    }
    return isError;
  };
</script>

<Sidebar>
  <section class="fluid-container mt-5 content" slot="content">
    <div class="row">
      <div class =" col-5 ms-4">
        <Input
          isTop={false}
          type="text"
          label={'First Name'}
          bind:value={ registeration.first_name}
          handleInput={handleName}
          size={150}
          errorMessage="Invalid Name"
          hint={'please enter a valid first name'}
          placeholder={'Enter first name'}
          bind:isError={isErrorfName}
        /> 
    </div>
    <div class= "col-5 ms-4">
    <Input
    isTop={false}
    type="text"
    label={'Last Name'}
    bind:value={registeration.last_name}
    handleInput={handleName}
    size={150}
    errorMessage="Invalid Name"
    hint={'please enter a valid last name'}
    placeholder={'Enter last name'}
    bind:isError={isErrorlName}
  /> 
  </div>

   <div class="col-5 ms-4">
    
  <Input
  isTop={false}
  type="date"
  label={'Birthday date'}
  bind:value={registeration.birthday}
  handleInput={() => {
    return false;
  }}
  size={150}
  errorMessage="Invalid birthdate"
  hint={'please enter a valid birthday date'}
  placeholder={'Enter birthday date'}
  bind:isError={isErrorBirthday}
/>
</div>

<!-- <div class="col-5 ms-4"> 
<Input
      isTop={false}
      type="file"
      label={'Profile Picture'}
      bind:value={registeration.image}
      handleInput={handleImage}
      size={150}
      errorMessage="image is invalid"
      hint={'please upload a valid image format'}
      placeholder={'upload the user profile image here'}
      bind:isError={isErrorImage}
    />
   </div> -->
<div class="col-5 ms-4" > 
  <Input
  isTop={false}
  type="text"
  label={'Telegram User Name'}
  bind:value={registeration.telegram_link}
  handleInput={() => {
    return false;
  }}
  size={150}
  errorMessage="Invalid Link"
  hint={'please enter a valid Telegram username link'}
  placeholder={'Enter telegram link e.g: @username'}
  bind:isError={isErrorLink}
/>
   
</div>
<div class="col-5 ms-4">
  <Input
  isTop={false}
  type="tel"
  label={'Mobile Number'}
  bind:value={registeration.mobile_number}
  handleInput={handleMobile}
  size={150}
  errorMessage="Invalid Mobile Number"
  hint={'please enter a valid mobile number in range(10, 15) digits'}
  placeholder={'01234567890'}
  bind:isError={isErrorMobile}
/>
 </div> 

 <div class="col-5 ms-4">
  <Input
  isTop={false}
  type="email"
  label={'Email'}
  bind:value={registeration.email}
  handleInput={handleMail}
  size={150}
  errorMessage="E-mail is  invalid"
  hint={'please write a valid E-mail format'}
  placeholder={'please enter the user email here'}
  bind:isError={isErrormail}
/>
 </div>
 <div class="col-5 ms-4">
  <Input
  isTop={false}
  type="password"
  label={'Password'}
  bind:value={registeration.password}
  handleInput={() => {
    return false;
  }}
  size={400}
  errorMessage="Password is  invalid"
  hint={'please write a valid password'}
  placeholder={'please enter your password here'}
  bind:isError={isErrorpass}
/>
</div>
<div class="col-5 ms-4">
  <Input
  isTop={false}
  
  type="text"
  label={'Job Title'}
  bind:value={registeration.job_title}
  handleInput={()=>{
     
    return false;
  }}
  size={150}
  errorMessage="job title is  invalid"
  hint={'please write a valid job title'}
  placeholder={'please the job title here'}
  bind:isError={isErrorJobTitle}
/>
</div>
 


<div class="form-group row  col-5 ms-4 mt-3">
       
  <label class="ps-0 mb-2" for="myselect2"
    >User Type</label
  >
  
<select
  bind:value={registeration.user_type}
  class="custom-select"
  id="myselect2"
>
  <option selected>Choose...</option>
  <option value="Admin">Admin</option>
  <option value="Supervisor">Supervisor</option>
  <option value="User">User</option>
</select>
</div>



<div class="form-group row col-5 ms-4 mt-3 me-1"  >
       
  <label for=myselect1 class="ps-0 mb-2">Team</label>
    
<select bind:value={registeration.team} class="custom-select" id="myselect1">
  <option value="Development">Development</option>
  <option value="Q&A">Q&A</option>
  <option value="Operations">Operations</option>
  <option value="Marketing">Marketing</option>
  <option value="Management">Management</option>
  <option value="Accounting">Accounting</option>
</select>
</div>

<div class="form-group row  col-5 ms-4 mt-3">
  <label class="ps-0 mb-2" for="myselect3"
      >Gender</label>
     
  <select
    bind:value={registeration.gender}
    class="custom-select"
    id="myselect3">
  <option value="Female">Female</option>
    <option value="Male">Male</option>
    </select>

</div>
<div class="col-5 ms-4">
<PeopleSelect
 isTop={false}
 mylabel= {"Supervisors"}
 bind:isError={isErrorSuper} 
 bind:selected={reportingto} />
</div>

<div class="col-5 ms-4">
 <LocationSelect
        mylabel= {"Location"}
        bind:isError={isErrorLocation}
        bind:selected={location}
        isTop={false}
      />
    </div>
</div>
 
 <div class="row p-3 m-3 border">
  <div class="col-5 ms-4">
      <Input
        isTop={false}
        type="number"
        label={'Net Current Salary'}
        bind:value={registeration.salary.current_salary.net[0]}
        handleInput={handleSalary}
        size={20}
        errorMessage="invalid salary value"
        hint={'please enter the net current salary for the employee'}
        placeholder={'Enter the net current salary'}
        bind:isError={isErrorNCSalary}
      />
    </div>
  
    <div class="col-5 ms-4">
      <Input
        isTop={false}
        type="number"
        label={'Gross Current Salary'}
        bind:value={registeration.salary.current_salary.gross[0]}
        handleInput={handleSalary}
        size={20}
        errorMessage="invalid salary value"
        hint={'please enter the gross current salary for the employee'}
        placeholder={'Enter the gross current salary'}
        bind:isError={isErrorGCSalary}
      />
      </div>

      {#if salaryField[0]==true}
      <div class="col-4  ms-4" >
      <Input  
        isTop={false}
        type="number"
        label={'Net Joining Salary'}
        bind:value={ registeration.salary.joining_salary.net[0]}
        handleInput={handleSalary}
        size={20}
        errorMessage="invalid salary value"
        hint={'please enter the net joining salary for the employee'}
        placeholder={'Enter the net joining salary'}
        bind:isError={isErrorJSalary}
      />
      </div>
      <div class="col-1 mt-5 pe-0">
      <button
      type="button"
      class="btn btn-light  minusbutton"
      on:click|preventDefault={()=>{salaryField[0]=false; showaddbutton=true;}}>➖</button>
      </div>
    
      {/if}
      {#if salaryField[1]==true}
      <div class="col-4 ms-4">
      <Input
        isTop={false}
        type="number"
        label={'Gross Joining Salary'}
        bind:value={registeration.salary.joining_salary.gross[0]}
        handleInput={handleSalary}
        size={20}
        errorMessage="invalid salary value"
        hint={'please enter the gross joining salary for the employee'}
        placeholder={'Enter the gross joining salary'}
        bind:isError={isErrorJSalary}
      />
    </div>
    <div class="col-1 mt-5 pe-0">
      <button
      type="button"
      class="btn btn-light  minusbutton"
      on:click|preventDefault={()=>{salaryField[1]=false;showaddbutton=true;}}>➖</button>
      </div>
      {/if}
      
      {#if salaryField[2]==true}
      <div class="col-4 ms-4"> 
      <Input
      isTop={false}
  
      type="number"
      label={'Net Salary before joining'}
      bind:value={registeration.salary.net_salary_before_joining[0]}
      handleInput={handleSalary}
      size={20}
      errorMessage="invalid salary value"
      hint={'please enter the net salary before joining for the employee'}
      placeholder={'Enter the net salary before joining'}
      bind:isError={isErrorNBSalary}
    />
  </div>
  <div class="col-1 mt-5 pe-0">
    <button
    type="button"
    class="btn btn-light  minusbutton"
    on:click|preventDefault={()=>{salaryField[2]=false; showaddbutton=true;}}>➖</button>
    </div>
    {/if}

    {#if salaryField[3]==true }
    <div class="col-4 ms-4">
    <Input
    isTop={false}
     
    type="number"
    label={'Benefits'}
    bind:value={registeration.salary.benefits[0]}
    handleInput={handleSalary}
    size={20}
    errorMessage="invalid salary value"
    hint={'please enter the benefits for the employee'}
    placeholder={'Enter the benefits'}
    bind:isError={isErrorBenefits}
  />
</div>
<div class="col-1 mt-5 pe-0">
  <button
  type="button"
  class="btn btn-light  minusbutton"
  on:click|preventDefault={()=>{salaryField[3]=false;showaddbutton=true;}}>➖</button>
  </div>
  {/if}
      {#if  showaddbutton==true}
      <button
        type="button"
        class="col-1 btn btn-light  thebutton"
        on:click|preventDefault={addAField}>➕</button>
      {/if} 
    </div>

    <button
      type="button"
      class="btn submit my-5"
      on:click|preventDefault={submit}>Create User</button> 
  </section>
</Sidebar>

<style>
  .content {
    height: fit-content;
  }
  
  .border {
    border-radius: 25px;
    border-color: dimgrey;
  }
  
   

  .submit {
    margin-top: 0.5cm;
    margin: 0.5cm 1cm 0cm 1cm;
    font-size: 16px;
    color: #2b515f;
    background-color: #eff6ff;
    width: 90%;
    border: 1px solid #2b515f;
  }
  .submit:hover {
    background-color: #2b515f;
    color: #eee;
  }
 
  .custom-select{
    margin-top: 0.3cm;
    height: 40px;
    border-radius: 5px;
    border-color:rgb(194, 192, 192);
    background-color:  var(--secondary-color);
}  
.thebutton{
  height:40px;
  width: 50px;
  margin-top:65px;
  margin-left: 10px;
}
.minusbutton{
  height:40px;
  width: 50px;
  margin-top:20px;
  
}
</style>
