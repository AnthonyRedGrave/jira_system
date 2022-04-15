<template>
  <div class="project_detail_view">
      {{project}}
  </div>
</template>

<script>
export default {
    name: 'ProjectDetail',
    data(){
        return{
            project: null
        }
    },
    methods:{
        getProject(){
            axios
                .get(`http://localhost:8000/api/projects/${this.$route.query.id}`, {
                headers: { Authorization: `Bearer ${this.$store.state.accessToken}` },
                })
                .then((response) => {
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