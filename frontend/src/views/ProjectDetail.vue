<template>
  <div class="project_detail_view">
      {{project}}
  </div>
</template>

<script>
import axios from 'axios'
import useSideBar from '@/components/composables/useSideBar'

export default {
    name: 'ProjectDetail',
    data(){
        return{
            project: null
        }
    },
    setup(){

      const {menu, selectSideBarLine} = useSideBar()
      return {
        selectSideBarLine,
        menu
      }
    },
    created(){
        this.getProject()
    },
    methods:{
        get(){
            this.$emit('selectSideBarLine', 'Dashboards')
        },
        getProject(){
            console.log(this.$route.query.id)
            axios
                .get(`http://localhost:8000/api/projects/${this.$route.query.id}`, {
                headers: { Authorization: `Bearer ${this.$store.state.accessToken}` },
                })
                .then((response) => {
                  console.log(response.data)
                  this.project = response.data
                  
                })
                .catch((err) => {
                    console.log(err);
                });
        }
    }
}
</script>

<style>

</style>