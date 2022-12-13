<script lang="ts">
  import Button from "../componants/ui/Button.svelte"

  import Input from '../componants/ui/Input.svelte';
  import authenticationAPI from '../apis/authentication/Authentication';
  import { validateEmail } from '../utils/validations';
  import type { loggingData } from '../utils/types';
  import { authStore } from '../utils/stores';
  
  let passwordValue: string;
  let emailValue: string;
  let successMessage: string;
  let errorMessage: string;
  let isErrormail: null | boolean = null;
  let isErrorpass: null | boolean = null;

  let formDisable = (isErrormail === true ||
    isErrorpass === true ||
    isErrormail ||
    isErrorpass) as boolean;
  
  $: formDisable = 
    isErrormail === true ||
    isErrormail === null ||
    isErrorpass === null ||
    isErrorpass === true;

  const submit = async () => {
    let isError = false;
    try { 
      const response = await authenticationAPI.login(
        emailValue,
        passwordValue
      );
      const loggingData: loggingData = response.results
      successMessage = response.message

      authStore.updateTokens(
        loggingData.access_token,
        loggingData.refresh_token
      );

      window.location.href = "/"
    } catch (error) {
      errorMessage = error.message
      isError = true;
    }
    return isError;
  };
</script>

<div class="card m-auto mt-5 pt-5">
  <img alt="threefold logo" src="/assets/images/codescalers_icon.png" />
  <h3>Sign In</h3>
  <div class="mb-1 input">
    <Input
      isTop={false}
      className="myInput"
      type="email"
      label={'Email'}
      bind:value={emailValue}
      handleInput={validateEmail}
      size={255}
      errorMessage="E-mail is  invalid"
      hint={'please write a valid E-mail format'}
      placeholder={'please enter your email here'}
      bind:isError={isErrormail}
    />
  </div>
  <div class="mb-1 input">
    <Input
      isTop={false}
      type="password"
      label={'Password'}
      bind:value={passwordValue}
      className="myInput"
      handleInput={() => {
        return false;
      }}
      errorMessage="Password is  invalid"
      hint={'please write a valid password'}
      placeholder={'please enter your password here'}
      bind:isError={isErrorpass}
    />
  </div>
  <div class="mt-3 pt-3 d-flex justify-content-center align-items-center w-100">
    <Button
      width={"250"}
      disabled={formDisable}
      successMessage={successMessage}
      errorMessage={errorMessage}
      label="Login"
      onClick={submit}
    />
  </div>
</div>
  
<svg
  id="visual"
  style="transform:rotate(0deg); transition: 0.3s"
  viewBox="0 0 1440 430"
  version="1.1"
  xmlns="http://www.w3.org/2000/svg"
  ><defs
    ><linearGradient id="sw-gradient-0" x1="0" x2="0" y1="1" y2="0"
      ><stop stop-color="rgba(8.295, 28.398, 65.624, 1)" offset="0%" /><stop
        stop-color="rgba(7.837, 21.303, 42.856, 1)"
        offset="100%"
      /></linearGradient
    ></defs
  ><path
    style="transform:translate(0, 0px); opacity:1"
    fill="url(#sw-gradient-0)"
    d="M0,344L120,351.2C240,358,480,373,720,322.5C960,272,1200,158,1440,121.8C1680,86,1920,129,2160,172C2400,215,2640,258,2880,293.8C3120,330,3360,358,3600,336.8C3840,315,4080,244,4320,186.3C4560,129,4800,86,5040,57.3C5280,29,5520,14,5760,14.3C6000,14,6240,29,6480,35.8C6720,43,6960,43,7200,35.8C7440,29,7680,14,7920,64.5C8160,115,8400,229,8640,258C8880,287,9120,229,9360,193.5C9600,158,9840,143,10080,157.7C10320,172,10560,215,10800,200.7C11040,186,11280,115,11520,114.7C11760,115,12000,186,12240,193.5C12480,201,12720,143,12960,121.8C13200,100,13440,115,13680,143.3C13920,172,14160,215,14400,250.8C14640,287,14880,315,15120,308.2C15360,301,15600,258,15840,200.7C16080,143,16320,72,16560,64.5C16800,57,17040,115,17160,143.3L17280,172L17280,430L17160,430C17040,430,16800,430,16560,430C16320,430,16080,430,15840,430C15600,430,15360,430,15120,430C14880,430,14640,430,14400,430C14160,430,13920,430,13680,430C13440,430,13200,430,12960,430C12720,430,12480,430,12240,430C12000,430,11760,430,11520,430C11280,430,11040,430,10800,430C10560,430,10320,430,10080,430C9840,430,9600,430,9360,430C9120,430,8880,430,8640,430C8400,430,8160,430,7920,430C7680,430,7440,430,7200,430C6960,430,6720,430,6480,430C6240,430,6000,430,5760,430C5520,430,5280,430,5040,430C4800,430,4560,430,4320,430C4080,430,3840,430,3600,430C3360,430,3120,430,2880,430C2640,430,2400,430,2160,430C1920,430,1680,430,1440,430C1200,430,960,430,720,430C480,430,240,430,120,430L0,430Z"
  /><defs
    ><linearGradient id="sw-gradient-1" x1="0" x2="0" y1="1" y2="0"
      ><stop stop-color="rgba(8.937, 10.697, 47.409, 1)" offset="0%" /><stop
        stop-color="rgba(11.167, 16.832, 61.07, 1)"
        offset="100%"
      /></linearGradient
    ></defs
  ><path
    style="transform:translate(0, 50px); opacity:0.9"
    fill="url(#sw-gradient-1)"
    d="M0,0L120,43C240,86,480,172,720,207.8C960,244,1200,229,1440,207.8C1680,186,1920,158,2160,121.8C2400,86,2640,43,2880,50.2C3120,57,3360,115,3600,172C3840,229,4080,287,4320,272.3C4560,258,4800,172,5040,136.2C5280,100,5520,115,5760,121.8C6000,129,6240,129,6480,136.2C6720,143,6960,158,7200,143.3C7440,129,7680,86,7920,71.7C8160,57,8400,72,8640,121.8C8880,172,9120,258,9360,301C9600,344,9840,344,10080,315.3C10320,287,10560,229,10800,179.2C11040,129,11280,86,11520,64.5C11760,43,12000,43,12240,50.2C12480,57,12720,72,12960,93.2C13200,115,13440,143,13680,136.2C13920,129,14160,86,14400,121.8C14640,158,14880,272,15120,308.2C15360,344,15600,301,15840,293.8C16080,287,16320,315,16560,272.3C16800,229,17040,115,17160,57.3L17280,0L17280,430L17160,430C17040,430,16800,430,16560,430C16320,430,16080,430,15840,430C15600,430,15360,430,15120,430C14880,430,14640,430,14400,430C14160,430,13920,430,13680,430C13440,430,13200,430,12960,430C12720,430,12480,430,12240,430C12000,430,11760,430,11520,430C11280,430,11040,430,10800,430C10560,430,10320,430,10080,430C9840,430,9600,430,9360,430C9120,430,8880,430,8640,430C8400,430,8160,430,7920,430C7680,430,7440,430,7200,430C6960,430,6720,430,6480,430C6240,430,6000,430,5760,430C5520,430,5280,430,5040,430C4800,430,4560,430,4320,430C4080,430,3840,430,3600,430C3360,430,3120,430,2880,430C2640,430,2400,430,2160,430C1920,430,1680,430,1440,430C1200,430,960,430,720,430C480,430,240,430,120,430L0,430Z"
  />
</svg>
  
<svelte:head>
  <style>
    body{
        padding-left: 0 !important;
        padding-right: 0 !important;
    }
    :global(.myInput label) {
        color: #9fa2b4;
        font-weight: bold;
        text-transform: uppercase;
        font-size: 12px;
    }

    :global(.myInput input) {
        color: #4b506d;

        background-color: #fff !important;
    }
    :global(.myInput input::placeholder) {
        color: #525568;
        font-weight: 200;
    }

    :global(.myInput .py-3) {
        padding-bottom: 0rem !important;
    }

    .card {
        display: flex;
        align-items: center;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
        padding: 20px 20px 20px 20px;
        height: 480px;
        width: 400px;
    }
    .card:hover {
        box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
    }
    img {
        height: 50px;
        width: 50px;
    }
  </style>
  
</svelte:head>
  
  