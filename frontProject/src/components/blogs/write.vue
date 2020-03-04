<template>
  <div>
    <div class="writeBox">
      <h1 class="text-primary">写文章</h1>
      <h3 class="d-inline text-primary">标题:&nbsp;&nbsp;&nbsp;&nbsp;</h3>
      <input class="titleInput form-control" v-model="title" disabled>
      <mavon-editor
        v-model="value"
        :toolbars="toolbars"
        @imgAdd="addImg"
        @imgDel="delImg"
        @save="save"
        ref="md"
      />
      <b-modal id="modal" ref="modal" title="提示" hide-footer @hide="hide()">
      <h3>{{this.info}}</h3>
      <br />
      <br />
      <b-button block @click="hide()">确定</b-button>
    </b-modal>
    </div>
  </div>
</template>
<script>
import Axios from "axios"
export default {
  data() {
    return {
      value: "",
      imgs: {},
      title:"",
      tag:"",
      info:"",
      sortItems:[],
      toolbars: {
        bold: true, // 粗体
        italic: true, // 斜体
        header: true, // 标题
        underline: true, // 下划线
        strikethrough: true, // 中划线
        mark: true, // 标记
        superscript: true, // 上角标
        subscript: true, // 下角标
        quote: true, // 引用
        ol: true, // 有序列表
        ul: true, // 无序列表
        link: true, // 链接
        imagelink: true, // 图片链接
        code: true, // code
        table: true, // 表格
        fullscreen: true, // 全屏编辑
        readmodel: true, // 沉浸式阅读
        htmlcode: false, // 展示html源码
        help: true, // 帮助
        /* 1.3.5 */
        undo: true, // 上一步
        redo: true, // 下一步
        trash: true, // 清空
        save: true, // 保存（触发events中的save事件）
        /* 1.4.2 */
        navigation: true, // 导航目录
        /* 2.1.8 */
        alignleft: true, // 左对齐
        aligncenter: true, // 居中
        alignright: true, // 右对齐
        /* 2.2.1 */
        subfield: true, // 单双栏模式
        preview: true // 预览
      }
    };
  },
  methods: {
    f(){

    },
    hide(){
      this.$refs.modal.hide();
      this.f();
    },
    alert(info,f=this.f){
      this.info=info;
      this.f=f;
      this.$refs.modal.show();
    },
    getData(){
      this.title=this.$route.params.title;
      Axios.get("/api/edit/blog?title="+this.title).then(response=>{
        if(response.data.message=="success"){
          this.value=response.data.inner;
        }else if(response.data.message=="no signIn"){
          this.alert("你还没有登录!",()=>{
            this.$router.push("/user/signIn");
          });
        }else if(response.data.message=="none"){
          this.alert("没有这篇文章!",()=>{
            this.$router.push("/write/");
          })
        }
      })
    },
    addImg(pos, file) {
      var formData=new FormData();
      formData.append("img",file);
      Axios.post("/api/edit/uploadImg",formData,{
        headers:{
          "Content-Type":"multipart/form-data"
        }
      }).then((response)=>{
        var data=response.data;
        console.log(data)
        if(data.message=="no signIn"){
          this.$router.push("/user/signIn")
        }else{
          this.$refs.md.$img2Url(pos,data.url);
        }
      });
      this.imgs[pos] = file;
    },
    delImg(pos) {
      pos=pos[0];
      var urls=pos.split("/");
      var imgId=urls[urls.length-1];
      Axios.post("/api/edit/deleteImg?imgId="+imgId);
      delete this.imgs[pos];
    },
    save(md, html) {
      Axios.post("/api/blog/edit",{
        inner:this.value,
        title:this.title
      })
    }
  },
  mounted(){
    this.getData();
  }
};
</script>
<style scoped>
.writeBox {
  margin-top: 80px;
}
.titleInput{
  margin-top:20px;
  margin-bottom:20px;
  width:800px;
  height:50px;
  font-size: 30px;
  display:inline-block;
}
select.form-control{
  display:inline-block;
  width:400px;
  height:50px;
  font-size:30px;
}
.v-note-wrapper{
  z-index:1000;
}
</style>