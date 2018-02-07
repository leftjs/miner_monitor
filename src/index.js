import express from 'express'

const app = express()

app.get('/wechat', (req, res) => {
  res.send('hello')
})
const port = process.env.PORT || 3000

app.listen(port, (err) => {
  if (err) {
    console.error(err)
  }

  if (__DEV__) { // webpack flags!
    console.log('> in development')
  }

  console.log(`> listening on port ${port}`)
})