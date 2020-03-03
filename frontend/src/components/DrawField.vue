<template>
  <div>
    <h1>{{ msg }}</h1>
    <h3>Q. {{ question.left_item + ' ' + question.operator + ' ? = ' + question.right_item }}</h3>
    <h3>Your Answer: {{ answer }}</h3>
    <h3 id="result">
      Result:
      <font-awesome-icon id="result_ok" style="display: none;" :icon="['far', 'circle']" />
      <font-awesome-icon id="result_ng" style="display: none;" :icon="['fas', 'times']" />
    </h3>

    <canvas id="canvas" width="420" height="420" style="background: #000000;" @mousedown="draw_activate()" @mousemove="get_current_position($event)" @mouseup="draw_deactivate()"></canvas>
    <div>
      <button @click="refresh_canvas">
        <font-awesome-icon :icon="['fas', 'redo']" />
      </button>
      <button @click="post">
        <font-awesome-icon :icon="['fas', 'check-circle']" />
      </button>
      <button @click="refresh">
        <font-awesome-icon :icon="['fas', 'sync-alt']" />
      </button>
    </div>
  </div>
</template>

<script>
import Methods from '@/api/methods'

export default {
  data() {
    return {
      msg: 'Fill in the Blank',
      question: {
        left_item: null,
        operator: '',
        right_item: null
      },
      is_active: 0,
      state_sub: 'DrawUnTerminable',
      initial_place: null,
      input_data: 1,
      answer: null,
      correct_answer: 2
    }
  },
  beforeMount() {
    this.refresh_question()
  },
  methods: {
    refresh() {
      this.refresh_canvas()
      this.refresh_question()
    },
    refresh_canvas() {
      // Canvasを真っ黒にする
      let canvas = document.getElementById('canvas')
      let ctx = canvas.getContext('2d')
      ctx.clearRect(0, 0, canvas.width, canvas.height)
    },
    refresh_question() {
      // 正解は0-9のいずれか
      this.correct_answer = Math.floor(Math.random() * (9 - 0) + 0)
      // 演算子は+,-,*,/のいずれか
      let operators = ['+', '-', '*', '/']
      this.question.operator = operators[Math.floor(Math.random() * operators.length)]

      switch (this.question.operator) {
        case '+':
          this.question.left_item = Math.floor(Math.random() * (100 - 1) + 1)
          this.question.right_item = this.question.left_item + this.correct_answer
          console.log(this.question)
          break
        case '-':
          this.question.left_item = Math.floor(Math.random() * (100 - 1) + 1)
          this.question.right_item = this.question.left_item - this.correct_answer
          console.log(this.question)
          break
        case '*':
          this.question.left_item = Math.floor(Math.random() * (100 - 1) + 1)
          this.question.right_item = this.question.left_item * this.correct_answer
          console.log(this.question)
          break
        case '/':
          this.question.right_item = Math.floor(Math.random() * (100 - 1) + 1)
          this.question.left_item = this.question.right_item * this.correct_answer
          console.log(this.question)
          break
      }
    },
    // サーバーから返ってくる値をログに出力したいのでasyncとawaitを行う
    async post() {
      let canvas = document.getElementById('canvas')
      let ctx = canvas.getContext('2d')
      let image_data = ctx.getImageData(0, 0, canvas.width, canvas.height)
      let draw_image_pixel_values = []

      const resize_count = canvas.width / 28
      let image_pixels = 0

      for (let x = 0; x < canvas.height; x += resize_count) {
        for (let y = 0; y < canvas.width; y += resize_count) {
          image_pixels = 0

          for (let d_y = 0; d_y < resize_count; ++d_y) {
            for (let d_x = 0; d_x < resize_count; ++d_x) {
              image_pixels += image_data.data[(x + d_x) * (image_data.width * 4) + (y + d_y) * 4]
            }
          }
          // 入力値って0から1だっけ？
          draw_image_pixel_values.push(image_pixels / 255.0)
        }
      }
      console.log(draw_image_pixel_values)
      let response = await Methods.testPosting(draw_image_pixel_values)
      console.log(typeof response.data.result)
      /* response.data.resultはstring型で[3]みたいな形で返却されるので、
       * [と]を除去する
       */
      this.answer = response.data.result.replace(/[\[\]]/g, '')

      if (this.correct_answer == this.answer) {
        document.getElementById('result_ng').style.display = 'none'
        document.getElementById('result_ok').style.display = ''
        console.log('ok')
      } else {
        document.getElementById('result_ok').style.display = 'none'
        document.getElementById('result_ng').style.display = ''
        console.log('ng')
      }
    },
    draw_activate() {
      document.addEventListener('mousemove', this.draw)
    },
    draw_deactivate() {
      this.is_active = 0
      document.removeEventListener('mousemove', this.draw)
    },
    get_current_position(event) {
      let newx = event.offsetX
      let newy = event.offsetY
      this.current_x = newx
      this.current_y = newy
    },
    draw() {
      if (!this.is_active) {
        this.last_draw_x = this.current_x
        this.last_draw_y = this.current_y
        this.draw_core(this.last_draw_x, this.last_draw_y, this.current_x, this.current_y)
        this.is_active = 1
      } else {
        this.draw_core(this.last_draw_x, this.last_draw_y, this.current_x, this.current_y)
        this.last_draw_x = this.current_x
        this.last_draw_y = this.current_y
      }
    },
    draw_core(x, y, nx, ny) {
      let canvas = document.getElementById('canvas')
      let ctx = canvas.getContext('2d')
      ctx.beginPath()
      ctx.strokeStyle = '#ffffff'
      ctx.lineWidth = 20
      ctx.moveTo(x, y)
      ctx.lineTo(nx, ny)
      ctx.stroke()
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1,
h2 {
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
button {
  background-color: #1e90ff;
  border-radius: 50%;
  color: white;
  padding: 12px 12px;
  margin: 10px;
  font-size: 16px;
  cursor: pointer;
  user-select: none; /* 選択できないようにする */
  outline: 0; /* クリック時の枠線を消す */
}
button:hover {
  background-color: #0d2e8f;
  color: white;
}
#result_ok {
  color: #0dff00;
}
#result_ng {
  color: #ff1d1dee;
}
</style>
