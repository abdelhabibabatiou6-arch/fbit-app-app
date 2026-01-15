const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const multer = require('multer');
const path = require('path');
const fs = require('fs');

const app = express();
const port = 3000;

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(cookieParser());
app.use(express.static('public'));

// Database setup
const db = new sqlite3.Database(':memory:'); // In-memory for simplicity, use file for persistence

db.serialize(() => {
  db.run("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)");
  db.run("INSERT INTO users (username, password) VALUES ('admin', 'password')");
  db.run("INSERT INTO users (username, password) VALUES ('user', 'pass')");
});

// Routes

// Home page - login form
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Login - vulnerable to SQL injection
app.post('/login', (req, res) => {
  const { username, password } = req.body;
  const query = `SELECT * FROM users WHERE username = '${username}' AND password = '${password}'`; // Vulnerable
  db.get(query, (err, row) => {
    if (err) {
      res.send('Error');
    } else if (row) {
      res.cookie('session', 'loggedin', { httpOnly: false }); // Insecure cookie
      res.redirect('/dashboard');
    } else {
      res.send('Invalid credentials');
    }
  });
});

// Dashboard
app.get('/dashboard', (req, res) => {
  if (req.cookies.session === 'loggedin') {
    res.send(`
      <h1>Welcome to Dashboard</h1>
      <a href="/search">Search</a><br>
      <a href="/upload">Upload File</a><br>
      <form action="/logout" method="POST">
        <input type="submit" value="Logout">
      </form>
    `);
  } else {
    res.redirect('/');
  }
});

// Logout
app.post('/logout', (req, res) => {
  res.clearCookie('session');
  res.redirect('/');
});

// Search page
app.get('/search', (req, res) => {
  if (req.cookies.session === 'loggedin') {
    res.sendFile(path.join(__dirname, 'public', 'search.html'));
  } else {
    res.redirect('/');
  }
});

// Search - vulnerable to XSS
app.post('/search', (req, res) => {
  if (req.cookies.session === 'loggedin') {
    const query = req.body.query;
    // Simulate search results
    const results = `<p>Search results for: ${query}</p>`; // Vulnerable to XSS
    res.send(`
      <h1>Search Results</h1>
      ${results}
      <a href="/dashboard">Back</a>
    `);
  } else {
    res.redirect('/');
  }
});

// Upload page
app.get('/upload', (req, res) => {
  if (req.cookies.session === 'loggedin') {
    res.sendFile(path.join(__dirname, 'public', 'upload.html'));
  } else {
    res.redirect('/');
  }
});

// File upload - no validation
const upload = multer({ dest: 'uploads/' });
app.post('/upload', upload.single('file'), (req, res) => {
  if (req.cookies.session === 'loggedin') {
    res.send('File uploaded successfully');
  } else {
    res.redirect('/');
  }
});

// Directory traversal example - serve files
app.get('/file', (req, res) => {
  const file = req.query.path;
  res.sendFile(path.join(__dirname, file)); // Vulnerable
});

app.listen(port, () => {
  console.log(`Vulnerable website running at http://localhost:${port}`);
});