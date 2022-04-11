import {ref, onBeforeMount} from 'vue'



export default function useSideBar() {
    let menu = ref([])

    const init = () => {
        
        menu.value = [
                    {
                        id: 1,
                        title: "Home",
                        active: false,
                        class: "nav-link text-white",
                        route: "/"
                    },
                    {
                        id: 2,
                        title: "Dashboards",
                        active: false,
                        class: "nav-link text-white",
                        route: "/dashboards"
                    },
                    {
                        id: 3,
                        title: "Repositories",
                        active: false,
                        class: "nav-link text-white",
                        route: "/repos"
                    },
                    {
                        id: 4,
                        title: "Backlog",
                        active: false,
                        class: "nav-link text-white",
                        route: "/backlog"
                    },
                    {
                        id: 5,
                        title: "Roadmap",
                        active: false,
                        class: "nav-link text-white",
                        route: "/roadmap"
                    },
                    {
                        id: 6,
                        title: "Notifications",
                        active: false,
                        class: "nav-link text-white",
                        route: "/notifications"
                    },
                ]
    }

    onBeforeMount(init);

    const selectSideBarLine = (line) =>{
        for (let i = 0;i<menu.value.length;i++){
            menu.value[i].active = false
            menu.value[i].class = "nav-link text-white"
        }

        line = menu.value.find(x => x.title === line)
        line.active = !line.active

        if (line.active){
            line.class = "nav-link active"
        }
        else{
            line.class = "nav-link text-white"
        }
    }


    return{
        menu,
        selectSideBarLine
    }
    
}