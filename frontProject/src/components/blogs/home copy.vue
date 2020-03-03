<template>
    <div class="row bg h-100">
        <div class="col-2 leftBox">
            <h3 class="text-primary">
                分类浏览
            </h3>
            <router-link v-for="item in sortItems" :key="item" v-bind:to="'/tag/'+item" tag="div" class="item">{{item}}</router-link>
        </div>
        <div class="col-9 rightBox" align="center">
            <div class="newBox">
                <b-carousel
                    id="news"
                    :interval="2000"
                    controls
                    indicators
                >
                    <b-carousel-slide v-for="text in texts" :key="text">
                        <template v-slot:img>
                            <img v-bind:src="getImg(text)" class="img-fluid newsImg" width="700">
                        </template>
                    </b-carousel-slide>
                </b-carousel>
            </div>
            <div class="row">

            </div>
        </div>
    </div>
</template>
<script>
import Axios from "axios";
export default {
    name:"home",
    data(){
        return {
            "sortItems":[],
            "newBlogs":[],
            "texts":[]
        }
    },
    methods:{
        getData(){
            const api="/api/page/home";
            Axios.get(api,{
                params:{
                    num:30,
                }
            }).then(response=>{
                if(response.data.message=="success"){
                    this.sortItems=response.data.sortItems;
                    this.newBlogs=response.data.newBlogs;
                    this.texts=response.data.texts;
                }else{
                    alert("something wrong");
                }
            }).catch(error=>{
                console.log(error);
            })
        },
        getImg(text){
            var canvas=document.createElement("canvas");
            var ctx=canvas.getContext("2d");
            var len=text.length;
            var lineWidth=7;
            var linelen=0;
            var l=0;
            var linenum=0;
            var lx=0;
            for(var i=0;i<len;i++){
                if(text[i]=="%"||lx%lineWidth==lineWidth-1){
                    linelen=Math.max(l,linelen);
                    l=0;
                    linenum++;
                    lx=0;
                }else{
                    l++;
                    lx++;
                }
            }
            linelen=Math.max(l,linelen);
            linenum++;
            ctx.font="100px 华文琥珀";
            canvas.width=linelen*100+20;
            canvas.height=linenum*100+20;
            ctx.font="100px 华文琥珀";
            ctx.fillStyle="white";
            ctx.fillRect(0,0,canvas.width,canvas.height);
            ctx.fillStyle="skyblue";
            ctx.fillRect(parseInt(linelen/2)*100+5,0,canvas.width-parseInt(linelen/2)*100-5,canvas.height);
            ctx.textAlign="left";
            ctx.textBaseline="top";
            var y=10;
            var x=10;
            var lx=0;
            for(var i=0;i<len;i++){
                if(lx<parseInt(linelen/2)){
                    ctx.fillStyle="skyblue";
                }else{
                    ctx.fillStyle="white";
                }
                if(text[i]!="%"){
                    var offsetx=100/2-ctx.measureText(text[i]).width/2;
                    ctx.fillText(text[i],x+offsetx,y);
                    x+=100;
                }
                
                if(lx%lineWidth==lineWidth-1||text[i]=="%"){
                    y+=100;
                    x=0;
                    lx=0;
                }else{
                    lx++;
                }
            }
            var img=new Image();
            return canvas.toDataURL("image/png");
        }
    },
    mounted(){
        this.getData();
    }
}
</script>
<style scoped>
.bg{
    background-color: azure;
}
.leftBox,.rightBox{
    margin-top: 50px;
    padding-left:30px;
    padding-top:30px;
}
.leftBox{
    background-color: skyblue;
}
.item{
    background-color: orange;
    margin-top:10px;
    margin-bottom:10px;
    border-radius:20px;
    height:40px;
    padding-left:20px;
    transition: .4s;
    color:white;
    font-size:20px;
    text-decoration: none;
}
.item:hover{
    margin-left:20px;
    margin-right:20px;
    background-color: orangered;
    cursor: pointer;
}
.newBox{
    border-radius: 20px;
    background-color: dodgerblue;
}
.newsImg{
    border-radius: 20px;
}
</style>