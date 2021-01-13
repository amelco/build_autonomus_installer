try {
    const express = require('express')
    const app = express()
    const http = require('http').Server(app)
    const io = require('socket.io')(http)
    const zmq = require('zeromq')
  
    // socket to talk to server
    const requester = zmq.socket('req')
  
    console.log('Executando o socket...')
    requester.connect('tcp://localhost:8000')
  
    requester.on('message', function(reply) {
      io.emit('detection', reply.toString())
      requester.send('atualize')
  
      // TODO remover esse log
      console.log('Received reply: [', reply.toString(), ']')
    })
  
    // Start
    requester.send('establish connection')
  
    const server = http.listen(3001, () => {
      console.log('Socket is running on port', server.address().port)
    })
  } catch (e) {
    console.log(e)
    console.log('<--!!!Ambiente node é necessário estar configurado!!!-->')
  }
  