import {ref, onBeforeMount} from 'vue'

export default function useDevelopersList() {
    let developers_list = ref([])

    const init = () =>{
        developers_list = ref([])
    }

    onBeforeMount(init)

    const listPush = (element) =>{
        console.log(this.developers_list.value)
        this.developers_list.value.push(element)
        console.log(this.developers_list.value)
    }

    return {
        developers_list,
        listPush
    }
}