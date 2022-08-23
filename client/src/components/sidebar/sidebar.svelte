<script>
    import Ad from "svelte-gestalt-icons/lib/Ad.svelte";
    import { Datepicker } from 'svelte-calendar';

</script>

<main>
    <br/>
    <br/>
    <br/>
  Details <br/>
  <Ad/>  Birthday <br/>
  <br/>
  <Ad/>  Days Off <br/>
    <br/>
  <Ad/>  Schedule <br/>
    <div class="datePicker">
  <Datepicker/>
</div>
    <div class="flex-container">
      <button class="types">Leave</button>
      <button type="button" class="types">Meeting</button>
      <button type="button" class="types">Event</button>
    </div>
    
   
    <div class="items">
    <label>
      Date <input type="text" name="date" />
    </label>
    <label>
      Add People <input type="text" name="add people" />
    </label>
    <label>
      Location <input type="text" name="location" />
    </label>
  </div>
    <button class="submit">Submit</button>


</main>

<style>
  .datePicker {
    margin: 1cm;
  }
.flex-container {
  display: flex;
  flex-grow: 1;   
  align-items: flex-start;
  background-color:blanchedalmond;
  width: 25%;
}
.items {
  align-items: flex-start;
}
.types {
  appearance: button;
  background-color: #4D4AE8;
  background-image: linear-gradient(180deg, rgba(255, 255, 255, .15), rgba(255, 255, 255, 0));
  border: 1px solid #4D4AE8;
  border-radius: 1rem;
  box-shadow: rgba(255, 255, 255, 0.15) 0 1px 0 inset,rgba(46, 54, 80, 0.075) 0 1px 1px;
  box-sizing: border-box;
  color: #FFFFFF;
  cursor: pointer;
  display: inline-block;
  font-family: Inter,sans-serif;
  font-size: 1rem;
  font-weight: 500;
  line-height: 1.5;
  margin: 0.5cm;
  padding: .5rem 1rem;
  text-align: center;
  text-transform: none;
  transition: color .15s ease-in-out,background-color .15s ease-in-out,border-color .15s ease-in-out,box-shadow .15s ease-in-out;
  user-select: none;
  -webkit-user-select: none;
  touch-action: manipulation;
  vertical-align: middle;
}
.submit {
  appearance: none;
  backface-visibility: hidden;
  background-color: #2f80ed;
  border-radius: 10px;
  border-style: none;
  box-shadow: none;
  box-sizing: border-box;
  color: #fff;
  cursor: pointer;
  display: inline-block;
  font-family: Inter,-apple-system,system-ui,"Segoe UI",Helvetica,Arial,sans-serif;
  font-size: 15px;
  font-weight: 500;
  height: 50px;
  letter-spacing: normal;
  line-height: 1.5;
  outline: none;
  overflow: hidden;
  padding: 14px 30px;
  position: relative;
  text-align: center;
  text-decoration: none;
  transform: translate3d(0, 0, 0);
  transition: all .3s;
  width: 20%;
  margin: 0.25cm;
  margin-left: 1cm;
  user-select: none;
  -webkit-user-select: none;
  touch-action: manipulation;
  vertical-align: top;
  white-space: nowrap;
}
label {
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  text-align: left;
  width: 400px;
  line-height: 26px;
  margin-bottom: 10px;
}

input {
  height: 20px;
  flex: 0 0 200px;
  margin-left: 10px;
}
</style>