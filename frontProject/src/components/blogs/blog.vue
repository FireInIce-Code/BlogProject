<template>
  <div class="bg">
      <div class="content">
          <h1>
              {{data.blog.title}}
          </h1>
          <hr>
          <div class="inner" v-html="data.blog.inner">
              {{data.blog.inner}}
          </div>
      </div>
  </div>
</template>

<script>
import Axios from "axios"
export default {
    data(){
        return {
            data:null
        }
    },
    methods:{
        getData(){
            Axios.get("/api/page/blog?id="+this.$route.params.id).then((response)=>{
                var data=response.data;
                if(data.message=="success"){
                    this.data=data;
                }else if(data.message=="the id is wrong"){
                    this.$router.push("/Error/404");
                }
            })
        }
    },
    mounted(){
        this.getData();
    }
}
</script>

<style>

</style>