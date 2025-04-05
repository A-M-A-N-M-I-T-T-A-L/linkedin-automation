# LinkedIn Automation Tool

An open-source tool for automating LinkedIn job search and networking, running locally on your PC for enhanced privacy and security.

## Features

- 🤖 Automated job parsing and analysis
- 🤝 Smart connection request management
- 📊 Beautiful analytics dashboard
- 🔒 Local data storage for privacy
- 📈 Resume optimization recommendations
- 🎯 Customizable job search filters

## Prerequisites

- Python 3.8+
- Chrome browser
- LinkedIn account
- Rust compiler (if building from source)

### Installing Rust (if needed)
Windows:
```bash
# Download and run rustup-init.exe from https://rustup.rs/
rustup-init.exe
```

Linux/MacOS:
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/linkedin-automation.git
cd linkedin-automation
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install requirements:
```bash
pip install -r requirements.txt
```

4. Set up your environment variables:
   - Copy `secrets.env.example` to `secrets.env`
   - Fill in your LinkedIn credentials and other settings

## Configuration

Update `secrets.env` with your settings:

```env
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_password
MAX_JOBS_TO_PARSE=100
MAX_CONNECTIONS_PER_DAY=20
```

## Usage

1. Start the automation:
```bash
python main.py
```

2. Launch the dashboard:
```bash
streamlit run dashboard/app.py
```

3. Monitor your progress through the dashboard at `http://localhost:8501`

## Features in Detail

### Job Parsing
- Automatically scans LinkedIn job recommendations
- Analyzes job descriptions using AI
- Filters jobs based on your criteria
- Stores job data locally for privacy

### Connection Management
- Sends personalized connection requests
- Tracks connection request status
- Prevents duplicate requests
- Respects LinkedIn's daily limits
- Rotates through multiple message templates

### Analytics Dashboard
- Real-time connection statistics
- Job parsing metrics
- Success rate tracking
- Resume optimization suggestions
- Skills gap analysis

## Safety & Privacy

- All data is stored locally on your PC
- No external API calls except LinkedIn
- Respects LinkedIn's rate limits
- Proxy support for additional privacy

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) first.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for educational purposes only. Use it responsibly and in accordance with LinkedIn's terms of service.
