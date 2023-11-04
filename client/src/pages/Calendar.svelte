<script lang="ts">
    import Calendar from "../componants/calendar/Calender.svelte";
    import CalendarEventsFilter from "../componants/calendar/CalendarEventsFilter.svelte";
    import CalendarEventForm from "../componants/calendar/CalendarForm.svelte";
		import { dayNames, initMonthItems, initMonth} from "../utils/calendar"
		import { findRowCol } from "../utils/calendar"
    import type { calendarItemsType, eventNameType } from '../utils/types';
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
		'public_holiday'
	]);
	
	$: month, year, initContent();

</script>
<Sidebar>
	<div slot="content">
		<div class="p-4">
			<div class="row">
				<div class="col-4">
					<CalendarEventsFilter bind:eventNames />
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
				<div class="col-8 d-flex align-center">
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
	</div>
</Sidebar>
