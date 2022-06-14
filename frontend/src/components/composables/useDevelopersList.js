import {ref, onBeforeMount} from 'vue'

export default function useDevelopersList() {
    let developers_list = ref([])

    const init = () =>{
        developers_list = ref([])
    }

    onBeforeMount(init)

    const listPush = (element) =>{
        this.developers_list.value.push(element)
    }

    return {
        developers_list,
        listPush
    }
}