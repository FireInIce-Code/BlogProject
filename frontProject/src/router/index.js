import Vue from "vue";
import Router from "vue-router";
import signs from "@/components/signs/signs";
import signIn from "@/components/signs/signIn";
import signUp from "@/components/signs/signUp";
import info from "@/components/signs/info";
import home from "@/components/blogs/home";
import write from "@/components/blogs/write";
import myBlogs from "@/components/blogs/myBlogs";
import blogView from "@/components/blogs/blog";
import tag from "@/components/blogs/tagBlog";
import test from "@/components/test/test";
Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/test",
      component: test
    },
    {
      path: "/",
      name: "home",
      component: home
    },
    {
      path: "/write/:title",
      name: "write",
      component: write
    },
    {
      path: "/write",
      name: "myBlogs",
      component: myBlogs
    },
    {
      path: "/blogs/:id",
      name: "blog",
      component: blogView
    },
    {
      path: "/user",
      name: "signs",
      component: signs,
      children: [
        {
          path: "signIn",
          name: "signIn",
          component: signIn
        },
        {
          path: "signUp",
          name: "signUp",
          component: signUp
        }
      ]
    },
    {
      path: "/info",
      name: "info",
      component: info
    },
    {
      path: "/info/:userId",
      name: "userInfo",
      component: info
    },
    {
      path:"/tag/:tag",
      name:"tag",
      component: tag
    }
  ]
});
