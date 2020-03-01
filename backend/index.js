const express = require('express')
const bodyParser = require('body-parser')
// corsポリシーに抵触するため、その対策としてcorsを利用する
const cors = require('cors')
var { PythonShell } = require('python-shell');

const app = express()
app.use(bodyParser.json())
app.use(cors())

app.post('/test', function (req, res) {
  var pyshell = new PythonShell('main.py');

  pyshell.send(JSON.stringify(req.body));

  pyshell.on('message', function (data) {
    res.send({
      result: data
    })
  });
})

app.listen(process.env.PORT || 3000)
