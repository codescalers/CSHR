<script lang="ts">
    import Calendar from "../componants/calendar/Calender.svelte";
    import CalendarEventsFilter from "../componants/calendar/CalendarEventsFilter.svelte";
    import CalendarEventForm from "../componants/calendar/CalendarForm.svelte";
	import { dayNames, monthNames, initMonthItems, initMonth} from "../utils/calendar"
	import { findRowCol } from "../utils/calendar"
    import type { calendarItemsType, eventItemType, eventNameType, meetingItemType, userDataType, vacationItemType } from '../utils/types';
	import Sidebar from "../componants/sidebar/Sidebar.svelte"
	
    export let isLoading: boolean = false;

	let headers = [];
	let now = new Date();
	let year = now.getFullYear();
	let month = now.getMonth();

	var days: any[] = [];
	var items: calendarItemsType[] = [];
	let item: calendarItemsType;

	
	// choose what date/day gets displayed in each date box.
	async function initContent() {
		isLoading = true;
		headers = dayNames;
		days = initMonth(days, month, year);
		items = await initMonthItems(isLoading, month, year, items, days);
		isLoading = false;
	}
	
	let eventNames: Set<eventNameType> = new Set([
		'event',
		'vacation',
		'meeting',
		'birthday',
	]);
	
	$: month, year, initContent();

</script>
<Sidebar bind:isLoading>
	<div slot="content">
		<div>
			<div
			class="d-flex flex-column-reverse align-items-sm-center flex-xl-row gap-sm-4 gap-xl-1 content homapage"
			>
				<div class="mb-5 mb-xl-0 d-flex flex-lg-column flex-row-reverse mx-5 ">
					<CalendarEventsFilter bind:eventNames/>
					<CalendarEventForm 
						on:message={(event) => {
							if (event.detail.postedVacation){
								item = event.detail.postedVacation
							}
							
							if (event.detail.postedMeeting){
								item = event.detail.postedMeeting
							}
							
							if (event.detail.postedEvent){
								item = event.detail.postedEvent
							}
							items = items;
							if(item){
								items.push(item)
							}
							const itemDate = new Date(item.date);
							let rc = findRowCol(itemDate, days);
							if (rc == null) {
								console.log('didn`t find date for ',item);
								item.startCol = item.startRow = 0;
							} else {
								item.startCol = rc.col;
								item.startRow = rc.row;
							}
						}}
					/>
				</div>
				<Calendar
					bind:month
					bind:year
					bind:eventNames
					bind:items
					bind:isLoading
					{headers}
					{days}
					on:onDelete={(event) => {
						if (items != undefined) {
							items = items.filter((item) => item.id !== event.detail.id);
						} // TODO: delete from server
					}}
				/>
			</div>
		</div>
	</div>
</Sidebar>

<style>
	.content {
	  height: fit-content;
	}
</style>
