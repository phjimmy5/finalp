require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const mysql = require('mysql2');
const bcrypt = require('bcrypt');
const path = require('path');
const session = require('express-session');
const http = require('http');
const socketIo = require('socket.io');

// start up the server
const app = express();
const port = 3000;
const server = http.createServer(app);
const io = socketIo(server);

// use middleware to send form data
app.use(bodyParser.urlencoded({ extended: true }));

// serve static files from the public directory
app.use(express.static(path.join(__dirname, 'public')));

// initialize middlware
const sessionMiddleware = session({
  secret: 'SecretKey', 
  resave: false,
  saveUninitialized: true,
  cookie: { secure: false } // not using https
});


app.use(sessionMiddleware);

// initialize MySQL db connection
const db = mysql.createConnection({
  host: 'localhost',
  user: 'root', // my db username
  password: process.env.DB_PASSWORD, // my db password (protected in .env file)
  database: 'sampledb' // db name
});

// connect to the database
db.connect((err) => {
  if (err) throw err;
  console.log('Connected to MySQL database.');
});

//  handle the registration form submission
app.post('/register', async (req, res) => {
  const { username, email, password } = req.body;

  try {
    const password_hash = await bcrypt.hash(password, 10);
    const query = 'INSERT INTO userinfo (username, email, password_hash) VALUES (?, ?, ?)';
    
    db.query(query, [username, email, password_hash], (err) => {
      if (err) {
        console.error('Error during user registration:', err);
        return res.status(500).send('User registration failed.');
      }

      console.log('User registered successfully!');
      req.session.user = { username };
      return res.redirect('/dashboard');
    });
  } catch (error) {
    console.error('Error hashing password:', error);
    res.status(500).send('Internal server error');
  }
});

//handle the login form submission
app.post('/login', (req, res) => {
  const { username, password } = req.body;

  const query = 'SELECT * FROM userinfo WHERE username = ?';

  db.query(query, [username], async (err, results) => {
    if (err) throw err;

    if (results.length > 0) {
      const user = results[0];
      const match = await bcrypt.compare(password, user.password_hash);
      if (match) {
        req.session.user = { username };
        return res.redirect('/dashboard');
      } else {
        return res.send('Invalid credentials.');
      }
    } else {
      return res.send('Invalid credentials.');
    }
  });
});

// middleware to check if the user is logged in
function isAuthenticated(req, res, next) {
  if (req.session.user) {
    next();
  } else {
    res.redirect('/login.html');
  }
}

//route to get back to the dashboard (must be logged in)
app.get('/dashboard', isAuthenticated, (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'dashboard.html'));
});

// route to handle logout button
app.get('/logout', (req, res) => {
  req.session.destroy((err) => {
    if (err) {
      return res.status(500).send('Error logging out.');
    }
    res.redirect('/index.html');
  });
});

// middleware to handle session for Socket.IO
io.use((socket, next) => {
  sessionMiddleware(socket.request, {}, next);
});


io.on('connection', (socket) => {
  console.log('A user connected.');

  // check if user is authenticated
  if (socket.request.session && socket.request.session.user) {
    const username = socket.request.session.user.username; // retrieves username
    socket.emit('username', username); 

    // loads previous chat messages from the database when a user joins site
    db.query('SELECT * FROM chat_messages ORDER BY timestamp ASC', (err, results) => {
      if (err) throw err;
      results.forEach((row) => {
        socket.emit('chat message', `${row.username}: ${row.message}`);
      });
    });

    // displays message to users and saves it
    socket.on('chat message', (msg) => {
      const [username, message] = msg.split(': '); // Assuming username is in the format 'username: message'
      const query = 'INSERT INTO chat_messages (username, message) VALUES (?, ?)';
      db.query(query, [username, message], (err) => {
        if (err) throw err;
        console.log('Message saved to database');
      });

      
      io.emit('chat message', msg);
    });
  } else {
    console.error('User is not authenticated.');
    socket.disconnect(); //disconnects user if not logged in
  }

  socket.on('disconnect', () => {
    console.log('A user disconnected.');
  });
});

// initializes the server using local server
server.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
