<template>
  <div class="bg" align="center">
    <div class="content" ref="content" align="left">
      <div class="row">
        <div class="col-11">
          <h1>{{data.blog.title}}<small>赞:{{data.blog.good}}</small></h1>
        </div>
        <div class="col-1 ml-auto blogGoodBox" align="right">
          <button class="btn btn-primary" @click="blogGood">赞</button>
        </div>
      </div>
      <hr />
      <div class="inner" v-html="data.blog.inner">{{data.blog.inner}}</div>
      <hr />
      <div>
        <h3 class="text-primary">我要评论</h3>
        <div class="row">
          <div class="col-8">
            <textarea class="form-control d-block rounded" v-model="plText"></textarea>
          </div>
          <div class="col-4">
            <button class="btn btn-primary" @click="pl">发表</button>
          </div>
        </div>
        <hr />
        <div>
          <div v-for="pl in data.pls" :key="pl" class="pl">
            <div class="row">
              <div class="col-8">
                <div>
                  <h4
                    class="text-primary"
                  >[{{pl.date}}]{{pl.user}}</h4>
                </div>
                {{pl.inner}}
              </div>
              <div class="col-4">
                <div class="row">
                  <div class="col-6">
                    <h4 class="text-primary">
                      <small>赞数:{{pl.goodNum}}</small>
                    </h4>
                  </div>
                  <div class="col-6">
                    <button class="btn btn-primary" v-bind:id="'good'+pl.id" @click="good">赞</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Axios from "axios";
import "../../assets/code.css";
export default {
  data() {
    return {
      data: {
        blog: {
          title: "",
          inner: ""
        }
      },
      plText:""
    };
  },
  methods: {
    getData() {
      Axios.get("/api/page/blog?id=" + this.$route.params.id).then(response => {
        var data = response.data;
        if (data.message == "success") {
          this.data = data;
        } else if (data.message == "the id is wrong") {
          this.$router.push("/Error/404");
        }
      });
    },
    pl() {
        Axios.post("/api/blog/pl",{
            blog:this.data.blog.id,
            inner:this.plText
        }).then((response)=>{
            this.getData();
        })
    },
    good(e){
        var id=parseInt(e.target.id.slice(4));
        console.log(e.target.id);
        Axios.post("/api/blog/good",{
            id:id
        }).then(()=>{
            this.getData();
        })
    },
    blogGood(){
      Axios.post("/api/blog/blogGood",{
        id:this.data.blog.id
      }).then(response=>{
        if(response.message=="no signIn"){
          this.$router.push("/user/signIn");
        }else{
          this.getData();
        }
      })
    }
  },
  mounted() {
    this.getData();
  }
};
</script>
<style scoped>
.bg {
  padding-top: 1px;
  width: 100%;
  height: 100%;
  background-color: lemonchiffon;
  overflow: auto;
}
.content {
  display: inline-block;
  margin-top: 100px;
  min-width: 800px;
  max-width:1200px;
  min-height: 600px;
  padding-left: 30px;
  padding-right: 30px;
  margin-left: auto;
  margin-right: auto;
  background-color: beige;
}
.pl {
  background-color: whitesmoke;
  border-radius: 10px;
  margin-top: 20px;
  margin-bottom: 20px;
  padding-left: 30px;
  padding-right: 30px;
  padding-top: 20px;
  padding-bottom: 10px;
}
.blogGoodBox{
  padding-top:20px;
}
</style>