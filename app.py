from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import or_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['POSTS_PER_PAGE'] = 6  # Number of posts per page
app.config['SECRET_KEY'] = 'secret_key'  # Add secret key for flash messages
db = SQLAlchemy(app)

@app.context_processor
def inject_now():
    return {
        'now': datetime.utcnow(),
        'year': datetime.utcnow().year
    }

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    subtitle = db.Column(db.String(300))
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(300))
    category = db.Column(db.String(50))
    featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tags = db.Column(db.String(200))  # Comma-separated tags
    reading_time = db.Column(db.Integer)  # Reading time in minutes

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        # Calculate reading time based on content length (assuming 200 words per minute)
        words = len(self.content.split())
        self.reading_time = max(1, round(words / 200))

with app.app_context():
    db.create_all()
    
    # Add sample posts if the database is empty
    if Post.query.count() == 0:
        sample_posts = [
            {
                'title': 'Getting Started with Flask',
                'subtitle': 'A beginner\'s guide to web development with Flask',
                'content': '''Flask is a lightweight WSGI web application framework that's perfect for building web applications. 
                In this guide, we'll explore the basics of Flask and how to create your first web application.

                Flask's simplicity and flexibility make it an excellent choice for both beginners and experienced developers. 
                Unlike larger frameworks, Flask gives you the freedom to choose your project's structure and libraries.

                Key Features of Flask:
                - Lightweight and modular design
                - Built-in development server and debugger
                - RESTful request dispatching
                - Jinja2 templating
                - Secure cookies support
                - WSGI 1.0 compliant
                - Unicode based
                - Extensive documentation

                Let's dive into creating your first Flask application!''',
                'category': 'Python',
                'featured': True,
                'tags': 'flask,python,web development',
                'image_url': 'https://picsum.photos/800/400?random=1'
            },
            {
                'title': 'Modern Web Design Principles',
                'subtitle': 'Essential principles for creating beautiful and functional websites',
                'content': '''Good web design is crucial for creating engaging and effective websites. 
                Let's explore the key principles that make a website stand out.

                1. Visual Hierarchy
                - Use size, color, and spacing to guide users
                - Highlight important elements
                - Create clear content sections

                2. Color Theory
                - Choose complementary colors
                - Maintain brand consistency
                - Use contrast effectively

                3. Typography
                - Select readable fonts
                - Maintain proper spacing
                - Create clear hierarchies

                4. Responsive Design
                - Ensure mobile compatibility
                - Flexible layouts
                - Optimized images''',
                'category': 'Design',
                'tags': 'web design,ux,ui',
                'image_url': 'https://picsum.photos/800/400?random=2'
            },
            {
                'title': 'Mastering CSS Grid Layout',
                'subtitle': 'Create complex layouts with CSS Grid',
                'content': '''CSS Grid has revolutionized web layout design, making it easier than ever to create complex, 
                responsive layouts. Here's what you need to know.

                CSS Grid Basics:
                - Two-dimensional layout system
                - Rows and columns
                - Gap spacing
                - Template areas

                Key Features:
                - Flexible track sizing
                - Item placement
                - Alignment control
                - Responsive design
                
                Best Practices:
                - Plan your grid structure
                - Use named grid areas
                - Implement fallbacks
                - Consider accessibility''',
                'category': 'CSS',
                'tags': 'css grid,layout',
                'image_url': 'https://picsum.photos/800/400?random=3'
            },
            {
                'title': 'JavaScript ES6+ Features',
                'subtitle': 'Modern JavaScript features you should know',
                'content': '''JavaScript has evolved significantly with ES6 and later versions. 
                Let's explore the most important features that make coding more efficient.

                1. Arrow Functions
                - Shorter syntax
                - Lexical this binding
                - Implicit returns

                2. Destructuring
                - Array destructuring
                - Object destructuring
                - Default values

                3. Template Literals
                - String interpolation
                - Multi-line strings
                - Tagged templates

                4. Promises and Async/Await
                - Asynchronous operations
                - Error handling
                - Cleaner code structure''',
                'category': 'JavaScript',
                'tags': 'javascript,programming',
                'image_url': 'https://picsum.photos/800/400?random=4'
            },
            {
                'title': 'Python Tips and Tricks',
                'subtitle': 'Advanced Python techniques to improve your code',
                'content': '''Python offers many powerful features that can make your code more efficient and readable. 
                Here are some advanced techniques you should know.

                1. List Comprehensions
                - Concise list creation
                - Filtering elements
                - Nested comprehensions

                2. Decorators
                - Function modification
                - Code reuse
                - Timing and logging

                3. Context Managers
                - Resource management
                - File handling
                - Database connections

                4. Generator Expressions
                - Memory efficiency
                - Lazy evaluation
                - Infinite sequences''',
                'category': 'Python',
                'tags': 'python,programming',
                'image_url': 'https://picsum.photos/800/400?random=5'
            },
            {
                'title': 'Database Design Best Practices',
                'subtitle': 'Creating efficient and scalable database structures',
                'content': '''When designing a database, it's essential to follow best practices for performance and maintainability.

                Key Principles:
                1. Normalization
                - Reduce redundancy
                - Maintain data integrity
                - Optimize storage

                2. Indexing Strategies
                - Primary keys
                - Foreign keys
                - Performance optimization

                3. Data Types
                - Choose appropriate types
                - Consider storage requirements
                - Plan for scaling

                4. Security
                - Access control
                - Data encryption
                - Backup strategies''',
                'category': 'Database',
                'tags': 'database design,sql',
                'image_url': 'https://picsum.photos/800/400?random=6'
            }
        ]
        
        for post_data in sample_posts:
            post = Post(
                title=post_data['title'],
                subtitle=post_data['subtitle'],
                content=post_data['content'],
                category=post_data['category'],
                featured=post_data.get('featured', False),
                tags=post_data.get('tags', ''),
                image_url=post_data.get('image_url', '')
            )
            db.session.add(post)
        
        db.session.commit()

@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    featured_post = Post.query.filter_by(featured=True).first()
    
    # Get paginated posts
    pagination = Post.query.filter_by(featured=False).order_by(Post.created_at.desc()).paginate(
        page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False
    )
    posts = pagination.items
    
    return render_template('home.html', 
                         featured_post=featured_post, 
                         posts=posts, 
                         pagination=pagination)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    
    if query:
        # Search in title, subtitle, content, and tags
        search_results = Post.query.filter(
            or_(
                Post.title.ilike(f'%{query}%'),
                Post.subtitle.ilike(f'%{query}%'),
                Post.content.ilike(f'%{query}%'),
                Post.tags.ilike(f'%{query}%')
            )
        ).order_by(Post.created_at.desc())
        
        # Paginate results
        pagination = search_results.paginate(
            page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False
        )
        posts = pagination.items
    else:
        pagination = None
        posts = []
    
    return render_template('search.html', 
                         query=query, 
                         posts=posts, 
                         pagination=pagination)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    
    # Get related posts based on category and tags
    if post.tags:
        post_tags = [tag.strip() for tag in post.tags.split(',')]
        related_posts = Post.query.filter(
            Post.id != post.id,
            or_(
                Post.category == post.category,
                *[Post.tags.ilike(f'%{tag}%') for tag in post_tags]
            )
        ).limit(3).all()
    else:
        related_posts = Post.query.filter(
            Post.id != post.id,
            Post.category == post.category
        ).limit(3).all()
    
    return render_template('post.html', post=post, related_posts=related_posts)

@app.route('/category/<string:category>')
def category(category):
    page = request.args.get('page', 1, type=int)
    
    # Get paginated posts for category
    pagination = Post.query.filter_by(category=category).order_by(
        Post.created_at.desc()
    ).paginate(page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    
    posts = pagination.items
    return render_template('category.html', 
                         category=category, 
                         posts=posts, 
                         pagination=pagination)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # Here you would typically send an email or store the message
        # For now, we'll just flash a success message
        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

if __name__ == '__main__':
    app.run(debug=True)
