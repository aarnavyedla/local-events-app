# Local Events Finder

A web app that helps users find upcoming events in their area, built with Python FastAPI and a vanilla JS frontend.

**Time spent: ~1.5 hours**

---

## Prerequisites
- Python 3.8+
- A free Ticketmaster API key from [developer.ticketmaster.com](https://developer.ticketmaster.com)

## Installation

1. Clone the repo
```bash
   git clone https://github.com/YOUR_USERNAME/local-events-app.git
   cd local-events-app
```

2. Install dependencies
```bash
   pip install -r requirements.txt
```

3. Create a `.env` file in the root directory using `.env.example` as a template
TICKETMASTER_API_KEY=your_api_key_here

4. Run the app
```bash
   python main.py
```

5. Open your browser and go to `http://localhost:8000`