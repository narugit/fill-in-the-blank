<template>
  <div>
    <h1>{{ msg }}</h1>
    <div><button @click='post'>click me</button></div>
  <canvas id="canvas" width="560" height="560" style="background: #000000;"
    @mousedown="draw_activate()"
   @mousemove="get_current_position($event)"
   @mouseup="draw_deactivate()"
  ></canvas>
    
  </div>
</template>

<script>
import Methods from '@/api/methods'

export default {
  name: 'HelloWorld',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      is_active: 0,
      state_sub: 'DrawUnTerminable',
      initial_place: null,
      input_data: 1
    }
  },
  methods: {
    // サーバーから返ってくる値をログに出力したいのでasyncとawaitを行う
    async post() {
      let canvas = document.getElementById('canvas')
      let ctx = canvas.getContext('2d')
      let image_data = ctx.getImageData(0, 0, canvas.width, canvas.height);
      let draw_image_pixel_values = []

      const resize_count = canvas.width / 28
      let image_pixels = 0

      for(let x = 0; x < canvas.height; x += resize_count){
    //   for(let x = 0; x < canvas.height; x += 1){
        for(let y = 0; y < canvas.width; y += resize_count){
        // for(let y = 0; y < canvas.width; y += 1){
          image_pixels = 0
        //   image_pixels += image_data.data[x*image_data.width*4 + y*4]

          for(let d_y = 0; d_y < resize_count; ++d_y){
            for(let d_x = 0; d_x < resize_count; ++d_x){
              image_pixels += image_data.data[(((x+d_x)*(image_data.width*4)) + ((y+d_y)*4))]
            }
          }
          // 入力値って0から1だっけ？
          draw_image_pixel_values.push(image_pixels / 255.0)
        }
      }
    　　
      console.log(draw_image_pixel_values)
      let response = await Methods.testPosting(draw_image_pixel_values)
      console.log(response.data.result)
    },
    draw_activate(){
      document.addEventListener("mousemove", this.draw);
    },
    draw_deactivate(){
      this.is_active = 0
      document.removeEventListener("mousemove", this.draw);
    },
    get_current_position(event){
      let newx = event.offsetX;
      let newy = event.offsetY;
      this.current_x = newx;
      this.current_y = newy;
    },
    draw() {
        if(!this.is_active){
            this.last_draw_x = this.current_x;
          this.last_draw_y = this.current_y;
        this.draw_core(this.last_draw_x, this.last_draw_y,this.current_x,this.current_y);
            this.is_active = 1

        }else{
            this.draw_core(this.last_draw_x, this.last_draw_y,this.current_x,this.current_y);
            this.last_draw_x = this.current_x;
          this.last_draw_y = this.current_y;

        }
    },
    draw_core(x,y,nx,ny) {
      let canvas = document.getElementById("canvas")
      let ctx = canvas.getContext("2d")
      ctx.beginPath();
      ctx.strokeStyle = '#ffffff'
      ctx.lineWidth = 20;
      ctx.moveTo(x, y);
      ctx.lineTo(nx, ny);
      ctx.stroke();
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
