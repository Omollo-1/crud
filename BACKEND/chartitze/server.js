// chartitze/server.js
const corsOptions = {
  origin: 'http://localhost:3000', // Your frontend URL
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true, // If you need cookies/auth
  optionsSuccessStatus: 200
};

app.use(cors(corsOptions));