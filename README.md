# Modern Flask Blog

A modern, responsive blog built with Flask, featuring a clean design and powerful features.

## Features

- 🎨 Modern, responsive design
- 🔍 Search functionality
- 📱 Mobile-friendly interface
- 🏷️ Category and tag filtering
- ⭐ Featured posts
- 📝 Rich blog post content
- 📊 Reading time estimation
- 📱 Contact form
- 📄 Pagination
- 🔗 Related posts

## Tech Stack

- Flask
- SQLAlchemy
- SQLite
- HTML/CSS
- JavaScript

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd blog
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Visit `http://localhost:5000` in your browser

## Project Structure

```
blog/
├── app.py              # Main application file
├── requirements.txt    # Project dependencies
├── static/            # Static files (CSS, JS, images)
├── templates/         # HTML templates
│   ├── base.html     # Base template
│   ├── home.html     # Home page
│   ├── post.html     # Individual post
│   └── ...          # Other templates
└── instance/         # Instance-specific files
    └── blog.db       # SQLite database
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
