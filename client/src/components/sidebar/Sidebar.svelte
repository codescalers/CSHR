<script lang="ts">
    import Header from "./Header.svelte"
    import NavBar from "./NavBar.svelte"
    import PageFooter from "./PageFooter.svelte"

    document.addEventListener("DOMContentLoaded", function(_) {
        const showNavbar = (toggleId: string, navId: string, bodyId: string, headerId: string, pageContent: string) =>{
            const toggle = document.getElementById(toggleId),
                nav = document.getElementById(navId),
                bodypd = document.getElementById(bodyId),
                headerpd = document.getElementById(headerId),
                pagecontent = document.getElementById(pageContent)
            if(toggle && nav && bodypd && headerpd && pagecontent){
                toggle.addEventListener('click', ()=>{
                    nav.classList.toggle('show-side-bar')
                    toggle.querySelector('i').classList.toggle('bx-x')
                    bodypd.classList.toggle('body-pd')
                    headerpd.classList.toggle('body-pd')
                    pagecontent.classList.toggle('page-content')
                }) 
            }
    }

    showNavbar('hamburger-icon','nav-bar','body-pd','header', "page-content")
    const linkColor = document.querySelectorAll('.nav_link')
    function colorLink(this: any){
        if(linkColor){
            linkColor.forEach(l=> l.classList.remove('active'))
            this.classList.add('active')
        }
    }
    linkColor.forEach(l=> l.addEventListener('click', colorLink))
        // Your code to run since DOM is loaded and ready
    });
</script>

<Header />
<NavBar />
<section>
    <div class="container-fluid body-content" id="page-content">
        <slot name="content"></slot>
    </div>
</section>
<PageFooter />