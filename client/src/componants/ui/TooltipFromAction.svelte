<script>
	export let title;
	export let x;
	export let y;
</script>
<div style="
		top: {y + 15}px;
		left: {x + 15}px;">{title}</div>

<style>
	div {
		border: 1px solid #ddd;
		box-shadow: 1px 1px 1px #ddd;
		background: white;
		border-radius: 4px;
		padding: 4px;
		position: absolute;
    z-index: 999;
	}
</style>
